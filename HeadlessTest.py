#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#

import time, json
from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# import logging
from yundama import identify


from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('user-agent="Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')

IDENTIFY = 2  # 验证码输入方式:        1:看截图aa.png，手动输入     2:云打码
COOKIE_GETWAY = 0 # 0 代表从https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18) 获取cookie   # 1 代表从https://weibo.cn/login/获取Cookie
# dcap = dict(DesiredCapabilities.PHANTOMJS)  # PhantomJS需要使用老版手机的user-agent，不然验证码会无法通过
# dcap["phantomjs.page.settings.userAgent"] = (
#     "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
# )
# logger = logging.getLogger(__name__)
# logging.getLogger("selenium").setLevel(logging.WARNING)


myWeiBo = [
    ('17165491160', 'password001')
]

def get_cookie_from_weibo_cn(account, password):

    driver = webdriver.Chrome('/Users/Lizzie/Desktop/AutomaticWB/Linux/chromedriver', chrome_options=chrome_options)
    driver.get('https://weibo.cn/login/')

    time.sleep(1)

    failure = 0

    while u"微博" in driver.title and failure < 5:
        failure += 1
        driver.save_screenshot("aa.png")
        username = driver.find_element_by_id('loginName')
        username.clear()
        username.send_keys(account)

        psd = driver.find_element_by_xpath('//input[@type="password"]')
        psd.clear()
        psd.send_keys(password)
        try:
            code = driver.find_element_by_name("code")
            code.clear()
            if IDENTIFY == 1:
                code_txt = raw_input("请查看路径下新生成的aa.png，然后输入验证码:")  # 手动输入验证码
            else:
                from PIL import Image
                img = driver.find_element_by_xpath('//form[@method="post"]/div/img[@alt="请打开图片显示"]')
                x = img.location["x"]
                y = img.location["y"]
                im = Image.open("aa.png")
                im.crop((x, y, 100 + x, y + 22)).save("ab.png")  # 剪切出验证码
                code_txt = identify()  # 验证码打码平台识别
            code.send_keys(code_txt)
        except Exception, e:
            pass

        commit = driver.find_element_by_id('loginAction')
        commit.click()
        time.sleep(3)
        if u"我的首页" not in driver.title:
            time.sleep(4)
        if u'未激活微博' in driver.page_source:
            print '账号未开通微博'
            return {}

    cookie = {}
    if u"我的首页" in driver.title:
        for elem in driver.get_cookies():
            cookie[elem["name"]] = elem["value"]
    return json.dumps(cookie)


if __name__=='__main__':
    for weibo in myWeiBo:
        print get_cookie_from_weibo_cn(weibo[0],weibo[1])