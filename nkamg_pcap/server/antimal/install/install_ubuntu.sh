#!/bin/bash
## Geoip server
    sudo apt-get install python-pip schedtool
    sudo pip install geoip2
## Server configure
    sudo apt-get install python-flask
    sudo pip install flask-socketio
    sudo apt-get install python-psutil
    sudo apt-get install python-flask-sqlalchemy
    sudo apt-get install python-gevent
## Server MYSQL
    sudo apt-get install mysql-server
    sudo apt-get install mysql-client
    sudo apt-get install libmysqlclient15-dev
    sudo apt-get install python-mysqldb
    wget http://peak.telecommunity.com/dist/ez_setup.py
    sudo python ez_setup.py -U setuptools
    sudo easy_install MYSQL-Python
    sudo easy_install SQLAlchemy
