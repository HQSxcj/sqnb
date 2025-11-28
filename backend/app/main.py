from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import platform
import uvicorn
import json
import os
from datetime import datetime

# 读取版本信息
def get_version_info():
    try:
        with open('/app/version.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading version.json: {e}")
        return {
            "version": "v0.0.1-dev",
            "build_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "commit_hash": "unknown"
        }

app = FastAPI(title="115网盘管理工具", version="0.0.1")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模拟115客户端
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
                    'name': f'示例电影-{platform.machine()}.mp4',
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
    print(f"Using real p115client on {platform.machine()}")
except ImportError:
    print(f"Using mock p115client on {platform.machine()}")
    P115Client = MockP115Client

import qrcode
import io
import base64
import asyncio

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
                "time": qr_info.get('time', ''),
                "architecture": platform.machine()
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def check_qr_login(self, uid: str):
        try:
            await asyncio.sleep(2)
            self.is_logged_in = True
            return {
                "success": True,
                "status": "success",
                "message": "登录成功",
                "user_info": {
                    "user_id": "test_user", 
                    "user_name": "测试用户",
                    "architecture": platform.machine()
                }
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def login_with_cookie(self, cookie_str: str):
        try:
            self.client = P115Client.from_cookie({})
            self.is_logged_in = True
            return {
                "success": True, 
                "message": "登录成功",
                "user_info": {
                    "user_id": "test_user", 
                    "user_name": "测试用户",
                    "architecture": platform.machine()
                }
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def get_file_list(self, path: str = "/", cid: str = "0"):
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
                    "icon": "fa-folder" if item.get('is_directory') else self._get_file_icon(item.get('name', '')),
                    "architecture": platform.machine()
                }
                files.append(file_info)
            
            return {
                "success": True,
                "files": files,
                "current_path": path,
                "current_cid": cid,
                "architecture": platform.machine()
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def search_files(self, keyword: str):
        return {
            "success": True,
            "files": [],
            "keyword": keyword,
            "architecture": platform.machine()
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

# 全局115客户端实例
client_115 = Client115()

# Pydantic模型
class LoginRequest(BaseModel):
    cookie: Optional[str] = None

class FileListRequest(BaseModel):
    path: str = "/"
    cid: str = "0"

class SearchRequest(BaseModel):
    keyword: str

# API路由
@app.get("/")
async def root():
    version_info = get_version_info()
    return {
        "message": "115网盘管理工具API", 
        "version": version_info["version"],
        "build_time": version_info["build_time"],
        "architecture": platform.machine()
    }

@app.get("/health")
async def health_check():
    version_info = get_version_info()
    return {
        "status": "healthy", 
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "version": version_info["version"]
    }

@app.get("/api/version")
async def get_version():
    """获取版本信息"""
    return get_version_info()

# 115网盘API
@app.post("/api/115/generate-qr")
async def generate_qr_code():
    """生成115登录二维码"""
    return await client_115.generate_qr_code()

@app.get("/api/115/check-login/{uid}")
async def check_qr_login(uid: str):
    """检查二维码登录状态"""
    return await client_115.check_qr_login(uid)

@app.post("/api/115/login-cookie")
async def login_with_cookie(request: LoginRequest):
    """使用Cookie登录"""
    if not request.cookie:
        raise HTTPException(status_code=400, detail="Cookie不能为空")
    return await client_115.login_with_cookie(request.cookie)

@app.post("/api/115/files")
async def get_file_list(request: FileListRequest):
    """获取文件列表"""
    return await client_115.get_file_list(request.path, request.cid)

@app.post("/api/115/search")
async def search_files(request: SearchRequest):
    """搜索文件"""
    return await client_115.search_files(request.keyword)

@app.get("/api/115/user-info")
async def get_user_info():
    """获取用户信息"""
    return {"success": True, "user_info": {}}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9711)
