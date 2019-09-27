# 操作手册

### 第一步：

* pip install -r requirements.txt

### 第二步：

* 新建一个mysql库，叫test_webssh
* python manage.py makemigrations
* python manage.py migrate


### 文档说明：
* 加了crontab
* 加了日志记录
### 接口：
* "" : index
* 



**再次特别感谢原文作者**
[原文的源代码](git@github.com:huyuan1999/django-webssh.git)


**以及特别感谢作者**
[博客地址](https://www.cnblogs.com/arrow-kejin/p/11439721.html)

+ 遗留问题：
    源代码的在webssh页面，与后台交互时，按ctrl+R搜索历史命令时，
    直接回车会抛异常，导致websocket长链接直接断开，有待进一步完善。
    