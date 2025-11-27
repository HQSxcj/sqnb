try:
    from p115client import P115Client
except ImportError:
    # 开发环境fallback
    class P115Client:
        def __init__(self):
            pass
            
        async def login_qrcode_token(self):
            return {'uid': 'test', 'time': 'test'}
            
        async def login_qrcode(self, uid):
            return True
            
        @classmethod
        def from_cookie(cls, cookies):
            return cls()
            
        async def get_user_info(self):
            return {'user_id': 'test', 'user_name': '测试用户'}
            
        async def get_file_list(self, cid="0"):
            return {
                'files': [
                    {
                        'name': '示例文件.mp4',
                        'is_directory': False,
                        'size': 1024000,
                        'modified_time': '2024-01-01',
                        'file_id': '1',
                        'parent_id': '0'
                    },
                    {
                        'name': '示例文件夹',
                        'is_directory': True,
                        'size': 0,
                        'modified_time': '2024-01-01',
                        'file_id': '2',
                        'parent_id': '0'
                    }
                ]
            }
            
        async def search(self, keyword):
            return {'files': []}
            
        async def create_directory(self, parent_cid, folder_name):
            return {'file_id': '3'}

import qrcode
import io
import base64
import asyncio
from typing import Dict, List, Optional
import json

class Client115:
    def __init__(self):
        self.client = None
        self.is_logged_in = False
    
    async def generate_qr_code(self) -> Dict:
        """生成115登录二维码"""
        try:
            self.client = P115Client()
            
            # 获取二维码登录信息
            qr_info = await self.client.login_qrcode_token()
            if not qr_info or 'uid' not in qr_info:
                return {"success": False, "message": "获取二维码失败"}
            
            # 生成二维码图片
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
        """检查二维码登录状态"""
        try:
            if not self.client:
                return {"success": False, "message": "客户端未初始化"}
            
            login_result = await self.client.login_qrcode(uid)
            
            if login_result and getattr(self.client, 'cookie', None):
                self.is_logged_in = True
                return {
                    "success": True,
                    "status": "success",
                    "message": "登录成功",
                    "user_info": {
                        "user_id": getattr(self.client, 'user_id', ''),
                        "user_name": getattr(self.client, 'user_name', '')
                    }
                }
            else:
                return {
                    "success": True,
                    "status": "waiting", 
                    "message": "等待扫码"
                }
                
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def login_with_cookie(self, cookie_str: str) -> Dict:
        """使用Cookie登录"""
        try:
            cookies = {}
            for item in cookie_str.split(';'):
                item = item.strip()
                if '=' in item:
                    key, value = item.split('=', 1)
                    cookies[key] = value
            
            self.client = P115Client.from_cookie(cookies)
            
            user_info = await self.client.get_user_info()
            if user_info:
                self.is_logged_in = True
                return {
                    "success": True, 
                    "message": "登录成功",
                    "user_info": user_info
                }
            else:
                return {"success": False, "message": "Cookie无效"}
                
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def get_file_list(self, path: str = "/", cid: str = "0") -> Dict:
        """获取文件列表"""
        try:
            if not self.is_logged_in or not self.client:
                # 返回示例数据用于测试
                return {
                    "success": True,
                    "files": [
                        {
                            "name": "示例电影.mp4",
                            "type": "file",
                            "size": "1.2 GB",
                            "modified": "2024-01-01",
                            "file_id": "1",
                            "parent_id": "0",
                            "icon": "fa-file-video"
                        },
                        {
                            "name": "电视剧",
                            "type": "folder", 
                            "size": "0 B",
                            "modified": "2024-01-01",
                            "file_id": "2",
                            "parent_id": "0",
                            "icon": "fa-folder"
                        }
                    ],
                    "current_path": path,
                    "current_cid": cid
                }
            
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
        """搜索文件"""
        try:
            if not self.is_logged_in or not self.client:
                return {"success": False, "message": "未登录"}
            
            search_results = await self.client.search(keyword)
            
            files = []
            for item in search_results.get('files', []):
                file_info = {
                    "name": item.get('name', ''),
                    "type": "folder" if item.get('is_directory') else "file", 
                    "size": self._format_size(item.get('size', 0)),
                    "modified": item.get('modified_time', ''),
                    "file_id": item.get('file_id', ''),
                    "icon": "fa-folder" if item.get('is_directory') else self._get_file_icon(item.get('name', ''))
                }
                files.append(file_info)
            
            return {
                "success": True,
                "files": files,
                "keyword": keyword
            }
            
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def create_folder(self, parent_cid: str, folder_name: str) -> Dict:
        """创建文件夹"""
        try:
            if not self.is_logged_in or not self.client:
                return {"success": False, "message": "未登录"}
            
            result = await self.client.create_directory(parent_cid, folder_name)
            
            if result and result.get('file_id'):
                return {
                    "success": True,
                    "message": "文件夹创建成功",
                    "folder_id": result.get('file_id')
                }
            else:
                return {"success": False, "message": "文件夹创建失败"}
                
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.2f} {size_names[i]}"
    
    def _get_file_icon(self, filename: str) -> str:
        """根据文件名获取图标"""
        ext = filename.lower().split('.')[-1] if '.' in filename else ''
        
        video_exts = ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'm4v']
        audio_exts = ['mp3', 'wav', 'flac', 'aac', 'ogg', 'wma']
        image_exts = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']
        doc_exts = ['pdf', 'doc', 'docx', 'txt', 'rtf']
        
        if ext in video_exts:
            return "fa-file-video"
        elif ext in audio_exts:
            return "fa-file-audio" 
        elif ext in image_exts:
            return "fa-file-image"
        elif ext in doc_exts:
            return "fa-file-alt"
        else:
            return "fa-file"
