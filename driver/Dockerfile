FROM ubuntu:16.04

# install testdriver
RUN apt-get -y update \
  && apt-get -y install flex bison gcc make automake firefox python3-pip python3-dev

RUN apt-get install firefox-geckodriver
#setup python3
RUN cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# install requirements
ADD requirements.txt ./
RUN pip3 install -r ./requirements.txt