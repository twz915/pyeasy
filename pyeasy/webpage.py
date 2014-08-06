#! /usr/bin/python
#coding:utf-8
from __future__ import print_function, unicode_literals

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from bs4 import BeautifulSoup as BS
import urllib
import os
import re


class WebPage(object):
    def __init__(self,url):
        self.url = url
        self.domain = url.split('/')[0]
        self.current_dir = os.path.dirname(url)

        self.data = BS(urllib.urlopen(self.url),'html5lib')
        
        self.head = self.data.head

        self.title = self.head.title.string
        self.keywords = self.head.find('meta',{'name':'keywords'})['content']
        self.description = self.head.find('meta',{'name':'description'})['content']
        
        self.body = self.data.body


    def find(self,string):
        #string: <a id='main' rel="nofollow"
        pass

    def find_hrefs(self,reg):# 找符合正则的网址
        for link in self.data.find_all(href=re.compile(reg)):
            url = link.get('href')
            yield self.convert_to_absolute_url(url)

    @property
    def all_pics(self, formats=[]):
        if not formats:
            formats = (
                '.png',
                '.jpg',
                '.jpeg',
                '.gif',
                '.bmp',
            )
        # <img src="/static/images/logo.png" alt="自强学堂 logo />
        for img in self.data.find_all('img'):
            url = img.get('src')
            if url.endswith(tuple(formats)):
                yield self.convert_to_absolute_url(url)


    @property
    def all_attachments(self, formats=[]):
        if not formats:
            formats = ('.rar','.zip','.mp3','.mp4','.js','.css')
        
        all_links = (
            # <a href="url">链接</a>
            self.all_links,
            # <link rel="stylesheet" type="text/css" href="/static/css/stdtheme.css">
            self.data.find_all('link', rel="stylesheet"),
            # <script src="/static/js/jquery-1.11.1.min.js" ></script>
            self.data.find_all('script'),
        )

        return [link for categrory in all_links for link in categrory if link.endswith(formats)]


    @property
    def all_links(self): # 找出所有的链接
        for link in self.data.find_all('a'):
            if not link.has_attr('href'):
                continue
            url = link.get('href')

            yield self.convert_to_absolute_url(url)


    def convert_to_absolute_url(self,url):
        if not url.startswith(('http','ftp')):
            if url.startswith('/'):
                url = '%s%s'%(self.domain,url)
            else:
                url = os.path.join(self.current_dir, url)

        return url



if __name__ == '__main__':
    p = WebPage('http://www.xiaomi.com')
    print(p.title)
    print(p.keywords)
    print(list(p.all_pics))
    #print(list(p.all_attachments))
    print("Done!")
