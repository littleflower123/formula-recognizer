from pix2tex.cli import LatexOCR
from PIL import Image

model = LatexOCR()

# 👇 正确：先读取图片
img = Image.open("2.png")

# 👇 再传进去
result = model(img)

print("识别结果：", result)