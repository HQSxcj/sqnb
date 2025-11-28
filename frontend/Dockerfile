FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# 复制后端依赖文件
COPY backend/requirements.txt .

# 安装Python依赖
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY backend/app ./app
COPY version.json .

# 复制前端文件
COPY frontend/index.html /var/www/html/

# 配置Nginx
RUN echo 'server { \
    listen 9710; \
    server_name localhost; \
    \
    location / { \
        root /var/www/html; \
        index index.html; \
        try_files \$uri \$uri/ /index.html; \
    } \
    \
    location /api/ { \
        proxy_pass http://localhost:9711; \
        proxy_set_header Host \$host; \
        proxy_set_header X-Real-IP \$remote_addr; \
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for; \
    } \
    \
    location /health { \
        proxy_pass http://localhost:9711; \
    } \
    \
    location /docs { \
        proxy_pass http://localhost:9711; \
    } \
}' > /etc/nginx/sites-available/default && \
    ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# 暴露端口
EXPOSE 9710

# 启动命令 - 同时启动后端和Nginx
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port 9711 & nginx -g 'daemon off;'"
