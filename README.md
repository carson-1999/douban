# 项目内容简介

爬取豆瓣网站`https://book.douban.com/top250`上面的Top250数据,然后将数据保存到Mysql数据库中,最后这些数据记录以Web的方式进行展示,并实现对这些数据记录的CRUD(增删改查)!

# 项目实现简介

1. **对豆瓣网站的爬虫的实现。**

   见项目中的`爬取豆瓣Top250脚本(beautifulSoup).py`文件即可。

   > 这个Python脚本的主要功能是爬取豆瓣图书Top250的信息并将其保存到MySQL数据库中。具体实现过程如下：
   >
   > 1. 引入需要的库：requests库用于发送http请求，BeautifulSoup库用于解析html页面，pymysql库用于将数据保存到MySQL数据库中，threading库用于实现多线程。
   > 2. 定义get_detail_urls()函数，用于获取每本书的详情页面的url链接。
   > 3. 定义parse_detail_url()函数，用于解析每本书的详情页面并将其保存到MySQL数据库中。
   > 4. 定义main()函数，用于爬取多页页面的内容，并利用多线程来解析数据。
   > 5. 在main()函数中，首先定义需要爬取的页面链接，然后遍历每个页面链接，获取每个页面中每本书的详情页面链接，再利用多线程来解析每本书的详情页面并将其保存到MySQL数据库中。
   > 6. 最后，在程序的末尾，创建多个线程来执行main()函数，以提高爬取速度。
   >
   > 总体来说，这段代码实现了一个简单的爬虫，并将爬取到的数据保存到了MySQL数据库中。

2. **数据的WEB展示及数据的CRUD的实现。**

   见项目中的`web program(by flask)文件夹`即可。

   > 这个文件夹是一个基于 Flask 和 MySQL 数据库的 Web 应用程序，用于展示和管理书籍信息。它实现了以下功能：
   >
   > - 在首页展示所有书籍的信息，并支持数据的分页查询和展示。
   > - 提供查询功能，根据书名和作者名查询书籍信息。
   > - 提供添加、修改和删除书籍信息的功能。
   >
   > 具体过程如下：
   >
   > 1. 导入所需的 Python 库和模块，包括 Flask、flask_paginate、pymysql 等。
   > 2. 初始化 Flask 应用程序和 MySQL 数据库连接。
   > 3. 定义首页路由函数 index()，根据请求方法（GET 或 POST）查询书籍信息并进行分页处理，最后将结果传递给 HTML 模板进行渲染。
   > 4. 定义添加书籍信息的路由函数 addBook()，返回一个包含表单的 HTML 模板。
   > 5. 定义修改书籍信息的路由函数 changeBook()，根据书籍 ID 查询数据库中对应的书籍信息，并将结果传递给 HTML 模板进行渲染。
   > 6. 定义更新书籍信息的路由函数 updateBook()，根据请求参数更新数据库中对应的书籍信息，并将结果重定向到首页。
   > 7. 定义插入书籍信息的路由函数 insertBook()，根据表单参数插入新的书籍信息到数据库中，并将结果重定向到首页。
   > 8. 定义删除书籍信息的路由函数 deleteBook()，根据书籍 ID 删除数据库中对应的书籍信息，并将结果重定向到首页。
   > 9. 启动 Flask 应用程序并监听请求，最后关闭游标对象和数据库连接。

# 项目的环境

1. 项目需要的`软件环境`如下:

> - 安装Python环境并配置环境变量。
>
> - 安装Mysql数据库环境并配置环境变量。
> - navicat软件,用于连接mysql数据库。

2. 项目用到的`Python第三方库`如下:

   [可用`pip`包管理工具进行安装]

> - requests
> - bs4
> - pymysql
> - threading
> - flask
> - flask_paginate

3. 项目可能需要的技术背景:

   > python + 爬虫 + flask + html + css + js + linux + json + mysql等。

# 使用指南

以下步骤基于`Windows系统`环境:

1. 准备并安装好项目所需的环境。

2. `Clone`本项目的所有内容到本地。

3. 打开`navicat`软件,连接本地的mysql数据库,在其中先建立好一个名叫`mydb`数据库,再打开`sql files文件夹`,运行其中的`1.create_douban_table.sql`文件,从而在`mydb数据库`中建立名叫`douban`的数据表。

4. 打开`crawler script文件夹`,运行其中的 `爬取豆瓣Top250脚本(beautifulSoup).py`爬虫程序,即可将豆瓣TOP250的书籍数据保存到本地mysql的mydb数据库的douban数据表中。

   > 【**备注**:如果此爬虫在运行过程中出现被封ip等情况,导致不能顺利爬取数据。此时也可以直接打开`sql files文件及`，利用`navicat软件`运行其中的`2.create_douban_data(2023-06-23爬取).sql`文件,从而直接将我爬取的数据直接存储入`douban`数据表中,从而方便后续的步骤实现】

5. 打开`web program(by flask)文件夹`，运行其中的`server.py`服务器程序,即可启动相应的`WEB可视化CRUD`数据处理程序。

6. 最后利用浏览器打开本地网址,即`127.0.0.1：5000`即可。

# 示例和演示

## 静态展示

本项目的部分效果图如下:

---

1. `爬取的数据(2023-06-23日爬取):`

![爬取的数据(2023-06-23日爬取)](https://github.com/carson-1999/douban/assets/68895188/9216cfd0-04cc-4f0a-a316-7ed22f8f74bf)


2. `前端效果:`

  ![前端效果](https://github.com/carson-1999/douban/assets/68895188/3a3d0bea-166d-4fc2-a0e1-9f2294bc4a13)


3. `数据查找效果:`

  ![数据查找效果](https://github.com/carson-1999/douban/assets/68895188/4ce28c9b-0448-409e-82dd-300521aa5c19)


4. `数据分页效果:`

   ![数据分页效果](https://github.com/carson-1999/douban/assets/68895188/ec0e7442-0ca1-42c8-a1fe-f334a9156b26)


5. `数据删除效果:`

![数据删除效果](https://github.com/carson-1999/douban/assets/68895188/1f8e7690-fb42-4241-bb40-75ab17f591f6)


6. `数据添加效果:`

![数据添加效果](https://github.com/carson-1999/douban/assets/68895188/b2886ca3-78c1-4b81-8d1d-d4856c420672)


7. `数据修改效果:`

![数据修改效果](https://github.com/carson-1999/douban/assets/68895188/21e2ab80-9442-4611-bf5e-2f7a9871710f)


---

## 动态展示

访问链接:http://159.75.153.14:5000/ 即可。

---
