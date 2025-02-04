# 使用官方的 Python 基础镜像
FROM python:3.8-alpine

# 设置工作目录
WORKDIR /app

# 将当前目录中的文件复制到镜像中的 /app 目录
COPY . /app

# 安装应用依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 80

# 定义容器启动时执行的命令
CMD ["python", "main.py"]