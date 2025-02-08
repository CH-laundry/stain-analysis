from flask import Flask, request, jsonify
import os
from linebot.v3.messaging import MessagingApi
from linebot.v3.webhook import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from waitress import serve  # 確保在最上面

# 讀取環境變數（只讀取一次）
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

# 確保環境變數已經設定
if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
    print("❌ 錯誤：環境變數 LINE_CHANNEL_ACCESS_TOKEN 或 LINE_CHANNEL_SECRET 未設置！")
    exit(1)  # 強制終止程式

app = Flask(__name__)  # ✅ 確保 `app` 只定義一次

line_bot_api = MessagingApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# ✅ Webhook 路由
@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers.get('X-Line-Signature')
    if not signature:
        return jsonify({"error": "缺少 X-Line-Signature"}), 400

    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return jsonify({"error": "無效的簽名"}), 400

    return jsonify({"message": "Webhook 接收成功"}), 200

# ✅ LINE 訊息回應
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Hello! 這是您的自動回覆訊息！")
    )

# ✅ 確保 `/` 路徑可以回應，確認伺服器運行
@app.route("/")
def home():
    return "C.H Laundry LINE Webhook is running!"

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    print(f"🚀 Flask 正在啟動，監聽 Port {port}")
    serve(app, host='0.0.0.0', port=port)
