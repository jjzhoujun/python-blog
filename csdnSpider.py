# -*- encoding: utf-8 -*-
'''
抓取个人博客列表，然后转成 md 文件保存， title是文件名
参考：Created on 2014-09-18 21:10:39

@author: Mangoer
@email: 2395528746@qq.com
'''

import urllib2
import re
from bs4 import BeautifulSoup
import random
import time


class CSDN_Blog_Spider:
    def __init__(self, url):

        print '\n'
        print('已启动网络爬虫。。。')
        print  '网页地址： ' + url

        user_agents = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
        ]
        # use proxy ip
        # ips_list = ['60.220.204.2:63000','123.150.92.91:80','121.248.150.107:8080','61.185.21.175:8080','222.216.109.114:3128','118.144.54.190:8118',
        #           '1.50.235.82:80','203.80.144.4:80']

        # ip = random.choice(ips_list)
        # print '使用的代理ip地址： ' + ip

        # proxy_support = urllib2.ProxyHandler({'http':'http://'+ip})
        # opener = urllib2.build_opener(proxy_support)
        # urllib2.install_opener(opener)

        agent = random.choice(user_agents)

        req = urllib2.Request(url)
        req.add_header('User-Agent', agent)
        req.add_header('Host', 'blog.csdn.net')
        req.add_header('Accept', '*/*')
        req.add_header('Referer', 'http://blog.csdn.net/mangoer_ys?viewmode=list')
        req.add_header('GET', url)
        html = urllib2.urlopen(req)
        page = html.read().decode('gbk', 'ignore').encode('utf-8')

        self.page = page
        self.title = self.getTitle()
        self.content = self.getContent()
        self.saveFile()

    def printInfo(self):
        print('文章标题是：   ' + self.title + '\n')
        print('内容已经存储到out.txt文件中！')

    def getTitle(self):
        rex = re.compile('<title>(.*?)</title>', re.DOTALL)
        match = rex.search(self.page)
        if match:
            return match.group(1)

        return 'NO TITLE'

    def getContent(self):
        bs = BeautifulSoup(self.page)
        html_content_list = bs.findAll('div', {'id': 'article_content', 'class': 'article_content'})
        html_content = str(html_content_list[0])

        rex_p = re.compile(r'(?:.*?)>(.*?)<(?:.*?)', re.DOTALL)
        p_list = rex_p.findall(html_content)

        content = ''
        for p in p_list:
            if p.isspace() or p == '':
                continue
            content = content + p
        return content

    def saveFile(self):

        outfile = open('out.txt', 'a')
        outfile.write(self.content)

    def getNextArticle(self):
        bs2 = BeautifulSoup(self.page)
        html_nextArticle_list = bs2.findAll('li', {'class': 'prev_article'})
        # print str(html_nextArticle_list[0])
        html_nextArticle = str(html_nextArticle_list[0])
        # print html_nextArticle

        rex_link = re.compile(r'<a href=\"(.*?)\"', re.DOTALL)
        link = rex_link.search(html_nextArticle)
        # print link.group(1)

        if link:
            next_url = 'http://blog.csdn.net' + link.group(1)
            return next_url

        return None


class Scheduler:
    def __init__(self, url):
        self.start_url = url

    def start(self):
        spider = CSDN_Blog_Spider(self.start_url)
        spider.printInfo()

        while True:
            if spider.getNextArticle():
                spider = CSDN_Blog_Spider(spider.getNextArticle())
                spider.printInfo()
            elif spider.getNextArticle() == None:
                print 'All article haved been downloaded!'
                break

            time.sleep(10)


# url = input('请输入CSDN博文地址：')
url = "http://blog.csdn.net/mangoer_ys/article/details/38427979"

Scheduler(url).start()