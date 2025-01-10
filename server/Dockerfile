# 使用 Ubuntu 22.04 作为基础镜像
FROM ubuntu:22.04

# 设置环境变量，避免交互式安装时的提示
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHON_VERSION=3.10.12

# 使用国内的 apt 源
RUN sed -i 's|archive.ubuntu.com|mirrors.aliyun.com|g' /etc/apt/sources.list && \
    sed -i 's|security.ubuntu.com|mirrors.aliyun.com|g' /etc/apt/sources.list

# 更新包列表并安装构建依赖和 Playwright 所需的依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    zlib1g-dev \
    libffi-dev \
    libssl-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    ca-certificates \
    git \
    libnss3 \
    libxss1 \
    libasound2 \
    libx11-xcb1 \
    libcups2 \
    libdbus-1-3 \
    libxcomposite1 \
    libxrandr2 \
    libpangocairo-1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 && \
    update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 下载并编译 Python 源码
RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar -xzf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall && \
    cd .. && \
    rm -rf Python-${PYTHON_VERSION} Python-${PYTHON_VERSION}.tgz

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . /app

# 使用国内 pip 源安装项目依赖和 Playwright
RUN python3.10 -m pip install --upgrade pip && \
    python3.10 -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    python3.10 -m pip install --no-cache-dir -r requirements.txt && \
    python3.10 -m pip install playwright && \
    playwright install --with-deps

# 默认命令
CMD ["python3.10"]