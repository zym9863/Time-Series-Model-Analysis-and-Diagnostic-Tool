# 使用Python 3.12的官方镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY app.py ./
COPY README.md ./

# 安装uv包管理器
RUN pip install uv

# 使用uv安装依赖
RUN uv sync --frozen

# 暴露端口
EXPOSE 8000

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# 启动命令
CMD ["uv", "run", "python", "app.py", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
