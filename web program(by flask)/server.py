import flask  # 后端框架
from flask_paginate import Pagination, get_page_parameter  # 分页
from flask import url_for  # 进行网页跳转

import pymysql  # 连接数据库

# 初始化
app = flask.Flask(__name__)
# 初始化数据库连接
# 使用pymysql.connect方法连接本地mysql数据库
db = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                     password='root', database='mydb', charset='utf8')
# 操作数据库，获取db下的cursor对象
cursor = db.cursor()


"""首页的书籍数据显示(分页,每页显示10条书籍数据)"""


@app.route('/', methods=['GET', "POST"])
def index():
    # 分页
    page = flask.request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10  # 每页显示的书籍条数
    offset = (page - 1) * per_page  # 偏移量
    # 普通浏览器访问链接(GET请求)
    if flask.request.method == 'GET':
        sql_list = "select * from douban LIMIT %s OFFSET %s"
        cursor.execute(sql_list, (per_page, offset))
        results = cursor.fetchall()
        # 此时总的记录条数
        sql = "select COUNT(*) from douban"
        cursor.execute(sql)
        count = cursor.fetchone()[0]
    # 提交表查查询特定书籍书籍时(Post请求)
    if flask.request.method == 'POST':
        # 获取输入的查询信息查找特定数据
        name = flask.request.values.get("name", "")
        author = flask.request.values.get("author", "")
        sql_list = "SELECT * FROM douban WHERE name LIKE %s AND author LIKE %s LIMIT %s OFFSET %s"
        cursor.execute(sql_list, ('%' + name + '%', '%' +
                       author + '%', per_page, offset))
        results = cursor.fetchall()
        # 此时总的记录条数
        sql = "select COUNT(*) from douban WHERE name LIKE %s AND author LIKE %s"
        cursor.execute(sql,  ('%' + name + '%', '%' + author + '%'))
        count = cursor.fetchone()[0]
    pagination = Pagination(page=page, per_page=per_page,
                            total=count, css_framework='bootstrap4')
    return flask.render_template('show.html', results=results, pagination=pagination)


"""跳转到插入书籍信息的页面"""


@app.route('/addBook', methods=['GET', "POST"])
def addBook():
    return flask.render_template('add.html')


"""跳转到相应书籍信息的修改页面,并回显相应书本的信息,方便确认和后续修改"""


@app.route('/changeBook', methods=['GET', "POST"])
def changeBook():
    # 读取对应书本的id
    id = flask.request.values.get('id', "")
    # 根据id从数据表中获取对应的书本信息,再将结果传递给修改页面进行显示
    results = ""  # 初始化此变量
    try:
        sql = "select * from douban where id = %s;"
        cursor.execute(sql, (id))
        results = cursor.fetchone()
        # 成功获取到相应的数据
        if results:
            return flask.render_template('update.html', results=results)
    except Exception as e:
        print("获取相应的修改信息页面出现错误:" + e)
        # 跳转到错误页面
        return flask.render_template('error.html')
    # 如果前面都没有跳转,那么还是停留在当前的修改页面
    return flask.render_template('update.html', results=results)


"""修改特定的书籍信息并更新到数据表中"""


@app.route('/updateBook', methods=['GET', "POST"])
def updateBook():
    # 获取修改页面的前端参数
    id = flask.request.values.get('id', "")
    name = flask.request.values.get('name', "")
    author = flask.request.values.get('author', "")
    publisher = flask.request.values.get('publisher', "")
    publish_year = flask.request.values.get('publish_year', "")
    pages = flask.request.values.get('pages', "")
    price = flask.request.values.get('price', "")
    binding = flask.request.values.get('binding', "")
    series = flask.request.values.get('series', "")
    ISBN = flask.request.values.get('ISBN', "")
    # 更新数据记录到数据表中
    try:
        sql = "update douban set name = %s,author = %s,publisher = %s,publish_year = %s,pages = %s,price = %s,binding = %s,series = %s,ISBN = %s where id = %s;"
        cursor.execute(sql, (name, author, publisher, publish_year,
                       pages, price, binding, series, ISBN, id))
        db.commit()
        print("成功更新了id为"+str(id)+"的书本数据记录!")
        # 更改成功,跳转回主目录
        flask.redirect(url_for('index'))
    except Exception as e:
        print("更新数据记录出现错误:" + e)
        # 跳转到错误页面
        return flask.render_template('error.html')
    # 如果前面都没有跳转,则还是跳转回主目录
    return flask.redirect(url_for('index'))


"""具体实现插入新的书籍信息"""


@app.route('/insertBook', methods=['GET', "POST"])
def insertBook():
    # 获取表单信息
    name = flask.request.values.get("name", "")
    author = flask.request.values.get("author", "")
    publisher = flask.request.values.get("publisher", "")
    publish_year = flask.request.values.get("publish_year", "")
    pages = flask.request.values.get("pages", "")
    price = flask.request.values.get("price", "")
    binding = flask.request.values.get("binding", "")
    series = flask.request.values.get("series", "")
    ISBN = flask.request.values.get("ISBN", "")
    # 插入数据到数据库
    try:
        sql = "INSERT INTO douban (name, author, publisher, publish_year, pages, price, binding, series, ISBN) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(sql, (name, author, publisher,
                             publish_year, pages, price, binding, series, ISBN))
        db.commit()
        print("成功插入一个新的书本数据记录!")
        # 跳转回主目录
        return flask.redirect(url_for('index'))
    except Exception as err:
        print("插入新数据出现错误:" + err)
        # 跳转到错误页面
        return flask.render_template('error.html')
    # 如果前面都没有跳转,则还是跳转停留在当前添加页面
    return flask.render_template('add.html')


"""删除特定的书籍信息,根据对应书本的id进行删除"""


@app.route('/deleteBook', methods=['GET', "POST"])
def deleteBook():
    # 获取前端传递的id参数
    id = flask.request.values.get('id', "")
    # 进行删除
    try:
        sql = "delete from douban where id = %s;"
        cursor.execute(sql, (id))
        db.commit()
        print("成功删除id为"+str(id)+"的书本数据记录!")
        # 跳转回主目录
        return flask.redirect(url_for('index'))
    except Exception as err:
        print("删除书本数据出现错误:" + err)
        # 跳转到错误页面
        return flask.render_template('error.html')
    # 如果前面没有跳转,则还是跳转回主目录
    return flask.redirect(url_for('index'))


# 启动服务器
#app.debug = True
try:
    app.run(host='0.0.0.0')
except Exception as err:
    print(err)
finally:
    cursor.close()  # 关闭游标对象
    db.close()  # 关闭数据库连接
