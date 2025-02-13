# 使用Python镜像
FROM python:alpine

# 设置工作目录
WORKDIR /app

# 将当前目录中的文件复制到镜像中的/app
COPY . /app

# 安装应用依赖
RUN pip install flask openai

# 暴露端口
EXPOSE 80

# 定义容器启动时执行的命令
CMD ["python", "main.py"]