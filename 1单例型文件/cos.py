import re
import requests
from pyquery import PyQuery as pq
import time
from urllib.parse import urlencode

Filepath='cosplay' #目录文件名 可以修改 注意不要含有"/"

def get_html(url):
    proxies = {"https": "https://183.129.207.73:14823", "https": "https://114.215.95.188:3128", }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    getweb = requests.get(str(url),headers=headers,proxies=proxies)
    try:
        return getweb.text
    except Exception as e:
        print(e)
    except IOError as e1:
        print(e1)

def DownloadFileWithFilename(url,filename,path):
    import requests
    import os
    import re
    try:
        if not os.path.exists(path):
            os.mkdir(path)
        if not os.path.exists(path):
            r = requests.get(url)
        r = requests.get(url)
        with open(str(path) + "/"+str(filename), "wb") as code:
            code.write(r.content)
            print('Downloaded!',str(path) + "/"+str(filename))
    except IOError as e:
        print("Download Failed!")
        print(e)
    except Exception as e1:
        print(e1)
        print("Download Failed!")


def getStaticHtmlImage(): #获取没有AJAX更新时网页的COSPLAY图片
    global Filepath
    web_static_state='https://bcy.net/coser'
    doc = pq(web_static_state)
    image = doc('li.js-smallCards._box a.db.posr.ovf img.cardImage').items()

    for i in image:  # 爬取ajax网页数据
        i = str(i.attr('src')).rstrip('/2X3')  # 这里的i是把获取的URL最后一段/2x3去除
        filename = str(re.search('[^/]+(?!.*/)', i).group(0))  # filename是URL的最后一段:xxx.jpg
        i2 = i + str('/w650')  # i2是高清图片URL:xxxxx/w650
        DownloadFileWithFilename(i2, filename, Filepath)
        time.sleep(3) #休眠三秒 防止封IP

def getDynamicHtmlImage(since1): #获取ajax更新数据的COSPLAY图片
    global Filepath
    ajax_get_data = {
        'since':since1,
        'grid_type':'flow',
        'sort':'hot',
        'tag_id':'399',
    }

    proxies = {"https": "https://183.129.207.73:14823", "https": "https://114.215.95.188:3128", }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

    web_dynamic = requests.get('https://bcy.net/circle/timeline/showtag?'+urlencode(ajax_get_data),headers=headers, proxies=proxies).text
    doc = pq(web_dynamic)
    image = doc('li.js-smallCards._box a.db.posr.ovf img.cardImage').items()

    for i in image:  # 爬取ajax网页数据
        i = str(i.attr('src')).rstrip('/2X3')  # 这里的i是把获取的URL最后一段/2x3去除
        filename = str(re.search('[^/]+(?!.*/)', i).group(0))  # filename是URL的最后一段:xxx.jpg
        i2 = i + str('/w650')  # i2是高清图片URL:xxxxx/w650
        DownloadFileWithFilename(i2, filename, Filepath)
        time.sleep(3) #休眠三秒 防止封IP

getStaticHtmlImage()

list_since = ['25861.565','25861.523','25861.483','25861.428'] #ajax请求的since

for i in list_since:
    print(i)
    getDynamicHtmlImage(i)