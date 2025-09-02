FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件到工作目录
COPY . /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用端口
EXPOSE 8000

# 运行应用
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

