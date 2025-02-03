from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# 確保有個資料夾來存放上傳的圖片
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return "污漬分析系統運行中"

# 新增一個 API 來處理圖片上傳
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "沒有檔案"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "檔案名稱是空的"}), 400

    # 儲存圖片
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    return jsonify({"message": "上傳成功", "file_path": file_path})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
