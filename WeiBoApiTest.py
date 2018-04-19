#!
# coding=utf-8
import sys
import urllib2, requests, time

reload(sys)
sys.setdefaultencoding('utf8')
from weibo import APIClient
import weibo
import webbrowser  # python内置的包

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

url = 'https://c.api.weibo.com/2/statuses/upload/biz.json'
utext = unicode('测试发微博'.encode('utf-8'), 'UTF-8')
data = {'access_token': access_token,'status': utext}
# r = vipClient.post(url,data=data)
r = requests.post(url,data=data)

def weibo_post(client ,text, imgs=[], url=False):
		url_post_pic = "https://upload.api.weibo.com/2/statuses/share.json"
		utext = unicode(text.encode('utf-8'), 'UTF-8')
		try:
			if not imgs:
				client.post.statuses__share(access_token=access_token, status=utext)
			else:
				for i, img in enumerate(imgs):
					if url:
						res = urllib2.urlopen(img)
						cat_img = res.read()
						img = '%d.png' % i
						with open(img, 'weibo') as f:
							f.write(cat_img)

					s_text = utext

					if len(imgs) > 1:
						s_text = str(i + 1) + s_text
					data = {
						'access_token': access_token,
						'status': s_text,
					}
					files = [
						('pic', open(img, 'rb'))
					]
					# print files, s_text
					r = requests.post(url_post_pic, data=data, files=files)
					time.sleep(5.0)
		except weibo.APIError, e:
			if e.error_code == 20012:
				if text.startswith('Text too long'):
					raise
				t_split = text.split()
				t_split = [t for t in t_split if t.startswith('http')]
				text = ''.join(['Text too long', t_split[-1]]) + ' '
				weibo_post(text, imgs, url)
			else:
				raise


weibo_post(vipClient, '测试发微博啊啊啊啊')

# 可以打印下看看里面都有什么东西
# print client.statuses__public_timeline()
# statuses = client.statuses__public_timeline()['statuses']
# statuses = vipClient.statuses.user_timeline_batch.get(uids=1749964961)
#
# length = len(statuses)
# # 输出了部分信息
# for i in range(0, length):
#     print '昵称：' + statuses[i]['user']['screen_name']
#     print '简介：' + statuses[i]['user']['description']
#     print '位置：' + statuses[i]['user']['location']
#     print '微博：' + statuses[i]['text']
#     if statuses[i].has_key('original_pic'):
#         print '微博：' + statuses[i]['original_pic']