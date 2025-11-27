FROM nginx:alpine

# 复制静态文件
COPY index.html /usr/share/nginx/html/
COPY assets/ /usr/share/nginx/html/assets/

# 复制自定义nginx配置（可选）
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 9710

CMD ["nginx", "-g", "daemon off;"]
