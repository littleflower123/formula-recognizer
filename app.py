from flask import Flask, request, jsonify
from flask_cors import CORS
from pix2tex.cli import LatexOCR
from PIL import Image
import os

# 初始化 Flask
app = Flask(__name__)
CORS(app)

# 👇 初始化模型（只加载一次，避免重复加载卡死）
print("正在加载模型（首次会比较慢）...")
model = LatexOCR()
print("模型加载完成")

@app.route('/')
def home():
    return "LaTeX OCR 本地服务已启动 ✅"

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        print("收到请求")

        image_file = request.files['image']
        image = Image.open(image_file)

        print("开始识别...")
        latex = model(image)
        print("识别完成")

        return jsonify({'latex': latex})

    except Exception as e:
        print("出错：", e)
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)