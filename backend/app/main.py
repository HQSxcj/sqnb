from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
from typing import Dict, List, Optional
import uvicorn
import os

from app.client_115 import Client115  # 注意：文件名不能以数字开头

app = FastAPI(title="115网盘管理工具", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9710", "http://127.0.0.1:9710", "*"],
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

class CreateFolderRequest(BaseModel):
    parent_cid: str
    folder_name: str

# API路由
@app.get("/")
async def root():
    return {"message": "115网盘管理工具API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

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

@app.post("/api/115/create-folder")
async def create_folder(request: CreateFolderRequest):
    """创建文件夹"""
    return await client_115.create_folder(request.parent_cid, request.folder_name)

@app.get("/api/115/user-info")
async def get_user_info():
    """获取用户信息"""
    return {"success": True, "user_info": {}}

# 文件整理相关API
@app.post("/api/organize/start")
async def start_organize():
    """开始文件整理"""
    return {"success": True, "message": "整理任务已开始"}

@app.get("/api/organize/status")
async def get_organize_status():
    """获取整理状态"""
    return {"status": "idle", "progress": 0}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9711)
