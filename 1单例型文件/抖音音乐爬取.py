# -*- coding:utf-8 -*-
"""
#Python学习交流群：125240963，群内每天分享干货，包括最新的python企业案例学习资料和零基础入门教程，欢迎各位小伙伴入群学习交流
"""
from contextlib import closing
import requests, json, time, re, os, sys, time

class douyin(object):
	"""docstring for douyin"""
	def __init__(self):
		super(douyin, self).__init__()
		self.headers = {
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'zh-CN,zh;q=0.9',
			'cache-control': 'max-age=0',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3',
		}

	def get_music_urls(self,mc_id):
		music_names = []
		music_urls = []
		user_url = 'https://api.amemv.com/aweme/v1/music/list/?iid=34451996099&device_id=52982221132&os_api=18&app_name=aweme&channel=App%20Store&idfa=00000000-0000-0000-0000-000000000000&device_platform=iphone&build_number=18504&vid=386F3505-7B99-444A-845A-E5EEA12C5936&openudid=e01e26ddeb822fd95f6599de43b7547cfe1a26ea&device_type=iPhone7,2&app_version=1.8.5&version_code=1.8.5&os_version=11.3&screen_width=750&aid=1128&ac=WIFI&cursor=0&mc_id='+str(mc_id)
		req = requests.get(user_url, headers=self.headers)
		html = json.loads(req.text)
		for each in html['music_list']:
			share_desc = each['title']
			music_names.append(share_desc + '.mp3')
			music_urls.append(each['play_url']['uri'])
		return music_names, music_urls

		
		
		

	def music_downloader(self, music_url,music_name):
		"""
		下载
		"""
		size = 0
		with closing(requests.get(music_url, headers=self.headers, stream=True)) as response:
			chunk_size = 1024
			content_size = int(response.headers['content-length']) 
			if response.status_code == 200:
				sys.stdout.write('  [文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))
				with open(music_name, "wb") as file:  
					for data in response.iter_content(chunk_size = chunk_size):
						file.write(data)
						size += len(data)
						file.flush()
						sys.stdout.write('  [下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
						sys.stdout.flush()



	def run(self):
		"""
		运行函数   
		Parameters:
			None
		Returns:
			None
		"""
		mc_id=0

		music_url_list='https://api.amemv.com/aweme/v1/music/collection/?iid=34451996099&device_id=52982221132&os_api=18&app_name=aweme&channel=App%20Store&idfa=00000000-0000-0000-0000-000000000000&device_platform=iphone&build_number=18504&vid=386F3505-7B99-444A-845A-E5EEA12C5936&openudid=e01e26ddeb822fd95f6599de43b7547cfe1a26ea&device_type=iPhone7,2&app_version=1.8.5&version_code=1.8.5&os_version=11.3&screen_width=750&aid=1128&ac=WIFI&mas=00dfe1ffff8907b970da90b3e7cf26a0ff84e922cf91ee92e768de&as=a12522c184a0fb66257265&ts=1528112644'
		collection = requests.get(music_url_list, headers=self.headers)
		js_collection=json.loads(collection.text)
		for mc in js_collection['mc_list']:
			mc_id=mc['id']
			mc_name=mc['mc_name']
			music_names, music_urls = self.get_music_urls(mc_id)
			#print(mc_name)
			if mc_name not in os.listdir('/Users/admin/Desktop/'):
				os.mkdir(mc_name)
			print('下载中:共有%d个作品!\n' % len(music_urls))
			for num in range(len(music_urls)):
				if '\\' in music_names[num]:
					music_name = music_names[num].replace('\\', '')
				elif '/' in music_names[num]:
					music_name = music_names[num].replace('/', '')
				else:
					music_name = music_names[num]
				if os.path.isfile(os.path.join(mc_name, music_name)):
					print('%s 已存在' % mc_name)
				else:
					self.music_downloader(music_urls[num], os.path.join(mc_name, music_name))
				print('\n')
		print('下载完成!')

if __name__ == '__main__':
	douyin = douyin()
	douyin.run()