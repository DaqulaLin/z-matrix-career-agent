# 使用轻量且高性能的 3.12 镜像
FROM python:3.12-slim

# 设置环境变量
ENV PYTHONUNBUFFERED=True
ENV APP_HOME /app
WORKDIR $APP_HOME

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源码
COPY . .

# --- 关键修改：从 gunicorn 改为 uvicorn ---
# ADK/FastAPI 必须使用 uvicorn 启动
# 使用 sh -c 确保能解析 $PORT 环境变量
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
#CMD ["python", "main.py"]