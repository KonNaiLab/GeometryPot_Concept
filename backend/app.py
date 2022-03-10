from flask import Flask, request, jsonify, make_response
import pymongo
import os

'''
-Line Bot
#pip install line-bot-sdk
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

''''''
#mydb = myclient["Geometry_Pot"]
#mycol = mydb["test1"]
#pots = mydb["Pots"]

def connect():
    # My test server link that will change when you install in another server
    myclient = pymongo.MongoClient(
        "mongodb+srv://chuncheiw_team:o6bROnEYRtsiRle2@cluster0.jjsfz.mongodb.net/Geometry_Pot?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)
    mydb = myclient["Geometry_Pot"]
    print(mydb)
    return mydb


def addpots(data):
    mydb = connect()
    pots = mydb["Pots"]
    newd = {
        "Name": data["Name"],
        "Lighttime": [8.00, 18.00],
        "HumidityLV": 0,
        "TemperatureLV": 0,
    }
    pots.insert_one(newd)
    return newd


db = connect()
print(db)


@app.route('/', methods=["GET"])
def home():
    # print(.collection)

    return "Hello"

'''Line Bot'''

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

@app.route('/add_data', methods=["POST"])
def insert():
    body = request.get_json()
    print(body)
    mydb = connect()
    x = mydb["test1"].insert_one(body)
    return "success"
''''''
def reply_message(token, message):
    line_bot_api.reply_message(token, TextSendMessage(text=message))

def broadcast_message(message):
    line_bot_api.broadcast(TextSendMessage(
        text=message))

    return 'Notified Janitors'
''''''

@app.route("/add_pot", methods=["POST"])
def add_pot():
    data = request.get_json()
    print(data["Name"])
    print(data)
    print("add to mongo")
    d = addpots(data)
    print(d)
    return "ok"


    # except:
    #    return "fail"
if __name__ == "__main__":
    # print("hello")
    app.run(debug=True, port=5555)
