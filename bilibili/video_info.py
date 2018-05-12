#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#

import time, json, re
from os import path
from urllib import quote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.action_chains import ActionChains
from sklearn.metrics import euclidean_distances
from elasticsearch import Elasticsearch
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')
import requests

chrome_options = Options()

chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('user-agent="Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')

def log(content):
    print(content)


path_temp = path.dirname(__file__)
path_temp = path.dirname(path_temp)
path_temp = path_temp + '/Mac/chromedriver'
# path_temp = '/home/service/guanba-data/guanba-data-parser/test/AutomaticWB/Linux/chromedriver'

def dele_es_doc():
    es = Elasticsearch(["http://114.215.128.188"], port=9200)
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
        url = 'http://114.215.128.188:9200/sampling_bilibili_video/video/'+index
        print requests.delete(url)

    for i in arr:
        url = 'http://114.215.128.188:9200/sampling_bilibili_video/video/' + i
        print requests.delete(url)


def load_video_info(i):
    try:
        video_url = i.find_element_by_xpath('.//a[@target="_blank"]').get_attribute('href')
        print(video_url)
        driver2 = webdriver.Chrome(path_temp, chrome_options=chrome_options)
        driver2.get(video_url)
        time.sleep(2)
        return driver2
    except:
        return None

def load_videos_info():
    es = Elasticsearch(["http://114.215.128.188"],port=9200)
    # es = Elasticsearch(["http://10.29.168.134"], port=9200)
    page = es.search(index="sampling_bilibili_target", doc_type="target", scroll='2m')

    sid = page['_scroll_id']
    scroll_size = page['hits']['total']
    list_temp = []
    while(scroll_size > 0):
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

    total = 0
    index = 0
    for i in list_temp:
        print(i['_source']['account_name'])
        if i['_source']['account_name'] == u'吴磊的爱丽丝':
            index = total
            # break
        else:
            total = total + 1
    print('总数:%d, 当前:%d'%(total,index))
    return
    list_temp = list_temp[261:int(list_temp.__len__())]
    driver = webdriver.Chrome(path_temp, chrome_options=chrome_options)
    driver.set_window_size(1680, 1050)

    def save_target_account(data):
        print es.index(index="sampling_bilibili_video", doc_type="video", body=data)

    for i in list_temp:
        url = i['_source']['link_url']
        account_name = i['_source']['account_name']
        target_name = i['_source']['target_name']
        print(i['_source']['account_name'])
        time.sleep(2)
        driver.get(url)
        #********#
        # print(driver.page_source)
        # more_btn = driver.find_element_by_xpath('//*[@id="page-index"]/div[1]/div[2]/h3/a[2]')
        # more_btn.click()
        # time.sleep(2)
        # has_more = True
        # while has_more:
        #     video_list = driver.find_element_by_xpath('//div[@id="video-list-style"]')
        #     submit_video_list = video_list.find_elements_by_xpath('.//li[@class="list-item clearfix fakeDanmu-item"]')
        #     for i in submit_video_list:
        #
        #         driver2 = load_video_info(i)
        #         if driver2 is None:
        #             continue
        #
        #         play_count = driver2.find_element_by_xpath('//*[@id="viewbox_report"]/div[2]/span[1]').text
        #         barrage_count = driver2.find_element_by_xpath('//*[@id="viewbox_report"]/div[2]/span[2]').text
        #         exceptional_count = driver2.find_element_by_xpath('//*[@id="viewbox_report"]/div[2]/span[4]').text
        #         collection_count = driver2.find_element_by_xpath('//*[@id="viewbox_report"]/div[2]/span[5]').text
        #         share_count = driver2.find_element_by_xpath('//*[@id="playpage_share"]/div[1]/span[2]').text
        #         video_title = driver2.find_element_by_xpath('//*[@id="viewbox_report"]/h1/span').text
        #         video_publish_time = driver2.find_element_by_xpath('//*[@id="viewbox_report"]/div[1]').text
        #         # comment_count = driver2.find_element_by_xpath('//span[@class="b-head-t results"]')
        #         data_temp3 = {}
        #         if u'万' in play_count:
        #             play_count2 = re.findall(r'\d+\.?\d*', play_count)[0]
        #             data_temp3['play_count'] = str(int(float(play_count2) * 10000))
        #         else:
        #             data_temp3['play_count'] = play_count
        #
        #         video_publish_time = str(
        #             re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", video_publish_time)[0])
        #
        #         data_temp3['barrage_count'] = barrage_count
        #         data_temp3['exceptional_count'] = exceptional_count.split(' ')[1]
        #         data_temp3['collection_count'] = collection_count.split(' ')[1]
        #         data_temp3['share_count'] = share_count
        #         data_temp3['account_name'] = account_name
        #         data_temp3['target_name'] = target_name
        #         data_temp3['video_title'] = video_title
        #         data_temp3['video_publish_time'] = video_publish_time
        #         save_target_account(data_temp3)
        #         driver2.close()
        #
        #     try:
        #         button = video_list.find_element_by_xpath('.//li[@class="be-pager-next"]')
        #         button.click()
        #         time.sleep(2)
        #     except:
        #         # data = {'target_name':name,'accounts':accounts}
        #         # save_target_account(es,data)
        #         print('没有下一页')
        #         has_more = False
        #********#
        try:
            more_btn = driver.find_element_by_xpath('//*[@id="page-index"]/div[1]/div[2]/h3/a[2]')
            more_btn.click()
            time.sleep(2)
        except:
            driver.refresh()
            try:
                more_btn = driver.find_element_by_xpath('//*[@id="page-index"]/div[1]/div[2]/h3/a[2]')
                more_btn.click()
                time.sleep(2)
            except:
                continue
        has_more = True
        while has_more:
            video_list = driver.find_element_by_xpath('//div[@id="video-list-style"]')
            submit_video_list = video_list.find_elements_by_xpath('.//li[@class="list-item clearfix fakeDanmu-item"]')
            for i in submit_video_list:

                driver2 = load_video_info(i)
                if driver2 is None:
                    continue
                try:

                    play_count = driver2.find_element_by_xpath('//*[@id="viewbox_report"]/div[2]/span[1]').text
                    barrage_count = driver2.find_element_by_xpath('//*[@id="viewbox_report"]/div[2]/span[2]').text
                    exceptional_count = driver2.find_element_by_xpath('//*[@id="viewbox_report"]/div[2]/span[4]').text
                    collection_count = driver2.find_element_by_xpath('//*[@id="viewbox_report"]/div[2]/span[5]').text
                    share_count = driver2.find_element_by_xpath('//*[@id="playpage_share"]/div[1]/span[2]').text
                    video_title = driver2.find_element_by_xpath('//*[@id="viewbox_report"]/h1/span').text
                    video_publish_time = driver2.find_element_by_xpath('//*[@id="viewbox_report"]/div[1]').text
                    # comment_count = driver2.find_element_by_xpath('//span[@class="b-head-t results"]')
                    data_temp3 = {}
                    if u'万' in play_count:
                        play_count2 = re.findall(r'\d+\.?\d*', play_count)[0]
                        data_temp3['play_count'] = str(int(float(play_count2) * 10000))
                    else:
                        data_temp3['play_count'] = play_count

                    video_publish_time = str(re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", video_publish_time)[0])

                    data_temp3['barrage_count'] = barrage_count
                    data_temp3['exceptional_count'] = exceptional_count.split(' ')[1]
                    data_temp3['collection_count'] = collection_count.split(' ')[1]
                    data_temp3['share_count'] = share_count
                    data_temp3['account_name'] = account_name
                    data_temp3['target_name'] = target_name
                    data_temp3['video_title'] = video_title
                    data_temp3['video_publish_time'] = video_publish_time
                    save_target_account(data_temp3)
                    driver2.close()
                except:
                    driver2.refresh()
                    try:
                        play_count = driver2.find_element_by_xpath('//*[@id="viewbox_report"]/div[2]/span[1]').text
                        barrage_count = driver2.find_element_by_xpath('//*[@id="viewbox_report"]/div[2]/span[2]').text
                        exceptional_count = driver2.find_element_by_xpath(
                            '//*[@id="viewbox_report"]/div[2]/span[4]').text
                        collection_count = driver2.find_element_by_xpath(
                            '//*[@id="viewbox_report"]/div[2]/span[5]').text
                        share_count = driver2.find_element_by_xpath('//*[@id="playpage_share"]/div[1]/span[2]').text
                        video_title = driver2.find_element_by_xpath('//*[@id="viewbox_report"]/h1/span').text
                        video_publish_time = driver2.find_element_by_xpath('//*[@id="viewbox_report"]/div[1]').text
                        # comment_count = driver2.find_element_by_xpath('//span[@class="b-head-t results"]')
                        driver2.close()
                        data_temp3 = {}
                        if u'万' in play_count:
                            play_count2 = re.findall(r'\d+\.?\d*', play_count)[0]
                            data_temp3['play_count'] = str(int(float(play_count2) * 10000))
                        else:
                            data_temp3['play_count'] = play_count

                        video_publish_time = str(
                            re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", video_publish_time)[0])

                        data_temp3['barrage_count'] = barrage_count
                        data_temp3['exceptional_count'] = exceptional_count.split(' ')[1]
                        data_temp3['collection_count'] = collection_count.split(' ')[1]
                        data_temp3['share_count'] = share_count
                        data_temp3['account_name'] = account_name
                        data_temp3['target_name'] = target_name
                        data_temp3['video_title'] = video_title
                        data_temp3['video_publish_time'] = video_publish_time
                        save_target_account(data_temp3)
                    except:
                        try:
                            driver2.close()
                        except:
                            pass
                        continue
            try:
                button = video_list.find_element_by_xpath('.//li[@class="be-pager-next"]')
                button.click()
                time.sleep(2)
            except:
                # data = {'target_name':name,'accounts':accounts}
                # save_target_account(es,data)
                print('没有下一页')
                has_more = False


def test():
    url = 'https://www.bilibili.com/video/av19982324'
    driver = webdriver.Chrome(path_temp, chrome_options=chrome_options)
    driver.set_window_size(1680, 1050)
    driver.get(url)

    print(driver.page_source)
    aa = driver.find_element(u'分享')

    print(aa)
# dele_es_doc()
# load_videos_info()
test()
exit()
quit()