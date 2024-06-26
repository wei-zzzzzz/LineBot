import os
import json
from getInfomation import get_parent, get_info
from choose import make_bubble
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import  *


app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])

@app.route("/<username>")
def sendMessage(username):
  try:
    df = get_info(username)
    message = f'早安{df["parents"]}先生/女士，您的小孩{df["student"]}已到校～'
    line_bot_api.push_message(df["userID"], TextSendMessage(text=message))
    return 'OK'
  except:
    print('error')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST','GET'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        print(body, signature)
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
    
# @handler.add(JoinEvent)
# def handle_join(event):
#     newcoming_text = "查詢上市臺股資訊問我就對了！！"
#     line_bot_api.reply_message(event.reply_token, TextMessage(text=newcoming_text))

# 處理訊息
@handler.add(MessageEvent)
def handle_message(event):
    # event->使用者資料
    parent = get_parent(event.message.text)
    if parent:
        message = TextSendMessage(text=parent)
    else:
        message = TextSendMessage(text="無此學生")
    line_bot_api.reply_message(event.reply_token, message)

    return 0

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
