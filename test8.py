#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#


import requests
import json, time, re, hashlib
from bs4 import BeautifulSoup

# url = 'https://space.bilibili.com/81800692/#/'
#
# header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
# response = requests.get(url, headers=header)
# html = response.text
# soup = BeautifulSoup(html, 'lxml')
# print(soup.text)

def calc_sign(str):
    hash = hashlib.md5()
    hash.update(str.encode('utf-8'))
    sign = hash.hexdigest()
    return sign


header1 = {'Host':'app.bilibili.com',
          'User-Agent':'bili-universal/6680 CFNetwork/893.14.2 Darwin/17.3.0',
          'Accept-Language':'zh-cn',
          'Buvid':'b357782fe6750524e5ad96bf2917e',
          'Accept-Encoding':'gzip'}

header2 = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

url_temp = 'https://space.bilibili.com/15735926?from=search&seid=15941148688358398306'
# user_id = re.findall(r"\d+\.?\d*", url_temp)
user_id = url_temp.split('?')[0]
user_id = user_id.split('/')[3]

has_more = True
pn = 1
while has_more:
    url = 'https://app.bilibili.com/x/v2/space/archive?actionKey=appkey&appkey=27eb53fc9058f8c3&build=6680&device' \
          '=phone&mobi_app=iphone&platform=ios&pn=%d&ps=20&vmid=%s'%(pn,user_id)
    response = requests.get(url, headers=header1)
    dict_temp = json.loads(response.text).get('data')
    if dict_temp is not None:
        list_temp = dict_temp.get('item')
        if list_temp is not None:
            if list_temp.__len__() > 1:
                pn = pn + 1
                for i in list_temp:
                    aid = i['param']
                    url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid=%s'%(aid)
                    response = requests.get(url, headers=header2)
                    data_temp = {}
                    dict_temp2 = json.loads(response.text).get('data')
                    if dict_temp2 is not None:
                        data_temp['play_count'] = dict_temp2['view']
                        data_temp['barrage_count'] = dict_temp2['danmaku']
                        data_temp['exceptional_count'] = dict_temp2['']
                        data_temp['collection_count'] = dict_temp2['favorite']
                        data_temp['share_count'] = dict_temp2
                        data_temp['account_name'] = dict_temp2
                        data_temp['target_name'] = dict_temp2
                        data_temp['video_title'] = dict_temp2
                        data_temp['video_publish_time'] = dict_temp2
            else:
                has_more = False
        else:
            has_more = False
