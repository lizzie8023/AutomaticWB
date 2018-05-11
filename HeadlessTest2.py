#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#

import time, json, os, random, StringIO
from selenium import webdriver
from PIL import Image
from io import BytesIO
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.action_chains import ActionChains
from sklearn.metrics import euclidean_distances
from math import sqrt
import numpy as np
from images import images


from yundama import identify

chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('user-agent="Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')

IDENTIFY = 2  # 验证码输入方式:        1:看截图aa.png，手动输入     2:云打码
COOKIE_GETWAY = 0 # 0 代表从https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18) 获取cookie   # 1 代表从https://weibo.cn/login/获取Cookie

myWeiBo = [
    ('17165491160', 'password001')
]

PIXELS = []

def getExactly(im):
    """ 精确剪切"""
    imin = -1
    imax = -1
    jmin = -1
    jmax = -1
    row = im.size[0]
    col = im.size[1]
    for i in range(row):
        for j in range(col):
            if im.load()[i, j] != 255:
                imax = i
                break
        if imax == -1:
            imin = i

    for j in range(col):
        for i in range(row):
            if im.load()[i, j] != 255:
                jmax = j
                break
        if jmax == -1:
            jmin = j
    return (imin + 1, jmin + 1, imax + 1, jmax + 1)


def getType(browser):
    """ 识别图形路径 """
    ttype = ''
    time.sleep(5)
    im0 = Image.open(BytesIO(browser.get_screenshot_as_png()))
    box = browser.find_element_by_id('patternCaptchaHolder')
    # im = im0.crop((int(box.location['x']) + 10,
    #                int(box.location['y']) + 100,
    #                int(box.location['x']) + box.size['width'] - 10,
    #                int(box.location['y']) + box.size['height'] - 10)).convert('L')

    im = im0.crop(((int(box.location['x']) + 10) * 2,
                   (int(box.location['y']) + 100) * 2,
                   (int(box.location['x']) + box.size['width'] - 10) * 2,
                   (int(box.location['y']) + box.size['height'] - 10) * 2)).convert('L')

    newBox = getExactly(im)
    im.crop(newBox).convert('L').save('b1.png')
    im = im.crop(newBox)
    # im = im.resize((230,220))
    # data = list(im.getdata())
    # print data
    # save_pngs(data)
    # browser.refresh()
    #
    #
    # return
    width = im.size[0]
    height = im.size[1]
    print(width,height)

    for png in images.keys():
        isGoingOn = True
        for i in range(width):
            for j in range(height):
                if ((im.load()[i, j] >= 245 and images[png][i][j] < 245) or
                        (im.load()[i, j] < 245 and images[png][i][j] >= 245)) and \
                                abs(images[png][i][j] - im.load()[i, j]) > 10:  # 以245为临界值，大约245为空白，小于245为线条；两个像素之间的差大约10，是为了去除245边界上的误差
                    isGoingOn = False
                    break
            if isGoingOn is False:
                ttype = ''
                break
            else:
                ttype = png
        else:
            break
    px0_x = box.location['x'] + 40 + newBox[0]
    px1_y = box.location['y'] + 130 + newBox[1]
    PIXELS.append((px0_x, px1_y))
    PIXELS.append((px0_x + 100, px1_y))
    PIXELS.append((px0_x, px1_y + 100))
    PIXELS.append((px0_x + 100, px1_y + 100))

    return ttype

def save_pngs(data):
    flag = input("sdfs:")
    if images.get('%s'%(str(flag))) is None:
        print('正在保存')
        images['%s'%(str(flag))] = data
        with open("images.py", "w") as f:
            f.write('%s=%s' % ("images", images))
    else:
        print('已存在,不需要保存')

    # if flag == 1:
    #     images["png"] = data
    #     with open("images.py", "w") as f:
    #         f.write('%s=%s' % ("images", images))
    #     time.sleep(20)

def getType_similirity(browser):

    """ 识别图形路径 ，采用欧氏距离计算相似度"""
    time.sleep(3.5)
    im0 = Image.open(StringIO.StringIO(browser.get_screenshot_as_png()))
    box = browser.find_element_by_id('patternCaptchaHolder')
    # im0 = im0.resize((1050, 840))
    # im = im0.crop((int(box.location['x']) + 10, int(box.location['y']) + 100,
    #                int(box.location['x']) + box.size['width'] - 10,
    #                int(box.location['y']) + box.size['height'] - 10)).convert('L')
    im = im0.crop(((int(box.location['x']) + 10) * 2,
                   (int(box.location['y']) + 100) * 2,
                   (int(box.location['x']) + box.size['width'] - 10) * 2,
                   (int(box.location['y']) + box.size['height'] - 10) * 2)).convert('L')

    newBox = getExactly(im)
    im = im.crop(newBox)
    im.save('b1.png')
    data = list(im.getdata())
    data_vec = np.array(data)
    vectDict = {}

    for i, j in images.items():
        vect = euclidean_distances(data_vec, j)
        vectDict[i] = vect[0][0]

    """对欧氏距离计算结果排序，取最小值"""
    sortDict = sorted(vectDict.iteritems(), key=lambda d: d[1], reverse=True)
    ttype = sortDict[-1][0]
    px0_x = box.location['x'] + 40 + newBox[0]
    px1_y = box.location['y'] + 130 + newBox[1]
    PIXELS.append((px0_x, px1_y))
    PIXELS.append((px0_x + 100, px1_y))
    PIXELS.append((px0_x, px1_y + 100))
    PIXELS.append((px0_x + 100, px1_y + 100))
    return ttype

def move(browser, coordinate, coordinate0):
    """ 从坐标coordinate0，移动到坐标coordinate """
    time.sleep(0.05)
    length = sqrt((coordinate[0] - coordinate0[0]) ** 2 + (coordinate[1] - coordinate0[1]) ** 2)  # 两点直线距离
    if length < 4:  # 如果两点之间距离小于4px，直接划过去
        ActionChains(browser).move_by_offset(coordinate[0] - coordinate0[0], coordinate[1] - coordinate0[1]).perform()
        return
    else:  # 递归，不断向着终点滑动
        step = random.randint(3, 5)
        x = int(step * (coordinate[0] - coordinate0[0]) / length)  # 按比例
        y = int(step * (coordinate[1] - coordinate0[1]) / length)
        ActionChains(browser).move_by_offset(x, y).perform()
        move(browser, coordinate, (coordinate0[0] + x, coordinate0[1] + y))


def draw(browser, ttype):
    """ 滑动 """
    if len(ttype) == 4:
        px0 = PIXELS[int(ttype[0]) - 1]
        login = browser.find_element_by_id('loginAction')
        ActionChains(browser).move_to_element(login).move_by_offset(px0[0] - login.location['x'] - int(login.size['width'] / 2), px0[1] - login.location['y'] - int(login.size['height'] / 2)).perform()
        browser.execute(Command.MOUSE_DOWN, {})

        px1 = PIXELS[int(ttype[1]) - 1]
        move(browser, (px1[0], px1[1]), px0)

        px2 = PIXELS[int(ttype[2]) - 1]
        move(browser, (px2[0], px2[1]), px1)

        px3 = PIXELS[int(ttype[3]) - 1]
        move(browser, (px3[0], px3[1]), px2)
        browser.execute(Command.MOUSE_UP, {})
    else:
        print('Sorry! Failed! Maybe you need to update the code.')

def get_cookie_from_weibo_cn(account, password):

    driver = webdriver.Chrome(os.getcwd() + '/Mac/chromedriver', chrome_options=chrome_options)
    driver.set_window_size(1050, 840)
    # driver.get('https://weibo.cn/login/')
    driver.get('https://passport.weibo.cn/signin/login?entry=mweibo&r=https://weibo.cn/。')
    time.sleep(1)

    failure = 0

    if u"微博" in driver.title and failure < 5:
        failure += 1
        driver.save_screenshot("aa.png")
        username = driver.find_element_by_id('loginName')
        username.clear()
        username.send_keys(account)
        psd = driver.find_element_by_xpath('//input[@type="password"]')
        psd.clear()
        psd.send_keys(password)
        commit = driver.find_element_by_id('loginAction')
        commit.click()
        ttype = getType_similirity(driver)

    return
    # while u"微博" in driver.title and failure < 5:
    #     failure += 1
    #     driver.save_screenshot("aa.png")
    #     username = driver.find_element_by_id('loginName')
    #     username.clear()
    #     username.send_keys(account)
    #
    #     psd = driver.find_element_by_xpath('//input[@type="password"]')
    #     psd.clear()
    #     psd.send_keys(password)
    #
    #     commit = driver.find_element_by_id('loginAction')
    #     commit.click()
    #
    #     ttype = getType(driver)
    #     print 'Result: %s!' % ttype
    #     draw(driver, ttype)  # 滑动破解
    #     time.sleep(10)
    #     return
    #     try:
    #         title = driver.find_element_by_class_name('patt-holder-header-title').text
    #         if u'安全验证' in title:
    #             ttype = getType_similirity(driver)
    #             print 'Result: %s!' % ttype
    #             draw(driver, ttype)  # 滑动破解
    #             time.sleep(10)
    #         else:
    #             pass
    #     except:
    #         # 图片验证码
    #         try:
    #             code = driver.find_element_by_name("code")
    #             code.clear()
    #             if IDENTIFY == 1:
    #                 code_txt = raw_input("请查看路径下新生成的aa.png，然后输入验证码:")  # 手动输入验证码
    #             else:
    #                 from PIL import Image
    #                 img = driver.find_element_by_xpath('//form[@method="post"]/div/img[@alt="请打开图片显示"]')
    #                 x = img.location["x"]
    #                 y = img.location["y"]
    #                 im = Image.open("aa.png")
    #                 im.crop((x, y, 100 + x, y + 22)).save("ab.png")  # 剪切出验证码
    #                 code_txt = identify()  # 验证码打码平台识别
    #             code.send_keys(code_txt)
    #         except Exception, e:
    #             pass
    #
    #     time.sleep(3)
    #     if u"我的首页" not in driver.title:
    #         time.sleep(4)
    #     if u'未激活微博' in driver.page_source:
    #         print '账号未开通微博'
    #         return {}
    #
    # cookie = {}
    # if u"我的首页" in driver.title:
    #     for elem in driver.get_cookies():
    #         cookie[elem["name"]] = elem["value"]
    # return json.dumps(cookie)

if __name__=='__main__':

    # for img in images:
    #     print img
    # exit()
    # quit()

    for weibo in myWeiBo:
        while True:
            get_cookie_from_weibo_cn(weibo[0], weibo[1])
            time.sleep(10)
