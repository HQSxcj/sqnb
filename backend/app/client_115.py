import qrcode
import io
import base64
import asyncio
from typing import Dict, List, Optional

class MockP115Client:
    def __init__(self):
        pass
        
    async def login_qrcode_token(self):
        return {'uid': 'mock_uid_12345', 'time': '1234567890'}
        
    async def login_qrcode(self, uid):
        return True
        
    @classmethod
    def from_cookie(cls, cookies):
        return cls()
        
    async def get_user_info(self):
        return {'user_id': 'mock_user', 'user_name': '测试用户'}
        
    async def get_file_list(self, cid="0"):
        return {
            'files': [
                {
                    'name': '示例电影.mp4',
                    'is_directory': False,
                    'size': 1073741824,
                    'modified_time': '2024-01-01 12:00:00',
                    'file_id': '1001',
                    'parent_id': '0'
                },
                {
                    'name': '电视剧',
                    'is_directory': True,
                    'size': 0,
                    'modified_time': '2024-01-01 12:00:00',
                    'file_id': '1002',
                    'parent_id': '0'
                }
            ]
        }
        
    async def search(self, keyword):
        return {'files': []}

# 使用模拟客户端
try:
    from p115client import P115Client
    print("Using real p115client")
except ImportError:
    print("Using mock p115client")
    P115Client = MockP115Client

class Client115:
    def __init__(self):
        self.client = None
        self.is_logged_in = False
    
    async def generate_qr_code(self) -> Dict:
        try:
            self.client = P115Client()
            qr_info = await self.client.login_qrcode_token()
            
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(qr_info['uid'])
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return {
                "success": True,
                "qrcode": f"data:image/png;base64,{img_str}",
                "uid": qr_info['uid'],
                "time": qr_info.get('time', '')
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def check_qr_login(self, uid: str) -> Dict:
        try:
            await asyncio.sleep(2)
            self.is_logged_in = True
            return {
                "success": True,
                "status": "success",
                "message": "登录成功",
                "user_info": {"user_id": "test_user", "user_name": "测试用户"}
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def login_with_cookie(self, cookie_str: str) -> Dict:
        try:
            self.client = P115Client.from_cookie({})
            self.is_logged_in = True
            return {
                "success": True, 
                "message": "登录成功",
                "user_info": {"user_id": "test_user", "user_name": "测试用户"}
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def get_file_list(self, path: str = "/", cid: str = "0") -> Dict:
        try:
            files_data = await self.client.get_file_list(cid=cid)
            files = []
            for item in files_data.get('files', []):
                file_info = {
                    "name": item.get('name', ''),
                    "type": "folder" if item.get('is_directory') else "file",
                    "size": self._format_size(item.get('size', 0)),
                    "modified": item.get('modified_time', ''),
                    "file_id": item.get('file_id', ''),
                    "parent_id": item.get('parent_id', ''),
                    "icon": "fa-folder" if item.get('is_directory') else self._get_file_icon(item.get('name', ''))
                }
                files.append(file_info)
            
            return {
                "success": True,
                "files": files,
                "current_path": path,
                "current_cid": cid
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def search_files(self, keyword: str) -> Dict:
        return {
            "success": True,
            "files": [],
            "keyword": keyword
        }
    
    def _format_size(self, size_bytes: int) -> str:
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.2f} {size_names[i]}"
    
    def _get_file_icon(self, filename: str) -> str:
        ext = filename.lower().split('.')[-1] if '.' in filename else ''
        video_exts = ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'm4v']
        if ext in video_exts:
            return "fa-file-video"
        else:
            return "fa-file"
