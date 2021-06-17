# 榛果

## 简介

1921 软件工程基础课程的大作业（后端部分）。

一个校园二手商品交易平台，支持用户上传商品与需求，且支持用户之间进行交易。

网站首页：

![image-20210617151040456](https://raw.githubusercontent.com/zhtjtcz/MyImg/master/img/20210617151040.png)



## 运行环境

Python 3.8 及以上

Django 3.2 及以上

依赖第三方库`django-cors-headers`，安装方法：

```shell
pip install django-cors-headers
```



## 项目说明

git clone 到本地后，使用`python manage.py runserver`并不能运行该项目。这是因为一些关键性的信息（如数据库地址，密码等）存在了本地的一个 Yaml 文件中，并没有上传到该仓库。具体可以参见`zhenguo/settings.py`中的Yaml读取语句。

如果想连接自己的数据库运行，则需要在本地的项目根目录下，创建`config.yaml`文件，并按以下格式编写：

```yaml
dbname: 数据库名称
dbhost: 数据库地址
dbuser: 账户
dbpassword: 密码
emailuser: 163邮箱
emailpassword: 163邮箱授权码
```

如果 Yaml 编写无误，直接使用`python manage.py runserver`即可运行本项目。不过由于大作业要求前后端分离开发，所以运行后看不到任何页面，仅仅可以使用 Postman 测试。

本项目并不完美，仅供 2021 及之后的同学学习 Django 参考使用。如有问题可以访问我的博客主页：[Marvolo's Blog](marvolo.top)，那上面会有一篇介绍后端学习路线以及我自己经验的文章，可以到评论区留言交流。

*公开此项目希望可以为 2021 及之后的同学学习软件工程提供一些微薄之力。*
