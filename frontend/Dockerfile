FROM nginx:alpine

# 复制前端文件
COPY index.html /usr/share/nginx/html/

# 自定义nginx配置
RUN echo 'server { \
    listen 9710; \
    server_name localhost; \
    \
    location / { \
        root /usr/share/nginx/html; \
        index index.html; \
        try_files \$uri \$uri/ /index.html; \
    } \
    \
    location /api/ { \
        proxy_pass http://backend:9711; \
        proxy_set_header Host \$host; \
        proxy_set_header X-Real-IP \$remote_addr; \
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for; \
        proxy_set_header X-Forwarded-Proto \$scheme; \
    } \
    \
    location /health { \
        proxy_pass http://backend:9711; \
    } \
    \
    location /docs { \
        proxy_pass http://backend:9711; \
    } \
    \
    location /openapi.json { \
        proxy_pass http://backend:9711; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 9710

CMD ["nginx", "-g", "daemon off;"]
