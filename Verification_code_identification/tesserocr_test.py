#coding:utf-8
import logging

from PIL import Image
import tesserocr

logging.basicConfig(level=logging.INFO)

image1 = Image.open('./UAPW.jpg')
image2 = Image.open('./2L3AN.jpg')

#转化为灰度图像
image1 =image1.convert('L')
#设定二值化阀值
threshold = 127
table =[]
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
# 二值化处理
image1 =image1.point(table, '1')
# image1.show()

#image2转化为灰度图像
image2 = image2.convert('L')
#image2二值化处理
image2 = image2.convert('1')
image2.show()

result1 = tesserocr.image_to_text(image1)
result2 = tesserocr.image_to_text(image2)

logging.info((result1,result2))
