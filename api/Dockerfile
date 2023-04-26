FROM ubuntu:22.04
ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
WORKDIR /ai-api
USER root

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && cat /etc/apt/sources.list && apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y openssh-server && sed -i "s/.*PermitRootLogin.*/PermitRootLogin yes/" /etc/ssh/sshd_config && mkdir /var/run/sshd
RUN apt-get install -y python3 python3-pip pkg-config
RUN apt-get install -y default-libmysqlclient-dev libcurl4-openssl-dev libssl-dev
RUN python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip

# install
COPY requirements.txt ./
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python3", "main.py", "-p 9090" ]
