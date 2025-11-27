# ------------------------------
# Stage 1: Build dependencies
# ------------------------------
FROM python:3.11-slim AS builder

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装依赖到 /app/.venv（虚拟环境）
RUN python -m venv .venv \
    && .venv/bin/pip install --upgrade pip \
    && .venv/bin/pip install --no-cache-dir -r requirements.txt

# ------------------------------
# Stage 2: Final image
# ------------------------------
FROM python:3.11-slim

WORKDIR /app

# 复制虚拟环境
COPY --from=builder /app/.venv /app/.venv

# 设置 PATH
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 复制项目文件
COPY . .

# 暴露端口（FastAPI/Flask 默认 8000）
EXPOSE 8000

# 默认启动命令（使用 Uvicorn）
# 如果是 Flask，把 app:app 改成你 Flask 对应的 app 名称
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
