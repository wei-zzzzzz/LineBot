import os
import json
import random
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import  *

line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])

def lambda_handler(event, context):
    @handler.add(MessageEvent)
    def handle_message(event):
        if event.message.type != 'text':
            reply_message = '給我幾個選項吧～'
        else:
            if event.message.text[:2] == '選項': 
                choices = event.message.text[3:].split(' ')
                reply_message = '我選 '+choices[random.randint(0, len(choices)-1)]
            else:
                reply_message = '給我幾個選項吧～'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
    
    # 一加入群組的發言
    @handler.add(JoinEvent)
    def handle_join(event):
        newcoming_text = "抽籤抽起來！！"
        line_bot_api.reply_message(event.reply_token, TextMessage(text=newcoming_text))
    
    #----------lambda main--------------------------------------
    # get X-Line-Signature header value
    signature = event['headers']['x-line-signature']

    # get request body as text
    body = event['body']

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {
            'statusCode': 502,
            'body': json.dumps("Invalid signature. Please check your channel access token/channel secret.")
            }
    return {
        'statusCode': 200,
        'body': json.dumps("Hello from Lambda!")
        }