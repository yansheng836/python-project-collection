# -*- coding: utf-8 -*-
import os
import re
import requests
from bs4 import BeautifulSoup

save_folder = r'./'
domain_name = 'http://www.27270.com/ent/meinvtupian/'
start_url = 'http://www.27270.com/ent/meinvtupian/'
# 'http://699pic.com/tupian/biyeji.html'
# http://www.27270.com/ent/meinvtupian/

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
    'Connection':'keep-alive',
    'DNT': '1',
    'Host': 'www.kongjie.com',
    'Referer': 'http://www.kongjie.com/home.php?mod=space&do=album&view=all&order=hot&page=1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
uid_picid_pattern = re.compile(r'.*?uid=(\d+).*?picid=(\d+).*?')



def save_img(image_url, uid, picid):
    """
    保存图片到全局变量save_folder文件夹下，图片名字为“uid_picid.ext”。
    其中，uid是用户id，picid是空姐网图片id，ext是图片的扩展名。
    """
    try:
        response = requests.get(image_url, stream=True)
        # 获取文件扩展名
        file_name_prefix, file_name_ext = os.path.splitext(image_url)
        save_path = os.path.join(save_folder, uid + '_' + picid + file_name_ext)
        with open(save_path, 'wb') as fw:
            fw.write(response.content)
        print(uid + '_' + picid + file_name_ext, 'image saved!', image_url)
    except IOError as e:
        print('save error！', e,"111", image_url,"222")


def save_images_in_album(album_url, count):
    """
    进入空姐网用户的相册，开始一张一张的保存相册中的图片。
    """
    # 解析出uid和picid，用于存储图片的名字
    response = requests.get(album_url)
    soup = BeautifulSoup(response.text, 'lxml')
    image_div = soup.select('.articleV4Body img')

    for image in image_div:
        print(image.attrs['src'])
        try:
            response = requests.get(image.attrs['src'])
            save_path = os.path.join(save_folder, str(count) + '.jpg')
            with open(save_path, 'wb') as fw:
                fw.write(response.content)
        except IOError as e:
            print('save error！', e, "222")




    # next_image = soup.select_one('div.pns.mlnv.vm.mtm.cl a.btn[title="下一张"]')
    # if not next_image:
    #     return
    # # 解析下一张图片的picid，防止重复爬取图片，不重复则抓取
    # next_image_url = next_image['href']
    # next_uid_picid_match = uid_picid_pattern.search(next_image_url)
    # if not next_uid_picid_match:
    #     return
    # next_uid = next_uid_picid_match.group(1)
    # next_picid = next_uid_picid_match.group(2)
    # # if not redis_con.hexists('kongjie', next_uid + ':' + next_picid):
    # save_images_in_album(next_image_url)


def parse_album_url(url):
    """
    解析出相册url，然后进入相册爬取图片
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    people_list = soup.select('li a.tit')
    count = 0
    for people in people_list:
        save_images_in_album(people.attrs['href'], count)
        count = count + 1
        # break

    # # 爬取下一页
    # next_page = soup.select_one('a.nxt')
    # if next_page:
    #     parse_album_url(next_page['href'])

if __name__ == '__main__':
    parse_album_url(start_url)


