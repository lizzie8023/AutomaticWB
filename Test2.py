#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#   微博登录方式2
import requests
import time
from sqlalchemy.orm import sessionmaker


class WeiBo(object):

    login_success = False

    def __init__(self, username, password):
        self.s = requests.session()
        proxies = {
            "http":"119.57.112.130:8080",
            "https":"114.245.152.189:8118"
        }
        # self.s.proxies.update(proxies)
        self.login_headers = {'Host': 'passport.weibo.cn',
                              'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0',
                              'Accept': '*/*',
                              'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                              'Accept-Encoding': 'gzip, deflate',
                              'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F',
                              'Content-Type': 'application/x-www-form-urlencoded',
                              'Connection': 'close'}
        self.headers = {'Host': 'm.weibo.cn',
                        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0',
                        'Accept': 'application/json, text/plain, */*',
                        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate',
                        'Referer': 'https://m.weibo.cn',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Connection': 'close'}
        self.username = username
        self.login_data = {
            'username': username,
            'password': password,
            'savestate': 1,
            'r': 'http%3A%2F%2Fm.weibo.cn%2F',
            'ec': 0,
            'pagerefer': '',
            'entry': 'mweibo',
            'wentry': '',
            'loginfrom': '',
            'client_id': '',
            'code': '',
            'qq': '',
            'mainpageflag': 1,
            'hff': '',
            'hfp': ''}
        self.cookies = self.verify_cookie()

    def login(self):
        url = 'https://passport.weibo.cn/sso/login'
        r = self.s.post(url, headers=self.login_headers, data=self.login_data)
        if r.json()['retcode'] == 20000000:
            print('登录成功')
            self.save_cookie(r.headers['Set-Cookie'])
            login_success = True
            return r.headers['Set-Cookie']
        else:
            print(r.json())
            print('登录失败，尝试重新登录')
            return None

    def save_cookie(self, cookie):
        with open('cookies/%s.txt' % self.username, 'w') as f:
            f.write(cookie)
        print('cookie保存成功')

    def get_cookie(self):
        try:
            with open('cookies/%s.txt' % self.username, 'r') as f:
                cookies = {}
                for line in f.read().split(';'):
                    name, value = line.strip().split('=', 1)  # 1代表只分割一次
                    cookies[name] = value
                return cookies
        except:
            return None

    def verify_cookie(self):

        try:
            cookies = self.get_cookie()

            if cookies is None:
                print('cookie过期或不存在')
                cookies = ''
            else:
                print('cookie获取成功，正在尝试cookie登录')

            url = 'https://m.weibo.cn'
            proxies = {
                "https": "https://114.245.152.189:8118"
            }
            r = self.s.get(url, headers=self.headers, cookies=cookies, proxies=proxies, timeout=5)
            if r.status_code == 200:
                print('登录成功')
                # print(r.text)
                login_success = True
                return cookies
            else:
                print('cookie过期,正在尝试重新登录')
                self.login()
                cookies = self.get_cookie()
                # print(cookies)
                return cookies
        except:
            print("登录失败")
            pass

        try:
            cookies = self.get_cookie()
            print('cookie获取成功，正在尝试cookie登录')
        except:
            print('cookie过期或不存在')
            cookies = ''
        url = 'https://m.weibo.cn'
        # params = {'t': str(int(time.time()))}
        r = self.s.get(url, headers=self.headers, cookies=cookies)
        if r.status_code == 200:
            print('登录成功')
            # print(r.text)
            login_success = True
            return cookies
        else:
            print('cookie过期,正在尝试重新登录')
            self.login()
            cookies = self.get_cookie()
            # print(cookies)
            return cookies

    def get_user_basic_info(self):
        url = "https://m.weibo.cn/home/me?format=cards"

        r = self.s.get(url, headers=self.headers, cookies=self.cookies)
        try:
            data = r.json()
        except Exception as e:
            print(e)
            data = None
        if not data:
            return None
        user_info = data[0]["card_group"][0]["user"]
        user = {}
        user["user_id"] = user_info["id"]
        user["user_name"] = user_info["name"]
        user["weibo_count"] = user_info["mblogNum"]
        user["follow_count"] = user_info["attNum"]
        return user

    def get_user_follows(self):
        d = self.get_user_basic_info()
        uid = d.get("user_id")
        follow_count = d.get("follow_count")
        if not uid:
            return None
        headers = self.headers
        referer = "https://m.weibo.cn/p/second?containerid=100505" + str(uid) + "_-_FOLLOWERS"
        headers["Referer"] = referer
        page = int(follow_count) // 10 + 1
        follow_list = []
        for i in range(1, int(page) + 1):
            if i == 1:
                url = "https://m.weibo.cn/api/container/getSecond?containerid=100505" + str(uid) + "_-_FOLLOWERS"
            else:
                url = "https://m.weibo.cn/api/container/getSecond?containerid=100505" + str(
                    uid) + "_-_FOLLOWERS&page=" + str(i)
            r = self.s.get(url, headers=headers, cookies=self.cookies)
            try:
                data = r.json()
            except Exception as e:
                print(e)
                data = None
            if not data:
                return None
            # print(data)
            follows = data.get("data").get("cards")  # 这里获取单页所有关注
            if not follows:
                continue

            for follow in follows:  # 遍历
                follow_tmp1 = {}  # 临时字典用来存关注的信息
                follow_tmp1["followed_weibo_id"] = follow["user"]["id"]
                follow_tmp1["followed_weibo_name"] = follow["user"]["screen_name"]
                follow_tmp1["weibo_user_id"] = uid
                tmp2 = follow_tmp1.copy()
                follow_list.append(tmp2)
            time.sleep(1)
        return follow_list

    def get_st(self):  # st是转发微博post必须的参数
        url = "https://m.weibo.cn/api/config"
        r = self.s.get(url, headers=self.headers, cookies=self.cookies)
        data = r.json()
        st = data["data"]["st"]
        return st

    def forward_weibo(self, weibo, content):
        st = self.get_st()
        url = "https://m.weibo.cn/api/statuses/repost"
        data = {"id": weibo["weibo_content_id"], "content": content, "mid": weibo["mid"], "st": st}
        r = self.s.post(url, data=data, headers=self.headers, cookies=self.cookies)
        # print(r.text)
        try:
            if r.json().get("ok") == 1:
                print("转发成功")
                return True
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def get_user_weibo(self, uid):  # 获取前十条微博
        url = "https://m.weibo.cn/api/container/getIndex?uid=" + str(uid) + "&luicode=20000174&type=uid&value=" + str(
            uid) + "&containerid=107603" + str(uid)
        r = self.s.get(url, headers=self.headers, cookies=self.cookies)
        cards = r.json().get("data").get("cards")
        weibos = []
        for card in cards:
            weibo = {}
            try:
                weibo["weibo_content_id"] = card.get("mblog").get("id")
                weibo["weibo_content"] = card.get("mblog").get("text")
                weibo["weibo_user_id"] = card.get("mblog").get("user").get("id")
                weibo["weibo_username"] = card.get("mblog").get("user").get("screen_name")
                weibo["mid"] = card.get("mblog").get("mid")
            except AttributeError:
                continue  # cards列表里面不一定是微博，用try来过滤
            tmp = weibo.copy()
            weibos.append(tmp)
        return weibos

    def original_weibo(self, content, pic_id=None):
        st = self.get_st()
        data = {
            "luicode": "10000011",
            "lfid": "2304135827525376_ - _WEIBO_SECOND_PROFILE_MORE_WEIBO",
            "featurecode": "20000320",
            "content": content,
            "st": st}
        if pic_id:
            data["picId"] = pic_id
        url = "https://m.weibo.cn/api/statuses/update"
        r = self.s.post(url, data=data, headers=self.headers, cookies=self.cookies)
        try:
            if r.json()["ok"] == 1:
                print("发送成功")
            else:
                print("发送失败")
        except Exception as e:
            print(e)
            return None

    def upload_pic(self, pic_path):
        headers = self.headers
        headers.pop("Content-Type")  # 这里删除content-type让requests自己生成
        url = "https://m.weibo.cn/api/statuses/uploadPic"
        st = self.get_st()
        try:
            files = {"pic": (pic_path, open(pic_path, "rb").read(), "image/jpeg")}
        except Exception:
            return None
        data = {"type": "json", "st": st}
        r = self.s.post(url, data=data, files=files, headers=self.headers, cookies=self.cookies)
        try:
            pic_id = r.json()["pic_id"]
            print("图片上传成功")
            return pic_id
        except Exception as e:
            print(e)
            return None


if __name__ == '__main__':

    username = "zezhi7751@sina.cn"
    password = "hai456123"
    while True:
        weibo = WeiBo(username=username, password=password)
        weibo.original_weibo("中兴今天破产没?中兴今天倒闭没?")
        time.sleep(60 * 60 * 24)
