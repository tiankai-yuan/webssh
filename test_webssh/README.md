# 操作手册

## 不用docker启动
### 第一步：

* pip install -r requirements.txt

### 第二步：

* 新建一个mysql库，叫test_webssh
* python manage.py makemigrations
* python manage.py migrate

## 用docker启动
* 进入到项目的根目录下，执行```docker-compose up -d```
* （用pycharm启动的: 配置好docker解释器，Host写0.0.0.0，端口号写8002）

### 文档说明：
* 加了crontab,用于删除过期无用的文件
* 加了命令记录，用于日后审计工作
### 接口：
* / : index
* /show/ : 操作记录的展示
    * 参数1（必写）: terminal_id (uuid(str))
    * 参数2 （和参数3一致，可写可不写）: start_time  (timestamp(str))
    * 参数3 （和参数2一致，可写可不写）: end_time  (timestamp(str))


**再次特别感谢原文作者**
[原文的源代码](git@github.com:huyuan1999/django-webssh.git)


**以及特别感谢作者**
[博客地址](https://www.cnblogs.com/arrow-kejin/p/11439721.html)

+ 遗留问题：
    源代码的在webssh页面，与后台交互时，按ctrl+R搜索历史命令时，
    直接回车会抛异常，导致websocket长链接直接断开，有待进一步完善。
    
### 欢迎大家访问我的博客地址：
* www.haiguixiansheng.org.cn
* www.cnblogs.com/haiguixiansheng
