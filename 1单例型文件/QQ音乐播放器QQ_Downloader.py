# QQ音乐下载器
#源码加微信：mmp9972
import requests
import os
import time
import re
import urllib


class Downloader():
	def __init__(self):
		self.headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
					}
		self.search_url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.top&searchid=34725291680541638&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w={}&g_tk=5381&jsonpCallback=MusicJsonCallback703296236531272&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
		self.fcg_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&jsonpCallback=MusicJsonCallback9239412173137234&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&callback=MusicJsonCallback9239412173137234&uin=0&songmid={}&filename={}.m4a&guid=8208467632'
		self.downloader_url = 'http://dl.stream.qqmusic.qq.com/{}.m4a?vkey={}&guid=8208467632&uin=0&fromtag=66'
	def run(self, keyword, num=1):
		# Step1
		# 根据歌名搜索，获取所需的信息
		print('[INFO]:Searching...')
		res = requests.get(self.search_url.format(keyword), headers=self.headers).text
		# media_mid
		media_mid_temp = re.findall('"media_mid":"(.*?)"', res)
		media_mid = []
		for i in range(len(media_mid_temp)):
			media_mid.append('C400'+media_mid_temp[i])
		# songmid
		songmid = re.findall('"lyric_hilight":".*?","mid":"(.*?)","mv"', res)
		# singer
		singer_temp = re.findall('"singer":\[.*?\]', res)
		singer = []
		for s in singer_temp:
			singer.append(re.findall('"name":"(.*?)"', s)[0])
		# songname
		songname = re.findall('},"name":"(.*?)","newStatus"', res)
		# Step2
		# 获取下载地址
		print('[INFO]:Parsing download url...')
		urls = []
		del_idex = []
		songname_keep = []
		singer_keep = []
		for m in range(len(media_mid)):
			try:
				fcg_res = requests.get(self.fcg_url.format(songmid[m], media_mid[m]), headers=self.headers)
				vkey = re.findall('"vkey":"(.*?)"', fcg_res.text)[0]
				urls.append(self.downloader_url.format(media_mid[m], vkey))
				songname_keep.append(songname[m])
				singer_keep.append(singer[m])
			except:
				print('[Warning]:One song lost...')
			time.sleep(0.5)
		# Step3
		# 下载歌曲
		print('[INFO]:Start downloading...')
		if num > len(urls):
			print('[Warning]:Only find %d songs...' % len(urls))
			num = len(urls)
		if not os.path.exists('./results'):
			os.mkdir('./results')
		for n in range(num):
			print('[INFO]:Downloading %dth song...' % (n+1))
			filepath = './results/{}'.format(songname_keep[n].replace("\\", "").replace("/", "").replace(" ", "")+'_'+singer_keep[n].replace("\\", "").replace("/", "").replace(" ", "")+'.m4a')
			urllib.request.urlretrieve(urls[n], filepath)
		print('[INFO]:All done...')



if __name__ == '__main__':
	while True:
		print('[INFO]:QQ music Downloader...')
		print('[Author]:Charles')
		keyword = input('Enter the SongName:')
		songnum = input('Enter the num you want to download:')
		try:
			songnum = int(songnum)
		except:
			continue
		dl = Downloader()
		dl.run(keyword, songnum)
