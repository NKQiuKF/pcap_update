# Web

## version 0.0 【已弃用】

基于 Flask-appBuilder

运行

```
sudo fabmanager run
python ws_3d.py
```

## version 0.1

基于 superset
## 需要安装的库
```
sudo pip install numpy
sudo pip install pandas
sudo pip install scikit-learn==0.16.1
```shell
## 显示的样例数据
web/views/antimal_db.sqlite
web/views/history.csv
web/views/web_atkinfo.csv

## 注意 history.csv 和 web_atkinfo.csv 以前版本在 server/
只修改了 web中读取数据的路径

## 运行
cd web/
修改 start.sh 中superset的安装路径
修改web/view/lib/sql/connect.py中的`your_db`，设为你的数据库所在的绝对路径
sh start.sh
打开 127.0.0.1:9999 可以看到视图

```
## 结束
`ctrl+C`结束superset<br/>
`sudo ./shutdown.sh`关闭机器学习模型
