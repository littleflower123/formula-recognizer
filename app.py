from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import os

# 初始化 Flask
app = Flask(__name__)
CORS(app)  # 解决跨域问题

# 👇 不要一开始加载模型（关键！）
model = None

def get_model():
    global model
    if model is None:
        from pix2tex.cli import LatexOCR
        print("👉 正在加载模型（第一次会比较慢）...")
        model = LatexOCR()
        print("✅ 模型加载完成")
    return model


@app.route('/')
def home():
    return "LaTeX OCR API is running ✅"


@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # 获取上传图片
        image_file = request.files['image']
        image = Image.open(image_file)

        # 👇 使用延迟加载模型
        latex = get_model()(image)

        # 返回结果
        return jsonify({'latex': latex})

    except Exception as e:
        return jsonify({'error': str(e)})


# 👇 Render 必须这样写
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)