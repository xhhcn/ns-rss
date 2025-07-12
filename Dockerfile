# 使用官方 Python 运行时作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY main.py .

# 创建数据目录用于存储历史记录
RUN mkdir -p /app/data

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 暴露端口（虽然这个应用不需要，但保持一致性）
EXPOSE 8080

# 启动应用
CMD ["python", "main.py"] 