# -*- coding:utf-8 -*- 
import requests
from lxml import etree
import re
from urllib.request import urlretrieve
#获取视频ID
#拼接完整url
#获取视频播放地址
#下载视频

def download():
	url = 'http://www.pearvideo.com/category_9'
	#获取源代码
	#html = requests.get(url)
	html = requests.get(url).text
	#把文本文件处理成可解释的对象
	#如果我用正则可以不可以也可以
	html = etree.HTML(html)
	video_id = html.xpath('//div[@class="vervideo-bd"]/a/@href')
	video_url = []
	starurl = 'http://www.pearvideo.com'
	#完整拼接url
	for id in video_id:
		newurl = starurl + '/' + id
		video_url.append(newurl)
	#获取视频播放地址
	for playurl in video_url:
		#获取页面源代码
		html = requests.get(playurl).text
		#print(playurl)
		req = 'srcUrl="(.*?)"'
		#视频真正播放地址
		purl = re.findall(req,html)
		#print(purl)
		#获取视频名称
		req = '<h1 class="video-tt">(.*?)</h1>'
		pname = re.findall(req,html)
		print("正在下载:%s"%pname)

		urlretrieve(purl[0],'./video/%s.mp4'%pname[0])
download()
'''
def downloadmore():
	n = 12
	while True:
		if n > 48:
			return
		url = "http://www.pearvideo.com/category_loading.jsp?reqType=5&categoryId=9&star=%d"%n
		n+=12
		download(url)
downloadmore()
'''