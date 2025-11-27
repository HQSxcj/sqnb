from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import platform
import uvicorn

from app.client_115 import Client115

app = FastAPI(title="115网盘管理工具", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return {
        "message": "115网盘管理工具API", 
        "version": "1.0.0",
        "architecture": platform.machine()
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "platform": platform.platform(),
        "architecture": platform.machine()
    }

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
