DJANGO QUICKSTART
==============

在 Django 1.4 的基础上快速建立项目文件，当然是最基本的，不过这要比 django-admin.py 的 startproject 指令更好用。

使用方法：

    $ python django-quickstart.py mydj
    Finish!
    Press any key to exit...
    $
    
即在当前目录完成创建了一个名为mydj的最基本的django项目。



目录结构如下：

    mydj
    --__init__.py
    --models.py
    --settings.py
    --urls.py
    --views.py
    --wsgi.py
    templates
    --index.html
    static
    --css
    --images
    --js
    manage.py
    run.py
    
mydj 为py代码主文件夹，其中 models.py 编写数据模型；setting.py 为项目设置；urls.py 配置url跳转路由；views.py 编写逻辑控制代码，里面预置了网站的首页实现方法 /index/；msgi.py 用户项目的wsgi部署。
templates 为页面模块文件，里面预置了一个index.html模版。

static 为静态文件目录，包含有css、images、js 三个子目录，用户存放项目的静态文件。

manage.py 为django自带的管理工具脚本。

run.py 是由 manage.py 修改的，运行 run.py 可实现用django测试服务器直接在8000端口部署项目并打开首页。这对于要将项目编译为exe的用户来说有一定的帮助。


-----------------------

