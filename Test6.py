#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#

import time, json, re
from elasticsearch import Elasticsearch
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')
import requests


def dele_es_doc():
    es = Elasticsearch(["http://10.29.168.134"], port=9200)
    page = es.search(index="sampling_bilibili_video", doc_type="video", scroll='2m')

    sid = page['_scroll_id']
    scroll_size = page['hits']['total']
    list_temp = []
    while (scroll_size > 0):
        # print('scrolling.... current scroll_id:%s'%sid)
        page = es.scroll(scroll_id=sid, scroll='2m')
        sid = page['_scroll_id']
        scroll_size = len(page['hits']['hits'])
        data_temp1 = page['hits']['hits']
        for i in data_temp1:
            list_temp.append(i)
    arr = []
    for i in list_temp:
        index = i['_id']
        url = 'http://114.215.128.188:9200/sampling_bilibili_video/video/' + index
        print requests.delete(url)

    for i in arr:
        url = 'http://114.215.128.188:9200/sampling_bilibili_video/video/' + i
        print requests.delete(url)

def save_target_account(es,data):
    print es.index(index="sampling_bilibili_video", doc_type="video", body=data)

def load_videos_info():

    es = Elasticsearch(["http://10.29.168.134"], port=9200)
    page = es.search(index="sampling_bilibili_target", doc_type="target", scroll='2m')
    sid = page['_scroll_id']
    scroll_size = page['hits']['total']
    list_temp = []
    header1 = {'Host': 'app.bilibili.com',
               'User-Agent': 'bili-universal/6680 CFNetwork/893.14.2 Darwin/17.3.0',
               'Accept-Language': 'zh-cn',
               'Buvid': 'b357782fe6750524e5ad96bf2917e',
               'Accept-Encoding': 'gzip'}

    header2 = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    while (scroll_size > 0):
        # print('scrolling.... current scroll_id:%s'%sid)
        page = es.scroll(scroll_id=sid, scroll='2m')
        sid = page['_scroll_id']
        scroll_size = len(page['hits']['hits'])
        data_temp1 = page['hits']['hits']
        for i in data_temp1:
            data_temp2 = i.get('_source').get('link_url')
            if data_temp2 is not None:
                list_temp.append(i)
            else:
                pass

    for i in list_temp:
        url_temp = i['_source']['link_url']
        account_name = i['_source']['account_name']
        target_name = i['_source']['target_name']
        # user_id = re.findall(r"\d+\.?\d*", url_temp)
        user_id = url_temp.split('?')[0]
        user_id = user_id.split('/')[3]

        has_more = True
        pn = 1
        while has_more:
            url = 'https://app.bilibili.com/x/v2/space/archive?actionKey=appkey&appkey=27eb53fc9058f8c3&build=6680&device' \
                  '=phone&mobi_app=iphone&platform=ios&pn=%d&ps=20&vmid=%s' % (pn, user_id)
            response = requests.get(url, headers=header1)
            dict_temp = json.loads(response.text).get('data')
            if dict_temp is not None:
                list_temp = dict_temp.get('item')
                if list_temp is not None:
                    if list_temp.__len__() > 1:
                        pn = pn + 1
                        for i in list_temp:
                            aid = i['param']
                            url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid=%s' % (aid)
                            response = requests.get(url, headers=header2)
                            data_temp = {}
                            dict_temp2 = json.loads(response.text).get('data')
                            if dict_temp2 is not None:
                                data_temp['play_count'] = dict_temp2['view']
                                data_temp['barrage_count'] = dict_temp2['danmaku']
                                data_temp['collection_count'] = dict_temp2['favorite']
                                data_temp['share_count'] = dict_temp2['share']
                                data_temp['exceptional_count'] = dict_temp2['coin']
                                data_temp['account_name'] = account_name
                                data_temp['target_name'] = target_name
                                data_temp['video_title'] = i['title']
                                data_temp['video_publish_time'] = i['ctime']
                                save_target_account(es,data_temp)
                            time.sleep(1)
                    else:
                        has_more = False
                else:
                    has_more = False



# dele_es_doc()
load_videos_info()
exit()
quit()