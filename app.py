import os
import json
import getInfomation
from choose import make_bubble
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import  *


app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST','GET'])
def callback():
<<<<<<< HEAD
=======

>>>>>>> c13cf5fe29d6eec16ecd5153ebaa485c67a56217
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
    parent = getInfomation(event.message.text)
    if parent:
        message = TextSendMessage(text=parent)
    else:
        message = TextSendMessage(text="無此學生")
    line_bot_api.reply_message(event.reply_token, message)

    return 0

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)