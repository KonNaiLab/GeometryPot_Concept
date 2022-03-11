from flask import Flask, abort, request, jsonify, make_response
import pymongo
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from sympy import N

from app import addpots,setpot,askstatus,findalert

app = Flask(__name__)

line_bot_api = LineBotApi('ikDp2ap89gvpkrB4f9djOEfXSvvAyDcZ+yhKTfU+90oaTOsJn/AZdk51VK1rnnl7Hv19eJukOsx0YQWga1d76FlNNH0B+7Li23iOKUkL1nMkNpJgRuyKw1k/CLsY6ivV1wyTuzGV84B54xsq5tE30QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('69b00f0f5fae1c6f51cda305a4acf289')

def connect():
    # My test server link that will change when you install in another server
    myclient = pymongo.MongoClient(
        "mongodb+srv://chuncheiw_team:o6bROnEYRtsiRle2@cluster0.jjsfz.mongodb.net/Geometry_Pot?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)
    mydb = myclient["Geometry_Pot"]
    print(mydb)
    return mydb

db = connect()

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

def reply_message(token, message):
    line_bot_api.reply_message(token, TextSendMessage(text=message))

def defalut_reply(token):
    default_reply_message = "ดูเหมือนว่าคุณทำบางอย่างผิดน่ะ คำสั่ง!help สามารถช่วยคุณได้"
    reply_message(token, default_reply_message)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):# สถานะ ตั้งค่า โซล help<--+ defult massy
    message = event.message
    token = event.reply_token
    if message.type == "text":
        text_message = message.text
        space_separated_message =text_message.strip().split(" ")
        if "!สถานะ"==text_message and len(space_separated_message)!=2:
            if type(space_separated_message[1])!=type(int):
                defalut_reply(token)
                return
            data=askstatus(space_separated_message[1],"all")#<==space_separated_message[1] ตัวเลข
            if data["light"]==0:
                light="ปิด"
            else:
                light="เปิด"
            if data["tank"]==0:
                tank="ไม่มี"
            else:
                tank="มี"
            humid=data["humid"]
            temp=data["temp"]
            message_reply="สถานะ\n ระดับน้ำในระดับที่กำหนด : {tank}\n ระดับความชื้น : {humid}\n หลอดไฟ : {light}\n อุณหภูมิ : {temp}"
            reply_message(token, message_reply)
            return 
        elif "!ตั้งค่า" == text_message and len(space_separated_message)!=3:
            
            return 
        elif "!โซน"==text_message:
            return 
        elif "!help"==text_message:
            return 
        else:
            defalut_reply(token)
        return

    
    '''
    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=event.message.text))
    '''

def reply_message(token, message):
    line_bot_api.reply_message(token, TextSendMessage(text=message))

def broadcast_message(message):
    line_bot_api.broadcast(TextSendMessage(text=message))

    return 'Notified Janitors'

if __name__ == "__main__":
    app.run(debug=True, port=2000)
'''
-Line Bot
#pip install line-bot-sdk
'''
'''
#อันนี้ขอเก็บไว้ https://elements.heroku.com/buildpacks/line/line-bot-sdk-python มันเอาไว้ใช้ดูว่ามีฟังค์ชันของ line bot
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('ikDp2ap89gvpkrB4f9djOEfXSvvAyDcZ+yhKTfU+90oaTOsJn/AZdk51VK1rnnl7Hv19eJukOsx0YQWga1d76FlNNH0B+7Li23iOKUkL1nMkNpJgRuyKw1k/CLsY6ivV1wyTuzGV84B54xsq5tE30QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('69b00f0f5fae1c6f51cda305a4acf289')

'''

'''Line Bot'''
'''
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
def reply_message(token, message):
    line_bot_api.reply_message(token, TextSendMessage(text=message))

def broadcast_message(message):
    line_bot_api.broadcast(TextSendMessage(text=message))

    return 'Notified Janitors'
'''
'''
def reply_message(token, message):
    line_bot_api.reply_message(token, TextSendMessage(text=message))

def broadcast_message(message):
    line_bot_api.broadcast(TextSendMessage(
        text=message))

    return 'Notified Janitors'
'''