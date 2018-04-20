#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import requests, json, urllib2
import weibo
from weibo import APIClient
import time
import webbrowser


class weibo_tool(object):
    api_key = "2517952414"
    api_secret = "1b5cbde6c1689409c9372c1b153e5a7e"
    callback_url = "http://dev.guanba.com/article/hot"
    access_token = "2.00QBWS1Gi8E6kC9374805e8aKs49TE"
    expires_in = 36000

    def weibo_init(self):
        # 初始化微博API
        print 'weibo init!'
        client = APIClient(app_key=self.api_key, app_secret=self.api_secret, redirect_uri=self.callback_url)
        # client.get_authorize_url()
        # referer_url = client.get_authorize_url()
        # print referer_url
        # code = raw_input("Input code:")
        # r = client.request_access_token(code)
        # access_token = r.access_token
        # expires_in = r.expires_in

        client.set_access_token(self.access_token, self.expires_in)
        self.client = client

    def weibo_post(self, text, imgs=[], url=False):
        url_post_pic = "https://c.api.weibo.com/2/statuses/upload/biz.json"
        utext = unicode(text.encode('utf-8'), 'UTF-8')
        data = {'access_token': self.access_token,'status': utext}
        r = requests.post(url_post_pic,data=data)
        print(r)


# try:
# 	if not imgs:
# 		self.client.post.statuses__share(access_token=self.access_token, status=utext)
# 	else:
# 		for i, img in enumerate(imgs):
# 			if url:
# 				res = urllib2.urlopen(img)
# 				cat_img = res.read()
# 				img = '%d.png' % i
# 				with open(img, 'weibo') as f:
# 					f.write(cat_img)
#
# 			s_text = utext
#
# 			if len(imgs) > 1:
# 				s_text = str(i + 1) + s_text
# 			data = {
# 				'access_token': self.access_token,
# 				'status': s_text,
# 			}
# 			files = [
# 				('pic', open(img, 'rb'))
# 			]
# 			# print files, s_text
# 			r = requests.post(url_post_pic, data=data, files=files)
# 			time.sleep(5.0)
# except weibo.APIError, e:
# 	if e.error_code == 20012:
# 		if text.startswith('Text too long'):
# 			raise
# 		t_split = text.split()
# 		t_split = [t for t in t_split if t.startswith('http')]
# 		text = ''.join(['Text too long', t_split[-1]]) + ' '
# 		self.weibo_post(text, imgs, url)
# 	else:
# 		raise


if __name__ == '__main__':
    wb = weibo_tool()
    wb.weibo_init()
    wb.weibo_post('aaa')
    pass