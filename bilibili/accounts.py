#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#

import time, json
from os import path
from urllib import quote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.action_chains import ActionChains
from sklearn.metrics import euclidean_distances
from elasticsearch import Elasticsearch
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('user-agent="Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')

def log(content):
    print(content)

path_temp = path.dirname(__file__)
path_temp = path.dirname(path_temp)
path_temp = path_temp + '/Mac/chromedriver'
driver = webdriver.Chrome(path_temp, chrome_options=chrome_options)
driver.set_window_size(1680, 1050)

source = '鹿晗、张艺兴、王俊凯、易烊千玺、王源、吴亦凡、黄子韬、杨洋、迪丽热巴、李易峰、蔡徐坤、范丞丞、朱正廷、陈立农、吴宣仪、黄明昊justin、杨幂、郑爽、赵丽颖、ANGERLABABY、范冰冰、谢娜、陈伟霆、周冬雨、黄晓明、刘昊然、靳东、关晓彤、彭于晏、华晨宇、唐嫣、胡歌、周杰伦、吴磊、井柏然、刘涛、宋茜、王嘉尔、杨紫、张杰、王凯、林更新、王子异、毛不易、黄景瑜、小鬼、张翰、李宇春、许魏洲、韩东君、Ninepercent、tfboys、Taylor Swift、Justin Bieber、Charlie Puth、Ariana Grande、Beyonce、Rihanna、Jasper、安吉、嗯哼、谢娜、张杰、邓超、孙俪、昆凌、胡一天、沈月'
sources = source.split('、')

config = {"host": "127.0.0.1",
             "port": 3306,
             "user": "root",
             "passwd": "password",
             "db_name": "mysql",
             "charset": "utf8mb4"}

def connectdb():
    print('连接到mysql服务器...')
    # 打开数据库连接
    host = config["host"]
    user = config["user"]
    passwd = config["passwd"]
    db_name = config["db_name"]
    port = config["port"]
    charset = config["charset"]
    db = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db_name, charset=charset)
    print('连接上了!')
    return db

def createTable(db):

    db_name = config["db_name"]

    cursor = db.cursor()
    sql = "create table if not exists bilibili (id int primary key not null auto_increment, name text(20), " \
          "video_count bigint(20), fans_count text(20), url text(256)) default charset=utf8;"
    cursor.execute(sql)

    cursor.execute("ALTER DATABASE `%s` CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci'" % db_name)

def save_target_account(db,data):
    # name = data["name"]
    # video_count = data["video_count"]
    #
    # sql = "INSERT INTO bilibili(name, video_count, fans_count, url) VALUES ('%s','%s' , '%s', '%s')" % (
    #           name, data["video_count"], data["fans_count"], data['link_url'])
    # cursor = db.cursor()
    # cursor.execute(sql)
    # db.commit()
    print es.index(index="sampling_bilibili_target", doc_type="target", body=data)


db = connectdb()
createTable(db)
es = Elasticsearch(["http://114.215.128.188"],port=9200)

for name in sources:
    url = 'https://search.bilibili.com/upuser?keyword=%s'%(quote(name))
    driver.get(url)
    time.sleep(3)
    driver.refresh()
    time.sleep(3)
    users = driver.find_element_by_xpath('//*[@id="server-search-app"]/div[2]/div[1]/div[2]/ul/li[9]')
    users.click()
    time.sleep(3)
    has_more = True
    page = 1
    accounts = []
    while has_more:
        if page > 10:
            has_more = False
            continue
        user_wrap = driver.find_element_by_class_name('user-wrap')
        info_wrap = user_wrap.find_elements_by_class_name('info-wrap')
        for info in info_wrap:

            try:
                headline = info.find_element_by_class_name('headline')
                text1 = headline.text
                text2 = info.find_element_by_xpath('.//div[@class="up-info clearfix"]').text
                text3 = info.find_element_by_xpath('.//a[@class="video-more"]').text
                account_name = text1.split(' + ')[0]
                video_count = text2.split('\n')[0].split('：')[1]
                fans_count = text2.split('\n')[1].split('：')[1]
                link_url = headline.find_element_by_xpath('.//a[@target="_blank"]').get_attribute('href')
                data = {'account_name':account_name,
                        'target_name':name,
                        'video_count':video_count,
                        'fans_count':fans_count,
                        'link_url':link_url}
                # save_target_account(db,data)
                # accounts.append(data)
                save_target_account(es,data)
                print("account_name:%s,video_count:%s,fans_count:%s,link_url:%s"%(account_name,video_count,fans_count,link_url))
            except:
                pass

        try:
            button = user_wrap.find_element_by_xpath('.//li[@class="page-item next"]')
            button.click()
            page = page + 1
            time.sleep(5)
        except:
            # data = {'target_name':name,'accounts':accounts}
            # save_target_account(es,data)
            print('没有下一页')
            has_more = False
    time.sleep(5)

exit()
quit()