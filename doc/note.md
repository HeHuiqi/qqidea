创建虚拟环境
pythom -m venv qqidea-env
cd qqidea-env
激活虚拟环境
source bin/activate


pip install Django

创建Django项目
django-admin startproject qqidea

cd qqidea

创建Django App
./manage.py startapp blog 
./manage.py startapp config 
./manage.py startapp comment 


./manage.py makemigrations
./manage.py migrate



退出虚拟环境
deactivate
