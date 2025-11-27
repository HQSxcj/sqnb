FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# 先复制requirements.txt
COPY requirements.txt .

# 直接使用pip安装，不要用virtualenv
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p /app/logs

EXPOSE 9711

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9711"]
