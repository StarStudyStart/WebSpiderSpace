# 图片处理
from PIL import Image,ImageFilter

mid_autom = Image.open("mid_autom.jpg")
blurry_mid_autom = mid_autom.filter(ImageFilter.GaussianBlur)
blurry_mid_autom.save("mid_autom_blurry.jpg")
blurry_mid_autom.show()
