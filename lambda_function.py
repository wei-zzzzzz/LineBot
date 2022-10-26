import os
import json
from choose import make_bubble 
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
            messages = TextSendMessage(text=reply_message)
        else:
            if event.message.text[:2] == '選項': 
                choices = event.message.text[3:].split(' ')
                bubble, choice = make_bubble(choices)
                reply_message = '我選 '+choice
                messages = [FlexSendMessage(alt_text='抽出來拉', contents=bubble), TextSendMessage(text=reply_message)]
            else:
                reply_message = '給我幾個選項吧～'
                messages = TextSendMessage(text=reply_message)
        line_bot_api.reply_message(event.reply_token, messages)
    
    # flex message postback
    @handler.add(PostbackEvent)
    def handle_message(event):
        messages = TextSendMessage(text=event.postback.data)
        # reply_arr = [message, image_message]
        line_bot_api.reply_message(event.reply_token, messages)
    
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