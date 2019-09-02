#!/bin/bash

sudo apt-get -y install python-pip schedtool
sudo apt-get -y install libxml2-dev libxslt1-dev
sudo apt-get -y install scapy
sudo apt-get -y install python-pcapy
sudo apt-get -y install zlib1g-dev
sudo apt-get -y install build-essential libssl-dev libffi-dev python-dev python-pip libsasl2-dev libldap2-dev
sudo apt-get -y install pypy
sudo apt-get -y install sqlite3
sudo apt-get -y install libevent-dev
sudo apt-get -y install libmysqld-dev

sudo apt-get -y install libc6-i686:i386 libexpat1:i386 libffi6:i386 libfontconfig1:i386 libfreetype6:i386 libgcc1:i386 libglib2.0-0:i386 libice6:i386 libpcre3:i386 libpng12-0:i386 libsm6:i386 libstdc++6:i386 libuuid1:i386 libx11-6:i386 libxau6:i386 libxcb1:i386 libxdmcp6:i386 libxext6:i386 libxrender1:i386 zlib1g:i386 libx11-xcb1:i386 libdbus-1-3:i386 libxi6:i386 libsm6:i386 libcurl3:i386

sudo pip install -r requirements.txt
#NKAMGFOLDER=$(dirname $(readlink -f "$0"))
#WEBFOLDER=${NKAMGFOLDER}"/web" 
#echo "export PYTHONPATH=${WEBFOLDER}:$PYTHONPATH" >> ~/.bashrc
#echo "安装完毕，重新开启终端后自动载入相关参数"
