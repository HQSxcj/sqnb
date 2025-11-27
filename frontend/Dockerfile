FROM nginx:alpine

# 复制静态文件
COPY index.html /usr/share/nginx/html/

# 自定义nginx配置
RUN echo 'server { \
    listen 9710; \
    server_name localhost; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html; \
        try_files \$uri \$uri/ /index.html; \
    } \
    location /api/ { \
        proxy_pass http://backend:9711; \
        proxy_set_header Host \$host; \
        proxy_set_header X-Real-IP \$remote_addr; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 9710

CMD ["nginx", "-g", "daemon off;"]
