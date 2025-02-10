from flask import Flask, request, jsonify
import os
import traceback  # 新增錯誤追蹤
from linebot import LineBotApi
from linebot.models import TextMessage
from linebot.v3.webhook import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, ImageMessage
from waitress import serve  # 確保在最上面

# 讀取環境變數
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
    print("❌ 錯誤：環境變數 LINE_CHANNEL_ACCESS_TOKEN 或 LINE_CHANNEL_SECRET 未設置！")
    exit(1)  # 強制終止程式

app = Flask(__name__)  # ✅ Flask 應用程式初始化
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)  
handler = WebhookHandler(CHANNEL_SECRET)

# ✅ 確保 /upload 路由存在
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "沒有上傳檔案"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "沒有選擇檔案"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # 模擬污漬分析
    stain_analysis_result = {
        "clean_probability": 75,
        "stain_level": "中度污漬"
    }

    return jsonify({
        "message": "上傳成功",
        "file_path": file_path,
        "stain_analysis": stain_analysis_result
    })

# ✅ Webhook 路由
@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers.get('X-Line-Signature')
    if not signature:
        print("❌ 缺少 X-Line-Signature")
        return jsonify({"error": "缺少 X-Line-Signature"}), 400

    body = request.get_data(as_text=True)
    print(f"📩 收到 Webhook 請求: {body}")  
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ 無效的 LINE 簽名")
        return jsonify({"error": "無效的簽名"}), 400
    except Exception as e:
        print(f"❌ Webhook 處理錯誤: {str(e)}")
        traceback.print_exc()  
        return jsonify({"error": "內部錯誤"}), 500

    return jsonify({"message": "Webhook 接收成功"}), 200

# ✅ 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("📩 收到文字訊息")
    try:
        line_bot_api.reply_message(
            event.reply_token,
            [TextMessage(text="Hello! 這是您的自動回覆訊息！")]
        )
        print("✅ 文字訊息回應成功")
    except Exception as e:
        print(f"❌ 文字訊息處理錯誤: {str(e)}")
        traceback.print_exc()

# ✅ 處理圖片訊息
@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    print("📸 handle_image() 被觸發！")  

    image_id = event.message.id
    print(f"🔍 圖片 ID: {image_id}")

    try:
        image_content = line_bot_api.get_message_content(image_id)
        image_path = f"received_{image_id}.jpg"

        with open(image_path, "wb") as f:
            for chunk in image_content.iter_content():
                f.write(chunk)
        
        print(f"✅ 圖片已儲存：{image_path}")

        reply_text = f"✅ 圖片已收到！（ID: {image_id}）\n目前還無法分析，但未來可做污漬檢測。"
        line_bot_api.reply_message(event.reply_token, [TextMessage(text=reply_text)])
        print("✅ 圖片訊息回應成功")

    except Exception as e:
        print(f"❌ 圖片處理錯誤: {str(e)}")
        traceback.print_exc()

# ✅ 確保 `/` 路徑可以回應，確認伺服器運行
@app.route("/")
def home():
    return "C.H Laundry LINE Webhook is running!"

# ✅ **顯示所有 API 路由，確認 `/upload` 是否存在**
print("📌 已註冊的路由：")
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    print(f"🚀 Flask 正在啟動，監聽 Port {port}")
    print("✅ 伺服器成功啟動，準備接受請求")
    serve(app, host='0.0.0.0', port=port)

@app.route("/routes", methods=["GET"])
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(str(rule))
    return jsonify({"routes": routes})

