from flask import Flask, abort, request, jsonify, make_response
from numpy import array
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

'''
zone={"เขตอบอุ่น":{"light" : [9,16],"humid" :56,"temp" :30},
"เขตร้อน":{"light" : [9,16],"humid" :56, "temp" :35},
"เขตแห้งแล้ง":{"light" : [9,16],"humid" :45,"temp" :35}}
'''
zone={"เขตอบอุ่น":{"humid" :56,"temp" :30},
"เขตร้อน":{"humid" :56, "temp" :35},
"เขตแห้งแล้ง":{"humid" :30,"temp" :34}}

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
    default_reply_message = "ดูเหมือนว่าคุณทำบางอย่างผิดน่ะ คำสั่ง !help สามารถช่วยคุณได้"
    reply_message(token, default_reply_message)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):# สถานะ ตั้งค่า โซล help<--+ defult massy
    message = event.message
    token = event.reply_token
    if message.type == "text":
        text_message = message.text
        space_separated_message =text_message.strip().split(" ")
        if "!สถานะ"==space_separated_message[0] and len(space_separated_message)==2: #!สถานะ 1
            data=askstatus(int(space_separated_message[1]),"all")#<==space_separated_message[1] ตัวเลข
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
            message_reply=f"สถานะ\n ระดับน้ำในระดับที่กำหนด : {tank}\n ความชื้น : {humid}\n หลอดไฟ : {light}\n อุณหภูมิ : {temp}"
            reply_message(token, message_reply)
            return 
        elif "!ตั้งค่า" == space_separated_message[0]: #and (len(space_separated_message)!=4 or len(space_separated_message)!=5): # !ตั้งค่า 1 ไฟ ค่าที่ต้องการ
            # !ตั้งค่า 1 ไฟ 0 5
            modedict={"หลอดไฟ":"light","ความชื้น":"humid","อุณหภูมิ":"temp"}
            if space_separated_message[2]=="หลอดไฟ":
                #roadcast_message("fuck")
                #broadcast_message(str(space_separated_message))
                new_data=[int(space_separated_message[3]),int(space_separated_message[4])]
            else:
                new_data=space_separated_message[3]
            #broadcast_message(str(new_data[0])+str(new_data[1]))
            data=setpot({"data":new_data},space_separated_message[1],modedict[space_separated_message[2]])
            return 
        elif "!โซน"==space_separated_message[0]:# !โซน ร้อน 1 || โซน ข้อมูล
            if len(space_separated_message)==1:
                message_reply2="เขตอบอุ่น: ความชื้น 56% อุณหภูมิ 30 c\nเขตร้อน ความชื้น 56% อุณหภูมิ 35 c\nเขตแห้งแล้ง ความชื้น 30% อุณหภูมิ 34 c"
                reply_message(token, message_reply2)
            elif len(space_separated_message)==3 and (space_separated_message[1] in zone):
                setpot({"data":zone[space_separated_message[1]]["temp"]},space_separated_message[2],"temp")
                setpot({"data":zone[space_separated_message[1]]["humid"]},space_separated_message[2],"humid")
            return
        elif "!help"==space_separated_message[0]:
            if len(space_separated_message)==1:
                message_reply="   !สถานะ <ลำดับกระถาง> = แสดงสถานะของกระถานนั้น\n   !ตั้งค่า <ลำดับกระถาง> <โหมดที่ต้องการ> <ค่าที่ต้องการ> = เปลี่ยนค่าที่ต้องการจะเปลี่ยน\n   !ตั้งค่า <ลำดับกระถาง> หลอดไฟ <เวลาเริ่มต้น> <เวลาสิ้นสุด> = เปลี่ยนระยะเวลาฉายไฟ\n   !โซน = แสดงข้อมูลโซนที่ให้เลือกทั้งหมด   \n   !โซน <เขตที่ต้องการ> <ลำดับกระถาง> = เปลี่ยนค่าตามโซลที่เลือก   \nโหมด     \n[อุณหภูมิ , ความชื้น]"
                reply_message(token, message_reply)
                return
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
'''