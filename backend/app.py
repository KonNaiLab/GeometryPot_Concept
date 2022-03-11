#from crypt import methods
from flask import Flask, request, jsonify, make_response
import pymongo
import os

app = Flask(__name__)
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
    ### add to pots
    pots = mydb["Pots"]
    newd = {
        "Name": data["Name"],
        "Lighttime": [[8.00, 18.00],[8.00, 18.00]],
        "HumidityLV": [0, 0],
        "TemperatureLV": [0,0],
    }
    pots.insert_one(newd)

    #######
    ### add to status
    sta = mydb["Status"]
    sd = {
        "Light": [0, 0],
        "Humid": [0, 0],
        "Temperature": [0, 0],
        "HaveW": [0, 0],
    }
    #######
    sta.insert_one(sd)
    ### manual mode
    manual = mydb["Manual"]
    man = {
        "fan": [0,0],
        "pump" : [0,0]
    }
    manual.insert_one(man)
    return newd
    
def setpot(data, potnumber, mode):
    modedict = {
        "light" : "Lighttime",
        "humid" : "HumidityLV",
        "temp" : "TemperatureLV"
    }
    mydb = connect()
    ### add to pots
    pots = mydb["Pots"]
    x = pots.find_one()
    myquery = { "Name": "Demo" }
    dat = x[modedict[mode]]
    if potnumber == "all":
        print("all")
        dat[0] = data
        dat[1] = data
    else:
        print(int(potnumber))
        dat[int(potnumber)-1] = data
    newvalues = { "$set": { modedict[mode]: dat } }
    pots.update_one(myquery, newvalues)
    return 0
def addstatus(data):
    return 0

db = connect()
print(db)


@app.route('/', methods=["GET"])
def home():
    # print(.collection)

    return "Hello"

@app.route('/add_data', methods=["POST"])
def insert():
    body = request.get_json()
    mydb = connect()
    x = mydb["test1"].insert_one(body)
    return "success"

def reply_message(token, message):
    line_bot_api.reply_message(token, TextSendMessage(text=message))

def broadcast_message(message):
    line_bot_api.broadcast(TextSendMessage(
        text=message))

    return 'Notified Janitors'


@app.route("/add_pot", methods=["POST"])
def add_pot():
    data = request.get_json()
    print(data["Name"])
    print(data)
    print("add to mongo")
    d = addpots(data)
    print(d)
    return "ok"

@app.route("/set_pot/<potnumber>/<mode>", methods=["POST"])
def set_pot(potnumber, mode):
    data = request.get_json()
    print(potnumber)
    print(type(potnumber))
    print(mode)
    print(type(mode))
    a = setpot(data["data"], potnumber, mode)
    return "ok number one"

if __name__ == "__main__":
    # print("hello")
    app.run(debug=True, port=5555)
