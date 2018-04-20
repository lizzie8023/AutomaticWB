#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from weibo import APIClient
import webbrowser  # python内置的包
import requests

type = sys.getfilesystemencoding()
APP_KEY = '2517952414'
APP_SECRET = '1b5cbde6c1689409c9372c1b153e5a7e'
CALLBACK_URL = 'http://dev.guanba.com/article/hot'

# 利用官方微博SDK
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

vipClient = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL, domain='c.api.weibo.com')
# 得到授权页面的url，利用webbrowser打开这个url
url = client.get_authorize_url()
# print url
# webbrowser.open_new(url)
# 获取code=后面的内容
# print '输入url中code后面的内容后按回车键：'
# code = raw_input()
r = "2.00QBWS1Gi8E6kC9374805e8aKs49TE"
# code = your.web.framework.request.get('code')
# client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
# r = client.request_access_token(code)
# access_token = r.access_token # 新浪返回的token，类似abc123xyz456
# expires_in = r.expires_in
access_token = "2.00QBWS1Gi8E6kC9374805e8aKs49TE"
expires_in = 36000

# 设置得到的access_token
vipClient.set_access_token(access_token, expires_in)

def weibo_post(text, imgs=[], url=False):
    url_post_pic = "https://c.api.weibo.com/2/statuses/upload/biz.json"
    utext = unicode(text.encode('utf-8'), 'UTF-8')
    data = {'access_token': vipClient.access_token, 'status': utext}
    r = requests.post(url_post_pic, data=data)
    print(r)

weibo_post('test')