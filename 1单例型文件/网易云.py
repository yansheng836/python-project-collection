from tkinter import *
# 执行 from package import * 时，如果包中的 __init__.py 代码定义了一个名为 __all__ 的列表，就会按照列表中给出的模块名进行导入
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import time

# 获取页面源代码
# 获取ID
# 下载音乐
# 思路
# https://blog.csdn.net/aa527844671/article/details/80823154
def download_song():
    # 获取URL地址
    url = entry.get()
    # 请求头
    header = {
        'Host': 'music.163.com',
        'Referer': 'https://music.163.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    # 获取页面源代码
    res = requests.get(url,headers=header).text
    # 创建对象 解析网页  lxml
    r = BeautifulSoup(res,"html.parser")
    # print(type(r))

    # 空音乐列表
    music_dict = {}
    # playlist=id?123412312  这里去找音乐播放URL地址
    result = r.find('ul', {'class': 'f-hide'}).find_all('a')
    for music in result:
        # 获取音乐ID
        music_id = music.get('href').strip("/song?id=")
        # 音乐名称
        music_name = music.text
        # print(music_id)
        # print(music_name)
        music_dict[music_id] = music_name
    # 字典  id:歌曲名称
    # print(music_dict)

# def download_song(music_dict,song_id):
    # 全部下载
    for song_id in music_dict:
        # 网易云官方的外界链接播放去获取下载链接
        # 该链接为浏览器在网页版缓存歌曲的下载链接
        song_url = 'http://music.163.com/song/media/outer/url?id=%s.mp3'%song_id
        # 下载地址
        path = 'E:\文章\新建文件夹\music\%s.mp3'%music_dict[song_id]

        # https://music.163.com/playlist?id=2269661190

        # 添加数据
        text.insert(END, "正在下载:%s"%music_dict[song_id])
        # 文本框向下滚动
        text.see(END)
        # 更新
        text.update()
        # 下载地址  下载路径   断点续传
        time.sleep(0.9)
        urlretrieve(song_url, path)

# music_dict = get_content(url)
# music_dict = get_content()
# pprint(music_dict)
# download_song(music_dict)
# while True:
#     song_id = input("请输入想下载的歌曲id:")
#     print("正在搜索歌曲信息并下载.")
#     download_song(song_id, music_dict)

# 创建窗口
root = Tk()
# 窗口标题
root.title("网易云音乐")
# 窗口大小
root.geometry("550x400")
# 窗口位置
root.geometry("+400+300")
# 标签控件 可以设置字体 大小 颜色
label = Label(root, text='请输入要下载的歌单URL:', font=('华文行楷', 10))
# row=0, column=0  grid 网格布局  pack   place   但是不要混合使用
# 定位
label.grid()
# 输入框 entry 显示单行文本  Text
entry = Entry(root, font=('微软雅黑', 25))
# row 行  column 列  pack  place
entry.grid(row=0, column=1)

# 列表框控件
text = Listbox(root,font = ('微软雅黑',15),width = 45,height = 10)
# columnspan  组件所跨越的列数
text.grid(row = 1,columnspan = 2)

# 点击按钮
button = Button(root, text='开始下载', font=('微软雅黑', 15), command=download_song)
# button['width'] = 10
# button['height'] = 1
# 你可以使用sticky选项去指定对齐方式 上下左右   N S W E
button.grid(row=2, column=0,sticky = W)

button1 = Button(root,text="退出",font=("微软雅黑",15),command = root.quit)
button1.grid(row = 2,column = 1,sticky = E)

root.mainloop()


