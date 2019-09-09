# -*- coding:utf-8 -*-

import requests
import re
import json
#获取JS源代码  获取英雄的ID
#拼接URL地址
#获取下载图片的地址
#下载图片

#驼峰命名法
#获取英雄图片
def getLOLImages():
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'}
	url_js = 'http://lol.qq.com/biz/hero/champion.js'
	#获取JS源代码 str bytrs字节
	res_js = requests.get(url_js).content
	#转码
	html_js = res_js.decode()
	#正则表达
	req = '"keys":(.*?),"data"'
	list_js = re.findall(req,html_js)
	#print(list_js[0])
	# str → dict
	dict_js = json.loads(list_js[0])
	#print(dict_js)
	#定义图片列表
	pic_list = []
	for key in dict_js:
		#print(key)
		for i in range(20):
			num = str(i)
			if len(num) == 1:
				hreo_num = "00"+num
			elif len(num) == 2:
				hreo_num = "0"+num
			numstr = key+hreo_num
			url = "http://ossweb-img.qq.com/images/lol/web201310/skin/big"+numstr+".jpg"
			#print(url)
			pic_list.append(url)

			list_filepath = []
			path = "E:\\文章\\LOL官网\LOLpic\\"
			#print(dict_js.values())
			for name in dict_js.values():
				for i in range(20):
					file_path = path + name + str(i) + '.jpg'
					list_filepath.append(file_path)
					#print(list_filepath)
	n = 0				
	for picurl in pic_list:
		res = requests.get(picurl)
		n+=1

		if res.status_code ==200:
			
			print("正在下载%s"%list_filepath[n])
			#time.sleep(1)
			with open(list_filepath[n],'wb') as f:
				f.write(res.content)






getLOLImages()

