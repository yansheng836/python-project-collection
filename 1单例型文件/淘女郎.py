# -*- coding: utf-8 -*-
# 抓取淘宝淘女郎图册
 
from selenium import webdriver
import re
import os
import urllib.request
import requests
 
def get_page_source(url, path):
	print('正在获取 %s 的源码数据' % url)
	driver = webdriver.PhantomJS()
	driver.get(url)
	html = driver.page_source
	driver.quit()
	with open(path + 'souce_code.txt', 'w', encoding='utf-8') as f:
		f.write(html)
	print('源码数据获取完成')
	return html
 
def get_mm_dict_list(html, path):
	print('正在获取主页面中MM列表数据')
	reg_mm_name = re.compile(r'class=\"name\">(.*?)</span>')
	reg_mm_city = re.compile(r'class=\"city\">(.*?)</span>')
	reg_mm_height = re.compile(r'<span>(.*?)&nbsp;')
	reg_mm_weight = re.compile(r'/&nbsp;(.*?)</span>')
	reg_mm_url = re.compile(r'<a href=\"(//mm.taobao.com/self/.*?)\"')
	mm_name_list = reg_mm_name.findall(html)
	mm_city_list = reg_mm_city.findall(html)
	mm_height_list = reg_mm_height.findall(html)
	mm_weight_list = reg_mm_weight.findall(html)
	mm_url_list = reg_mm_url.findall(html)
	dict_key = ['name', 'city', 'height', 'weight', 'url']
	mm_dict_list = []
	if len(mm_name_list) == len(mm_city_list) == len(mm_height_list) == len(mm_weight_list) == len(mm_url_list):
		mm_list = zip(mm_name_list, mm_city_list, mm_height_list, mm_weight_list, mm_url_list)
	for i in list(mm_list):
		mm_dict = dict(zip(dict_key, i))
		mm_dict_list.append(mm_dict)
	with open(path + 'mm_list.txt', 'w', encoding='utf-8') as f:
		text = '%s' % mm_dict_list
		f.write(text)
	print('%s 个MM列表数据获取完成' % len(mm_dict_list))
	return mm_dict_list
 
def set_path(path_name):
	path = 'F:\\%s\\' % path_name
	print('正在设置保存路径为：', path)
	if os.path.isdir(path):
		return path
	else:
		os.mkdir(path)
		return path
 
def get_mm_img(path, mm_dict_list):
	for i in range(len(mm_dict_list)):
		mm_path = path + mm_dict_list[i]['name'] + ' ' + mm_dict_list[i]['city'] + ' ' + mm_dict_list[i]['height'] + ' ' + mm_dict_list[i]['weight'] +'\\'
		print('正在设置保存路径为：', mm_path)
		if os.path.isdir(mm_path):
			mm_path = mm_path
		else:
			os.mkdir(mm_path)
			mm_path = mm_path
		mm_page_source = get_page_source('https:' + mm_dict_list[i]['url'], mm_path)
		print('正在获取 %s 的图片数据' % mm_dict_list[i]['name'])
		reg_img = re.compile(r'(//img.alicdn.com/imgextra/.*?)\"')
		mm_img_list = reg_img.findall(mm_page_source)
		n = 0
		with open(mm_path + 'mm_img_list.txt', 'w', encoding='utf-8') as f:
			text = '%s' % mm_img_list
			f.write(text)
		for j in mm_img_list:
			n += 1
			response = requests.get('https:' + j)
			if response.status_code == 200:
				print('正在下载 %s 的第 %d 张图片:%s' % (mm_dict_list[i]['name'], n, j))
				url = 'https:' + j
				urllib.request.urlretrieve(url, '%s%s.%s' %(mm_path, n, j[-3:]))
			else:
				print('下载 %s 的第 %d 张图片失败:%s' % (mm_dict_list[i]['name'], n, j))
 
def main():
	url = 'https://mm.taobao.com/search_tstar_model.htm'
	path = set_path('淘宝MM')
	index_source = get_page_source(url, path)
	mm_dict_list = get_mm_dict_list(index_source, path)
	get_mm_img(path, mm_dict_list)
 
if __name__ == '__main__':
	main()