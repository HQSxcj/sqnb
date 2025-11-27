FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 升级pip和setuptools
RUN pip install --upgrade pip setuptools wheel

# 先安装基础依赖
COPY requirements-base.txt .

RUN pip install --no-cache-dir -r requirements-base.txt

# 单独安装 p115client
RUN pip install --no-cache-dir "p115client @ git+https://github.com/ChenyangGao/p115client.git"

# 验证安装
RUN python -c "import p115client; print(f'p115client version: {p115client.__version__}')"

# 复制应用代码
COPY . .

EXPOSE 9711

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9711"]
