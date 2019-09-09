# 第三方请求库
import requests
# re正则表达式
import re
# 导入一个url处理的方法
from urllib.parse import urlencode

# 打包我们要组合的数据
def get_data(offset):
    form_data = {
        'autoload':	'true',
        'count':	'20',
        'cur_tab':	'3',
        'format':	'json',
        'from':'gallery',
        'keyword':	'街拍',
        'offset':	offset
    }
    return form_data

def get_url(data):
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    # 得到一个json数据,保存在响应当中
    response = requests.get(url).json()
    # 定义一个空的列表,保存我们获取的url
    list_url = []
    # 遍历response得到所有的url
    for items in response.get('data'):
        # 添加url到空的列表中
        list_url.append(items.get('article_url'))
        # items['data']
    # 把装的url返回
    return list_url


def get_list_page(url):
    # 加上请求头,伪装成浏览器
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    # 请求Url,得到响应
    response = requests.get(url, headers=header).text
    re_str = re.findall(r'JSON.parse\((.*?)\)',response)[0]
    re_str = re_str.replace('\\', '')
    # print(re_str)
    re_string = re.findall(r'{"url":"(.*?)"',re_str)
    urls = set(re_string)
    return urls

def down_image(url):
    # print(url)
    name = url.split('/')[-1]
    # print(name)
    response = requests.get(url).content
    with open('./images/%s.jpg' % name, 'wb+') as f:
        f.write(response)


offset = int(input('请输入你想要下载的页数'))
page = 0

while page < offset:
    offset = page * 20
# 接收返回值
    data = get_data(offset)
    # 接收所有的url
    urls = get_url(data)
    # 遍历urls依次取出url
    for url in urls:
        set_urls = get_list_page(url)
        for url in set_urls:
            down_image(url)
    page += 1