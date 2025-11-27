# SQNB - 115网盘智能整理工具

SQNB 是一个专为 **115 网盘** 纯线上整理工具

## 🎯 功能简介

### 🔐 智能登录
- 扫码登录 115 网盘  
- 支持 Cookie 登录  
- 自动保持登录状态  

### 📂 文件管理
- 可视化文件浏览器  
- 图标 / 列表 / 详情 三种视图模式  
- 支持快速搜索与筛选  
- 文件自动分类显示  

### ⚙️ 智能整理
- 自定义重命名规则  
- 自动文件分类  
- 智能识别电影、电视剧  
- 支持 TMDB 元数据匹配  

### 📊 任务管理
- 实时任务进度  
- 详细运行日志  
- 任务历史记录  

### 🎨 用户体验
- 现代化暗色界面  
- 多主题切换  
- 响应式设计（适配手机）  

## 🚀 快速开始

### 方式一：Docker Run（简单快捷）

```bash
docker run -d \
  -p 9710:9710 \
  -p 9711:9711 \
  --name sqnb \
  yongzz668/sqnb:latest
```
### 方式二:Docker Compose
```version: '3.8'
services:
  sqnb:
    image: yongzz668/sqnb:latest
    container_name: sqnb
    ports:
      - "9710:9710"
      - "9711:9711"
    restart: unless-stopped
```

# http://localhost:9710
