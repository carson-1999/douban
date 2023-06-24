import requests  # http请求库
from bs4 import BeautifulSoup  # 数据解析库
import pymysql  # 存储数据到mysql
import threading  # 多线程



"""获取各本书的详情页面的urls"""


def get_detail_urls(url):
    resp = requests.get(url, headers=headers)
    html = resp.text
    soup = BeautifulSoup(html, 'lxml')  # 创建一个beautifulsoup对象
    detail_urls = []
    for link in soup.find_all('a', {'class': 'nbg'}):
        detail_urls.append(link.get('href'))
    return detail_urls


"""解析详情页面的内容并保存数据到Mysql数据库中"""


def parse_detail_url(detail_url):
    global num  # 全局变量,统计存入数据记录的条数
    #sql相关语句
    # 使用pymysql.connect方法连接本地mysql数据库
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root',password='root', database='mydb', charset='utf8')
    # 操作数据库，获取db下的cursor对象
    cursor = db.cursor()
    info = []  # 存储每本书的信息
    resp = requests.get(detail_url, headers=headers)
    html = resp.text
    soup = BeautifulSoup(html, 'lxml')
    # 获取书名
    try:
        name = soup.find('div', id='wrapper').find('h1').get_text().strip()
        #print(name)
    except Exception as e:
        print("获取书的名字出现错误,默认填充为空")
        name = 'null'
        #print("Error: {}".format(e))
    finally:
        info.append(name)
    # 获取书的作者
    try:
        if soup.find('div', id='info').find('span', text=' 作者'):
            author = soup.find('div', id='info').find(
                'span', text=' 作者').find_next_sibling('a').get_text().strip().replace('\n', ' ')
            #print(author)
        else:
            author = soup.find('div', id='info').find(
                'span', text='作者:').find_next_sibling('a').get_text().strip().replace('\n', ' ')
            #print(author)
    except Exception as e:
        print("获取书的作者出现错误,默认填充为空")
        author = 'null'
    finally:
        info.append(author)
    # 获取书的出版社
    try:
        publisher = soup.find('div', id='info').find(
            'span', text='出版社:').find_next_sibling('a').get_text().strip().replace('\n', ' ')
        #print(publisher)
    except Exception as e:
        print("获取书的出版社名出现错误,默认填充为空")
        publisher = 'null'
    finally:
        info.append(publisher)
    # 获取书的出版年
    try:
        publish_year = soup.find('div', id='info').find(
            'span', text='出版年:').find_next_sibling(text=True).strip()
        #print(publish_year)
    except Exception as e:
        print("获取书的出版年错误,默认填充为空")
        publish_year = 'null'
    finally:
        info.append(publish_year)
    # 获取书的页数
    try:
        pages = soup.find('div', id='info').find(
            'span', text='页数:').find_next_sibling(text=True).strip()
        #print(pages)
    except Exception as e:
        print("获取书的页数错误,默认填充为空!")
        pages = 'null'
    finally:
        info.append(pages)
    # 获取书的定价
    try:
        price = soup.find('div', id='info').find(
            'span', text='定价:').find_next_sibling(text=True).strip()
        #print(price)
    except Exception as e:
        print("获取书的定价出现错误,默认填充为空")
        price = 'null'
    finally:
        info.append(price)
    # 获取书的装帧方式
    try:
        binding = soup.find('div', id='info').find(
            'span', text='装帧:').find_next_sibling(text=True).strip()
        #print(binding)
    except Exception as e:
        print("获取书的装订方式出现错误,默认填充为空")
        binding = 'null'
    finally:
        info.append(binding)
    # 获取书的系列
    try:
        series = soup.find('div', id='info').find(
            'span', text='丛书:').find_next_sibling('a').get_text().strip().replace('\n', ' ')
        #print(series)
    except Exception as e:
        print("获取书的所属系列出现错误,默认填充为空")
        series = 'null'
    finally:
        info.append(series)
    # 获取书的ISBN
    try:
        ISBN = soup.find('div', id='info').find(
            'span', text='ISBN:').find_next_sibling(text=True).strip()
        #print(ISBN)
    except Exception as e:
        print("获取书的ISBN列出现错误,默认填充为空")
        ISBN = 'null'
    finally:
        info.append(ISBN)
    """保存数据到mysql的mydb数据库的douban数据表中"""
    # 查询是否已经存在该条数据记录
    select_sql = "SELECT * FROM douban WHERE name=%s AND author=%s AND publisher=%s AND publish_year=%s AND pages=%s AND price=%s AND binding=%s AND series=%s AND ISBN=%s"
    cursor.execute(select_sql, (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8]))
    result = cursor.fetchone()
    if result:
        #print("该条数据记录已经存在，不执行插入操作")
        pass
    else:
        # 执行插入数据的操作
        try:
            # 操作全局变量之前先获取线程锁
            lock.acquire()
            # 改变全局变量值
            num = num + 1
            
            # 执行sql
            sql = "insert into douban(id,name,author,publisher,publish_year,pages,price,binding,series,ISBN)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (num, info[0], info[1], info[2], info[3],
                                 info[4], info[5], info[6], info[7], info[8]))
            db.commit()  # 提交
            # 释放线程锁
            lock.release()
        except Exception as e:
            print("数据库保存Error: {}".format(e))
        finally:
            # 最后关闭数据库连接
            cursor.close()
            db.close()
            #打印信息
            print(info)
            info.clear()  # 清空列表,方便下次存储


# 主函数


def main():

    # 更改basic_url来爬取多页，观察得到规律25递增
    basic_url = 'https://book.douban.com/top250?start={}'
    # 爬取多页页面u的内容，利用for循环和.format()的25递增规律
    threads = []  # 线程列表threads
    urls = [] #存储需要爬取的10个页面链接
    for x in range(0, 226, 25):
        test_url = basic_url.format(x)
        urls.append(test_url)
    #print(urls)
    #爬取top250的总共10个页面
    for url in urls:
        print("当前爬取的页面url是:" + url)
        # 引入多线程来解析数据
        detailed_urls = get_detail_urls(url)
        print("当前页面中书的数量为:"+str(len(detailed_urls)))
        for detail_url in detailed_urls:
            parse_detail_url(detail_url)

    


    # -----------------------------------------------------------------------------
    # unit test,随便尝试一个链接
    #test_url = 'https://book.douban.com/top250?start=0'
    """
    # 引入多线程来解析数据,提高速度
    detailed_urls = get_detail_urls(test_url)
    threads = []  # 线程列表threads
    print("长度为:"+str(len(detailed_urls)))
    for detail_url in detailed_urls:
        t = threading.Thread(target=parse_detail_url, args=(detail_url,))
        threads.append(t)
    # 注意的是，如果我们不使用join()方法等待线程执行完毕，那么主线程可能会在子线程还没有执行完毕时就结束了。这可能会导致数据丢失或其他问题。因此，在使用多线程时，一定要记得使用join()方法等待所有线程执行完毕
    for t in threads:
        t.start()  # start()方法会开启一个新的线程并执行其中的代码
    for t in threads:
        t.join()  # join()方法会使主线程等待子线程执行完毕后再继续执行
    # 最后关闭数据库连接
    db.close()
    # 打印存入数据库的数据记录数
    print("成功存入数据库的记录条数为: "+str(num))
    """
    #-------------------------------------------------------------------------------


# 运行主程序
if __name__ == '__main__':
    # 伪造浏览器请求头信息,这里仅仅伪造浏览器信息和cookie信息
    # 自己账号的cookies,可以首次登录豆瓣后抓包从浏览器的请求参数中复制得到
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36', 'cookie': 'bid=fshpkUVp9qw; douban-fav-remind=1; ll="118282"; __utmz=30149280.1686675341.5.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ap_v=0,6.0; __utma=30149280.807619509.1683271702.1686675341.1687527143.6; __utmc=30149280; __utma=81379588.1698741621.1687527143.1687527143.1687527143.1; __utmc=81379588; __utmz=81379588.1687527143.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _pk_ses.100001.3ac3=*; dbcl2="271592659:8mu4EE7Kjzo"; ck=lXoC; __utmt_douban=1; __utmb=30149280.11.10.1687527143; __utmt=1; __utmb=81379588.11.10.1687527143; _pk_id.100001.3ac3=4f06a33bff62bde5.1687527143..1687532006.undefined.; push_noty_num=0; push_doumail_num=0'}

    # 统计存入数据库的记录数(全局变量)
    num = 0

    # 创建一个线程锁,保护全局变量
    lock = threading.Lock()
    #运行主函数（引入多线程）
    #main()
    threads = []  # 线程列表threads
    #创建8个线程(我的电脑是8核)
    for i in range(8):
        t = threading.Thread(target=main)
        threads.append(t)
    for t in threads:
        t.start()  # start()方法会开启一个新的线程并执行其中的代码
    for t in threads:
        t.join()  # join()方法会使主线程等待子线程执行完毕后再继续执行
    # 打印存入数据库的数据记录数
    print("成功存入数据库的记录条数为: "+str(num))
