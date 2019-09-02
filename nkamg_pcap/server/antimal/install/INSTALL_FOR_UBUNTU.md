# Installation of AntiBot System

## Set Up Bro

### Install libraries 
    sudo apt-get install libpcap-dev openssl libssl-dev bind9 cmake make swig bison flex g++ gcc gawk curl sendmail libgeoip-dev zlib1g-dev libmagic-dev python-dev libcaf-dev
    sudo apt-get install --reinstall zlibc zlib1g zlib1g-dev

### Install GeoIPLite Database
    wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
    wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCityv6-beta/GeoLiteCityv6.dat.gz
    gunzip GeoLiteCity.dat.gz
    gunzip GeoLiteCityv6.dat.gz
    sudo mv GeoLiteCity.dat  /usr/share/GeoIP/GeoLiteCity.dat
    sudo mv GeoLiteCityv6.dat /usr/share/GeoIP/GeoLiteCityv6.dat
    sudo ln -s /usr/share/GeoIP/GeoLiteCity.dat /usr/share/GeoIP/GeoIPCity.dat
    sudo ln -s /usr/share/GeoIP/GeoLiteCityv6.dat /usr/share/GeoIP/GeoIPCityv6.dat
### Installing Bro
    mkdir /tmp/bro
    cd /tmp/bro
    git clone --recursive git://git.bro.org/bro
    cd bro
    ./configure **the default installation path is /usr/local/bro.**
    make
    sudo make install

### Configuring Bro
  - export PATH=/usr/local/bro/bin:$PATH. You can also add
    PATH=/usr/local/bro/bin:$PATH to the ~/.profile file.
  - $PREFIX/etc/node.cfg -> Configure the network interface to monitor
  - $PREFIX/etc/networks.cfg-> Configure the local networks
  - $PREFIX/etc/broctl.cfg -> Change the MailTo address and the log rotation.
### Starting Bro
    sudo broctl
    [BroControl] > install
    [BroControl] > start
    [BroControl] > status



## Install Linux Libraries
    sudo apt-get install libjudy-dev libpcap0.8-dev htop

## Install Python Libraries:
    sudo apt-get install python-numpy python-scipy python-pandas python-matplotlib ipython python-networkx python-six python-patsy python-statsmodels python-statsmodels-lib python-dateutil python-pip python-setuptools python-ipy python-rpy2 python-mysqldb python-sqlalchemy python-flask python-progressbar ipython-notebook
### pip install
    pip install brewer2mpl tabulate
    pip install -U scikit-learn
<!---
### Install sklearn
    mkdir /tmp/scikit
    cd /tmp/scikit
    git clone https://github.com/joker0x5F5F/scikit-learn
    cd scikit-learn
    git checkout tsne-kldivergence
    python setup.py install 
-->

## Set up R 
    sudo add-apt-repository ppa:marutter/rrutter 
    sudo apt-get update 
    sudo apt-get install r-base r-base-dev 
    sudo apt-get install python rpy2

### Install CLUES
    cd /tmp
    wget http://cran.r-project.org/src/contrib/clues_0.5-4.tar.gz
    tar -xzvf clues_0.5-4.tar.gz
    vim clues/src/dmedian.f95
    change the text 
    ========================================
    ! check the input arguments for errors
    if((n < 1) .or. (n > iupper)) then
        !write(ipr, fm17) "***** fatal error--the second input argument to & 
        !    & the median subroutine is outside the allowable ", iupper,  &
        !    & " interval *****"
        !write(ipr, fm47) "***** the value of the argument is ", n, " *****"
        call dblepr("**** fatal error--the second input argument to & 
            & the median subroutine is outside the allowable &
            &  interval *****", -1, 0, 0)
        !write(ipr, fm47) "***** the value of the argument is ", n, " *****"
        call intpr("***** the value of the argument is ", -1, n, 6)
        return
    elseif(n > 1) then
    =======================================
    to 
    =======================================
    ! check the input arguments for errors
    !if((n < 1) .or. (n > iupper)) then
        !write(ipr, fm17) "***** fatal error--the second input argument to & 
        !    & the median subroutine is outside the allowable ", iupper,  &
        !    & " interval *****"
        !write(ipr, fm47) "***** the value of the argument is ", n, " *****"
    !   call dblepr("**** fatal error--the second input argument to & 
    !        & the median subroutine is outside the allowable &
    !        &  interval *****", -1, 0, 0)
        !write(ipr, fm47) "***** the value of the argument is ", n, " *****"
    !    call intpr("***** the value of the argument is ", -1, n, 6)
    !    return
    !else
    if(n > 1) then
    =======================================
    
    tar the modified code to a .tar.gz file and install tar.gz from R using
install.package("/tmp/....tar.gz", repos = NULL, type="source")

<!---
## Set Up MySQL

### Install MySQL
    sudo apt-get install mysql-server

### Login to MySQL: 
    mysql -u root -p

### Create the project database
    create database botnet_project

### Create a user
    create user 'wz'@'localhost'; set password for 'wz'@'localhost'=password('botnet')

### Use database: 
    use botnet_project

### Grant privileges to user wz: 
    grant all on botnet_project.* to 'wz'@'localhost';
-->

## Install Maltrail
    sudo apt-get install python-pcapy
    sudo pip install pygeoip
    sudo apt-get install schedtool

## Server configure
    sudo apt-get install python-flask
    sudo pip install flask-socketio
## Server MYSQL
    sudo apt-get install mysql-server
    sudo apt-get install mysql-client
    sudo apt-get install libmysqlclient15-dev
    sudo apt-get install python-mysqldb
    wget http://peak.telecommunity.com/dist/ez_setup.py
    sudo python ez_setup.py -U setuptools
    sudo easy_install MYSQL-Python
    sudo easy_install SQLAlchemy
