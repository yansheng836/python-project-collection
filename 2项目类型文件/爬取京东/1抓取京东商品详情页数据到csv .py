# 爬取京东商品详情页信息
import requests
from bs4 import BeautifulSoup
import os  #os模块包含普遍的操作系统功能
import csv
import re
import json
import time

# 爬取页面链接
def make_a_link(keyword, page):
    try:
        url='https://search.jd.com/Search?keyword='+ keyword + '&enc=utf-8&page=' + str(2 * page - 1)
        r = requests.get(url)
        #如果状态码是40X或者50X，那么可以使用Response.raise_for_status()抛出一下异常
        # 如果是返回200，则raise_for_status()并不会抛出异常。
        r.raise_for_status
        print('正在爬取第{}页...'.format(page))
        print('---' * 45)
        r.encoding = 'gbk'
        print(url)
        return r.text
    except:
        print('链接错误！！！')
        return ''
#查找每件商品的页面链接
def find_only_link(html):
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all('div', class_='gl-i-wrap')
    return (link.find('div', class_='p-name p-name-type-2').a['href'] for link in links)  # 页面链接的生成表达式
# 链接单页面
def link_to_url(link):
    try:
        r = requests.get(link)
        r.raise_for_status
        r.encoding = 'gbk'
        return r.text
    except:
        print('此页无法链接！！！')
        return ''
 # 爬取商品价格
def getprice(purl):
    uid = re.match(r'.+?(\d+).+', purl).group(1)
    content = link_to_url('https://p.3.cn/prices/mgets?skuIds=J_' + uid)
    jd = json.loads(content.lstrip('[').rstrip(']\n'))  # 生成json数据格式
    return jd['p']
# 爬取商品评论
def getcomment(purl):
    uid = re.match(r'.+?(\d+).+', purl).group(1)
    content = link_to_url('https://club.jd.com/comment/productCommentSummaries.action?referenceIds=' + uid)
    jd = json.loads(content)
    comment = []
    jds = jd['CommentsCount'][0]
    comment.append(jds['CommentCountStr'])  # 评论数
    comment.append(jds['GoodCountStr'])  # 好评数
    comment.append(jds['GoodRate'])  # 好评率
    return comment
# 爬取商品名称
def getname(purl):
    uid = re.match(r'.+?(\d+).+', purl).group(1)
    content = link_to_url('https://c.3.cn/recommend?&methods=accessories&sku=' + uid + '&cat=9987%2C653%2C655')
    try:
        jd = json.loads(content)
        return jd['accessories']['data']['wName']
    except:
        return ''
 # 爬取卖家
def getseller(purl):
    uid = re.match(r'.+?(\d+).+', purl).group(1)
    content = link_to_url('https://chat1.jd.com/api/checkChat?pid=' + uid + '&returnCharset=utf-8')
    try:
        jd = json.loads(content.lstrip('null(').rstrip(');'))
        try:
            return jd['seller']
        except:
            return ''
    except:
        ''
  # 保存到csv
def save_to_csv(ulist, keyword):
    path = 'F:/Python代码/爬虫/'   #路径
    # if not os.path.exists(path):  #是否存在该目录
    #     os.mkdir(path)  #创建目录
    with open(path + '京东' + keyword + '数据.csv', 'w+') as f:
        writer = csv.writer(f)   #写入csv
        writer.writerow(['商品', '价格', '店铺', '链接', '评论数', '好评数', '好评率'])
        for i in range(len(ulist)):
            if ulist[i] and ulist[i][0]:
                writer.writerow(
                    [ulist[i][0], ulist[i][1], ulist[i][2], ulist[i][3], ulist[i][4], ulist[i][5], ulist[i][6]])
                # 主函数
def relmain(keyword):  # 高阶函数
    def main(page):
        r = re.compile(r'.*?html')
        ulist = []
        for p in range(page):
            p += 1
            text = make_a_link(keyword, p)
            for url in find_only_link(text):
                ul = []
                if r.match(url):
                    if getname(url):
                        ul.append(getname(url))  # 商品名称
                        ul.append(getprice(url))  # 价格
                        ul.append(getseller(url))  # 店铺
                        ul.append('https:' + url)  # 链接
                        ul.extend(getcomment(url))  # 评论
                ulist.append(ul)  #列表中含有列表  可以看做是二维数组
        save_to_csv(ulist, keyword)
    return main

if __name__ == '__main__':
    keyword = input('输入要爬取的商品：')
    pages = int(input('输入要爬取的页数：'))
    time_start = time.time()
    relmain(keyword)(pages)
    print('耗时{}秒。'.format(time.time() - time_start))  # 爬取所需时间