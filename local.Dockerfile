FROM ubuntu:16.04

# install testdriver
RUN apt-get -y update \
  && apt-get -y upgrade \
  && apt-get -y install flex bison gcc make automake firefox jq curl wget dnsutils python3-pip python3-dev
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz -O /tmp/geckodriver.tar.gz && tar -C /opt -xzf /tmp/geckodriver.tar.gz && chmod 755 /opt/geckodriver && ln -fs /opt/geckodriver /usr/bin/geckodriver && ln -fs /opt/geckodriver /usr/local/bin/geckodriver

#setup python3
RUN cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# install requirements
ADD requirements.txt ./
RUN pip3 install -r ./requirements.txt

COPY startup.sh .