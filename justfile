upload:
    rsync -rvhP api ff@build-server:~/

build:
    cd api
    docker build -t ai-api .

init:
    sudo apt-get install -y python3 python3-pip pkg-config
    sudo apt install libcurl4-openssl-dev libssl-dev
    sudo apt-get install libmysqlclient-dev
    python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple requests
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple flask
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple flask-cors
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pyOpenSSL
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple Flask-SSLify
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple gevent
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple redis
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple bs4
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple ephem
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple timezonefinder pytz
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple mysqlclient
    pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pycurl
    sudo apt install redis
