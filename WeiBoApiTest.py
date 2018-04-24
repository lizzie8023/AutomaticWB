#! /usr/bin/python
# -*- coding: utf-8 -*-
from weibo import APIClient
import urllib2
import urllib

#APP_KEY和APP_SECRET，需要新建一个微博应用才能得到
APP_KEY = '4106825333' #写自己的
APP_SECRET = '7dcd656bc3689ef845f810445aba2947'
#管理中心---应用信息---高级信息，将"授权回调页"的值改成https://api.weibo.com/oauth2/default.html
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
AUTH_URL = 'https://api.weibo.com/oauth2/authorize'

def GetCode(userid,passwd):
    client = APIClient(app_key = APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    referer_url = client.get_authorize_url()
    postdata = {
        "action": "login",
        "client_id": APP_KEY,
        "redirect_uri":CALLBACK_URL,
        "userId": userid,
        "passwd": passwd,
        }

    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0",
        "Referer":referer_url,
        "Connection":"keep-alive"
    }
    req  = urllib2.Request(
        url = AUTH_URL,
        data = urllib.urlencode(postdata),
        headers = headers
    )
    resp = urllib2.urlopen(req)
    return resp.geturl()[-32:]

if __name__ == "__main__":
    print GetCode('17165498565','123456a?')