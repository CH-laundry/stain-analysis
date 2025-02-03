from flask import Flask, request, jsonify
import os
import cv2  # 影像處理函式庫
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def analyze_stain(image_path):
    """ 簡單的污漬分析函數，判斷污漬顏色與大小，並預測清洗成功率 """
    try:
        image = cv2.imread(image_path)
        if image is None:
            return {"error": "無法讀取圖片"}

        # 轉換成灰階
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        # 計算污漬大小（黑色部分）
        stain_size = np.sum(thresh == 0)
        image_size = thresh.shape[0] * thresh.shape[1]
        stain_ratio = stain_size / image_size

        # 根據污漬比例 & 顏色判斷
        if stain_ratio < 0.02:
            stain_level = "輕微污漬"
            clean_probability = 95  # 高機率可清除
        elif stain_ratio < 0.1:
            stain_level = "中度污漬"
            clean_probability = 70  # 可能需要專業清洗
        else:
            stain_level = "嚴重污漬"
            clean_probability = 40  # 可能難以完全清除

        return {
            "stain_level": stain_level,
            "clean_probability": clean_probability
        }

    except Exception as e:
        return {"error": str(e)}

@app.route('/upload', methods=['POST'])
def upload_file():
    """ 接收用戶上傳的圖片並分析污漬 """
    if 'file' not in request.files:
        return jsonify({"error": "未上傳檔案"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "檔案名稱無效"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # 進行污漬分析
    stain_result = analyze_stain(filepath)

    return jsonify({
        "message": "上傳成功",
        "file_path": filepath,
        "stain_analysis": stain_result
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
