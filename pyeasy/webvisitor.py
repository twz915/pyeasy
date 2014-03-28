#!/usr/bin/python
#coding:utf-8

'''
easy to request web url
get(url,parameters)
post(url,parameters)
todo:
    getAllUrls
    getUrlAt(label1,label2)
    getUrlById
    getUrlByName
'''

import urllib 
import urllib2 

def get(url, data={}): 
    string = urllib.urlencode(data)
    url = url if ('?' in url) else (url+'?%s'%string)

    response = urllib.urlopen(url)
    return response.read()

def post(url, data): 
    req = urllib2.Request(url) 
    data = urllib.urlencode(data) 
    #enable cookie 
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor()) 
    response = opener.open(req, data) 
    return response.read() 
   
def main(): 
    posturl = "http://www.xiami.com/member/login" 
    data = {'email':'xxx', 'password':'xxx', 'autologin':'1', 'submit':'登 录', 'type':''} 
    print post(posturl, data) 
   
if __name__ == '__main__': 
    main()
