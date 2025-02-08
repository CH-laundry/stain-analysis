from flask import Flask, request, jsonify
import os
from linebot.v3.messaging import MessagingApi
from linebot.v3.webhook import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessage
from linebot.v3.messaging import TextMessageContent
from waitress import serve  # 確保在最上面

# 讀取環境變數（只讀取一次）
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

# 確保環境變數已經設定
if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
    print("❌ 錯誤：環境變數 LINE_CHANNEL_ACCESS_TOKEN 或 LINE_CHANNEL_SECRET 未設置！")
    exit(1)  # 強制終止程式

app = Flask(__name__)  # ✅ 確保 `app` 只定義一次

line_bot_api = MessagingApi(channel_access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# ✅ Webhook 路由
@app.route("/webhook", metho
