##coding=utf-8
#根据肤色数量判断
from PIL import Image
basedir=r'D:\Python\PycharmProjects\nudedetection\imag2'
import os
for filename in os.listdir(basedir):
    full_filename=os.path.join(basedir,filename)
    img = Image.open(full_filename).convert('YCbCr')
    w, h = img.size
    data = img.getdata()
    cnt = 0
    for i, ycbcr in enumerate(data):
        y, cb, cr = ycbcr
        if 86 <= cb <= 117 and 140 <= cr <= 168:
            cnt += 1
    print '%s is a porn image?:%s.'%(filename, 'Yes' if cnt > w * h * 0.3 else 'No')
