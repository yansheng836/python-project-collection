# 第一步：导入第三方包
import requests
from lxml import etree

#第二步：获取目标网页
def _get(url):
    # 2.2设置简单的反爬虫机制
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5221.400 QQBrowser/10.0.1125.400'}
    # 2.3 请求目标网页，拿取爬取网页的内容，并保存内容
    response = requests.get(url, headers=headers)
    # 2.4 返回获得网页
    return response.text
#Python学习交流群：125240963，群内每天分享干货，包括最新的python企业案例学习资料和零基础入门教程，欢迎各位小伙伴入群学习交流
# 第三步：抓取网页中图片的url地址
def html(text):

    # 3.2 将获取的网页保存在html对象里，便于解析拿取数据
    html = etree.HTML(text)
    # 3.3 分析页面的结构，获取图片的url地址，并返回图片的url地址
    img_urls = html.xpath("//div[@class='main-content']//img/@src")
    # 3.4 返回获得的图片url
    return img_urls

# 第四步：判断获取图片的状态码是否正确
def get_img(img_urls):
    # 4.2 请求图片的url
    response = requests.get(img_urls)
    # 4.3 如果状态码是200，代表获取正确的url，返回获取的网页
    if response.status_code == 200:
        return response.content

# 主函数，程序的入口
def main():
    url = 'http://www.manhuadao.cn/Comic/ComicView?comicid=58df8c73d401da325c9cf77c&chapterid=9587480'
    # 2.1 执行_get(url)方法,并传入url,保存为text
    text = _get(url)

    # 3.1 执行html(text)方法,并传入text,保存为img_urls
    img_urls = html(text)

    # 3.6 遍历img_urls获取单个img_url
    for img_url in img_urls:
        # http: // mhdgu.1391.com / bookcenter / 176845 / 2201313 / U_7_1_44c885ce - f3f0 - 4e35 - 9ced - 3e8b52683d73.jpg
        # 3.6.1 对img_url以‘.’进行分割，并取得倒数第二个值，保存为img_name1
        img_name1 = img_url.split(".")[-2]
        # print(img_name1[-2])

        # 3.6.2 对img_name1以‘/’进行分割，并取得倒数第一个值，保存为img_name2
        img_name2 = img_name1.split("/")[-1]
        # print(img_name2[-1])

        # 3.6.3 对img_name2以 ‘-’进行分割，并取得倒数第一个数，保存为img_name3
        img_name3 = img_name2.split("-")[-1]
        # print(img_name3[-1])

        # 3.6.4 将取得的img_name3保存在img_name中
        img_name = img_name3
        # 4.1 执行get_img(img_url)方法，并且传入img_url,保存为content
        content = get_img(img_url)

# 第五步：让计算机代替我们去下载，以二进制数据写入到磁盘里
        with open('images/%s.jpg' % img_name, 'wb') as f:
            f.write(content)
            # 以二进制的方式写入数据
            print(img_name+"下载完毕")

# 执行主函数
if __name__ == '__main__':
    main()