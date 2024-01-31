#              蓝山运维考核-readme

### 1.实现的基本功能

用户登录/用户验证/简单的ui

监控主机功能/docker功能 

下载lamp

数据库目前做了登陆用

### 2.技术使用

Flask==1.1.2
jinja2==2.11.3
markupsafe==1.1.1
werkzeug==1.0.1
itsdangerous==2.0.1
flask_login==0.6.2
psutil==5.9.8
Pillow==8.4.0
PyMySQL==1.0.3
cryptography==3.4.8

具体使用如下：

##### ***<u>Flask：python的轻量框架</u>***

**实例构建**：

![image-20240129200911876](C:\Users\12695\AppData\Roaming\Typora\typora-user-images\image-20240129200911876.png)

导入一些必要的参数，模板

**路由定义**：确定应用程序如何响应特定 URL 

![image-20240129201355267](C:\Users\12695\AppData\Roaming\Typora\typora-user-images\image-20240129201355267.png)

定义了验证码路由

![image-20240129201439032](C:\Users\12695\AppData\Roaming\Typora\typora-user-images\image-20240129201439032.png)

定义的根目录路由

![image-20240129201530209](C:\Users\12695\AppData\Roaming\Typora\typora-user-images\image-20240129201530209.png)

定义了登陆后验证的路由

**处理请求**

![image-20240129203517010](C:\Users\12695\AppData\Roaming\Typora\typora-user-images\image-20240129203517010.png)

**运行**

![image-20240129203605717](C:\Users\12695\AppData\Roaming\Typora\typora-user-images\image-20240129203605717.png)

**flask-login的应用**

![image-20240129203753206](C:\Users\12695\AppData\Roaming\Typora\typora-user-images\image-20240129203753206.png)

创建user定义（承袭usermixin）

![image-20240129203924702](C:\Users\12695\AppData\Roaming\Typora\typora-user-images\image-20240129203924702.png)

定义一个永华加载函数，用user_id为作为参数，返回User（user_id）处理过的结果

![image-20240129205014037](C:\Users\12695\AppData\Roaming\Typora\typora-user-images\image-20240129205014037.png)

追踪用户状态

![image-20240129205047505](C:\Users\12695\AppData\Roaming\Typora\typora-user-images\image-20240129205047505.png)

只有在登陆状态才可以访问





### ***<u>jinja2</u>***：模板引擎，用于渲染html

![image-20240129205353856](C:\Users\12695\AppData\Roaming\Typora\typora-user-images\image-20240129205353856.png)

### <u>***MarkupSafe***</u> ：防止用户提供的数据中有恶意代码或者脚本

### ***<u>Werkzeug</u>*** 是一个 WSGI 工具库，被设计用于构建 Web 框架。它是 Flask 的底层库之一，提供了一些用于处理 HTTP 请求和响应的核心功能。路由系统+响应对象+文件上传+url构建

### ***<u>itsdangerous</u>*** ：lask 的一个独立模块，用于在 Python 应用中处理安全性相关的事务，例如生成和验证加密签名、生成 token 等。其主要目的是为了处理用户身份验证、cookie 签名、防止 CSRF 攻击等方面的需求。//不知道是啥，估计是一个依赖包

### ***<u>psutil</u>*** ：是一个用于检索系统信息以及管理进程和系统资源利用率的 Python 库。它提供了一组跨平台的功能，允许你在不同操作系统上获取有关 CPU、内存、磁盘、网络等方面的信息，同时还可以获取和管理运行中的进程信息。
