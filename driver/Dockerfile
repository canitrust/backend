FROM ubuntu:18.04

# Customize sources for apt-get
RUN  echo "deb http://archive.ubuntu.com/ubuntu bionic main universe\n" > /etc/apt/sources.list \
  && echo "deb http://archive.ubuntu.com/ubuntu bionic-updates main universe\n" >> /etc/apt/sources.list \
  && echo "deb http://security.ubuntu.com/ubuntu bionic-security main universe\n" >> /etc/apt/sources.list

RUN apt-get -y update \
  && apt-get install -y --no-install-recommends firefox firefox-geckodriver python3-pip python3-minimal python3-setuptools \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/* 

ADD requirements.txt ./

RUN ln -s /usr/bin/python3 /usr/local/bin/python && pip3 install --upgrade pip

RUN pip3 install -r ./requirements.txt