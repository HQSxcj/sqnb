FROM --platform=$TARGETPLATFORM python:3.11-slim

WORKDIR /app

# 使用兼容的包管理器
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# 复制后端依赖文件
COPY backend/requirements.txt .

# 安装Python依赖
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY backend/app ./app

# 复制前端文件到Nginx目录
COPY frontend/index.html /var/www/html/

# 配置Nginx - 使用兼容的配置
RUN echo 'server { \n\
    listen 9710; \n\
    server_name localhost; \n\
    \n\
    location / { \n\
        root /var/www/html; \n\
        index index.html; \n\
        try_files \$uri \$uri/ /index.html; \n\
    } \n\
    \n\
    location /api/ { \n\
        proxy_pass http://localhost:9711; \n\
        proxy_set_header Host \$host; \n\
        proxy_set_header X-Real-IP \$remote_addr; \n\
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for; \n\
    } \n\
    \n\
    location /docs { \n\
        proxy_pass http://localhost:9711; \n\
    } \n\
    \n\
    location /openapi.json { \n\
        proxy_pass http://localhost:9711; \n\
    } \n\
}' > /etc/nginx/sites-available/default && \
    ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# 暴露端口
EXPOSE 9710 9711

# 启动命令 - 兼容不同架构
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port 9711 & nginx -g 'daemon off;'"
