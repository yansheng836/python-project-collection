#!/usr/bin/env python  
# -*- coding: utf-8 -*-

import re
import requests


# url1 = 'https://www.ybdu.com/xiaoshuo/2/2531/259845.html'

def get_html(url):
    response = requests.get(url)
    return response.text


def get_chapter_info(html):
    ul = re.findall(r'<ul class="mulu_list">(.*?)</ul>', html, re.S)[0]
    chapter_info = re.findall(r'<a href="(.*?)">(.*?)</a>', ul)
    return chapter_info

def get_chapter_content(url):
    print(url)
    response = get_html(url)
    content = re.findall(r'<div id="htmlContent" class="contentbox">(.*?)<div class="ad00">', response, re.S)[0]
    content = content.replace('&nbsp;', '')
    content = content.replace('<br />', '')
    return content

def main():
    url = 'https://www.ybdu.com/xiaoshuo/2/2531/'
    html = get_html(url)
    title = re.findall(r'<h1>(.*?)全文阅读</h1>', html)[0].strip()
    chapter_info = get_chapter_info(html)
    with open('%s.txt' % title, 'w', encoding='utf-8')as f:
        f.write('%s\n' % title)
        for chapter in chapter_info:
            f.write('%s' % chapter[1])
            content = get_chapter_content(url+chapter[0])
            f.write('%s' % content)
if __name__ == '__main__':
    main()
