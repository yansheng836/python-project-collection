# -*- coding: utf-8 -*-
# 爬取美女网站
import requests
import os
import time
from bs4 import BeautifulSoup

class MeiNv:
    def __init__(self,path):
        self.filePath = path
        self.headers = {"user-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"}

    # 发起request请求
    def doRequest(self, url):
        html = requests.get(url, headers = self.headers)
        return html.text
    # 得到图片的信息
    def doSoup(self, content):
        con_soup = BeautifulSoup(content, 'lxml')
        a_list = con_soup.find("div", class_="all").find_all('a')
        for item in a_list:
            # 连接名字，作为文件夹名字
            title = item.get_text()
            self.mkdir(title)
            # 取出值中的图片位置
            page = item['href']
            page_html = self.doRequest(page)
            # 匹配图片的数目
            html_soup = BeautifulSoup(page_html,'lxml')
            max_span = html_soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
            for i in range(1,int(max_span)+1):
                time.sleep(1)
                page_url = page + '/' + str(i)
                # 读取图片的信息
                img_html = self.doRequest(page_url)
                imghtml_soup = BeautifulSoup(img_html, 'lxml')
                img_url = imghtml_soup.find('div', class_ = 'main-image').find('img')['src']
                name = img_url[-9:-4]
                img = requests.get(img_url, headers = self.headers)
                self.writeToFile(name, img.content)
    # 将图片信息写入文件中
    def writeToFile(self, filename, content):
        f = open(filename+'.jpg','wb')
        f.write(content)
        f.close()

    # 创建目录
    def mkdir(self, path):
        path = path.strip()
        isEXists = os.path.exists(os.path.join("F:\\大Python\\学习代码专用\\文章代码\\网易云", path))
        if not isEXists:
            print (u'创建了一个名为%s的文件夹'%(path))
            os.makedirs(os.path.join(self.filePath, path))
            os.chdir(os.path.join(self.filePath, path))
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False

    def start(self, url):
        content = self.doRequest(url)
        contents = self.doSoup(content)
        self.writeToFile(contents)
        # print content

url = "http://www.mzitu.com/all"
path = "F:\\大Python\\学习代码专用\\文章代码\\网易云"
meinv = MeiNv(path)
meinv.start(url)




