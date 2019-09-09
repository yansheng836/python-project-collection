

import requests  
import re 
import time  
 
"""    爬取哔哩哔哩视频弹幕信息"""  
# 2043618 是视频的弹幕标号,这个地址会返回时间列表 
# https://www.bilibili.com/video/av1349282 
url = 'https://comment.bilibili.com/rolldate,2043618'  
# 获取弹幕的id 2043618 
video_id = url.split(',')[-1]print(video_id) 
# 获取json文件 
html = requests.get(url)  
# print(html.json())  
# 生成时间戳列表 
time_list = [i['timestamp'] for i in html.json()] 
# print(time_list) 
# 获取弹幕网址格式 'https://comment.bilibili.com/dmroll,时间戳,弹幕号'  
# 弹幕内容,由于总弹幕量太大,将每个弹幕文件分别保存 
 
for i in time_list:    
  content = ''    
  j = 'https://comment.bilibili.com/dmroll,{0},{1}'.format(i, video_id)    
  #print(j)    
  text = requests.get(j).text 
 
    # 匹配弹幕内容    res = re.findall('<d p=".*?">(.*?)</d>', text)     
 
    # 将时间戳转化为日期形式,需要把字符串转为整数    timeArray = time.localtime(int(i))    date_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)    print(date_time)    content += date_time + ' 
 
    for k in res:        
      content += k +  
      content +=  
    file_path = 'txt/{}.txt'.format(time.strftime("%Y_%m_%d", timeArray))
    print(file_path)  
 
    with open(file_path, mode='w+', encoding='utf8') as f:        f.write(content)  