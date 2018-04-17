#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests
import re
class Weibo(object):
    '''
    新浪微博类
    '''
    def __init__(self, username, password):
        '''
        借助移动端进行登录
        '''
        #user,password用户名密码,使用自己注册的sina用户名密码
        self.username = username
        self.password = password
        self.session = requests.Session()
        # proxies = {
        #     "https": "60.190.199.68:808"
        # }
        # self.session.proxies.update(proxies)
        self._login()
    def _login(self):
        #登录地址
        url_login = r"https://passport.weibo.cn/sso/login" # 是的，这就是移动端的登录地址
        headers = { # 这个请求头一定要有，否则会失败
            "Host": "passport.weibo.cn",
            "Connection": "keep-alive",
            "Origin": "https://passport.weibo.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Referer": "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F",
            "Accept-Language": "zh-CN,zh;q=0.8",}
        postdata = {
            "username" : self.username,
            "password" : self.password,
            "savestate" : "1",
            "ec" : "0",
            "pagerefer" : "https%3A%2F%2Fpassport.weibo.cn%2Fsignin%2Fwelcome%3Fentry%3Dmweibo%26r%3Dhttp%253A%252F%252Fm.weibo.cn%252F%26wm%3D3349%26vt%3D4",
            "entry" : "mweibo", #我猜，这里是mobile weibo的意思，表明登录是来自移动端
            "wentry" : "",
            "loginfrom" : "",
            "client_id" : "",
            "code" : "",
            "qq" : "",
            "hff" : "",
            "hfp" : "",
        }

        resp = self.session.post(url_login,data=postdata,headers=headers).json()
        self.uid = resp['data']['uid'] #保存用户id
        for url in resp['data']['crossdomainlist'].values(): # 响应中返回的domainlist每个要请求一下，否则登录不完整
            if not url.startswith("http:") and not url.startswith("https:"): url = "http:" + url
            self.session.get(url)
        self.session.get("https://m.weibo.cn/")

    def add_new(self, content):
        '''
        create a new weibo发布新微博方法
        '''
        addurl = "https://m.weibo.cn/mblogDeal/addAMblog"
        st = re.findall(r'"st":"(\w+)"', self.session.get(r"http://m.weibo.cn/mblog").text)
        # 如果发送数据中有一些值为数字字母等混合的长得像随机数的参数，
        # 建议可以在页面源代码里找找，然后用正则表达式提取出来。就像这里的st
        data = {'content': content, 'st': st[0], }
        headers = {  # headers也是必不可少的，否则会有什么安全问题导致发送失败
            "Host": "m.weibo.cn",
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Origin": "http://m.weibo.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "http://m.weibo.cn/mblog",
            "Accept-Language": "zh-CN,zh;q=0.8"
        }
        respon = self.session.post(addurl, data, headers=headers).json()
        return respon.get("msg", "Unknow Error")  # 这里的msg是发布结果



if __name__=='__main__':
    wb = Weibo(username="zezhi7751@sina.cn",password="hai456123")
    wb.add_new("测试一下啊啊啊啊")