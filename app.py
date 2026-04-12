from flask import Flask, request, jsonify
from flask_cors import CORS
from pix2tex.cli import LatexOCR
from PIL import Image

# 初始化 Flask
app = Flask(__name__)
CORS(app)  # 解决跨域问题

# 👇 初始化模型（只加载一次）
model = LatexOCR()

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # 获取上传图片
        image_file = request.files['image']
        image = Image.open(image_file)

        # 👇 使用 pix2tex 识别 LaTeX
        latex = model(image)

        # 返回结果
        return jsonify({'latex': latex})

    except Exception as e:
        # 出错时返回错误信息（方便调试）
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)