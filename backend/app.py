from flask import Flask, request, jsonify, make_response
import pymongo
import os
import datetime
import time

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
    #myquery = { "Name": "xtest" }
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

def setman(data, potnumber, mode):
    mydb = connect()
    ### add to pots
    pots = mydb["Manual"]
    x = pots.find_one()
    #myquery = { "Name": "xtest" }
    dat = x[mode]
    if potnumber == "all":
        print("all")
        dat[0] = data
        dat[1] = data
    else:
        print(int(potnumber))
        dat[int(potnumber)-1] = data
    newvalues = { "$set": {mode: dat } }
    pots.update_one({}, newvalues)

def askstatus(potnumber, ask):
    askdict = {
        "light": "Light",
        "humid": "Humid",
        "temp" : "Temperature",
        "tank" : "HaveW"
    }
    mydb = connect()
    status = mydb["Status"]
    data = status.find_one()
    m = mydb["Manual"]
    man = m.find_one()
    if ask == "all":
        return {
            "light": (data[askdict["light"]])[potnumber-1],
            "humid": (data[askdict["humid"]])[potnumber-1],
            "temp" : (data[askdict["temp"]])[potnumber-1],
            "tank" : (data[askdict["tank"]])[potnumber-1]
        }
    elif ask == "fan":
        return {
            ask : (man["fan"])[potnumber-1]
        }
    else:
        return {
            ask : (data[askdict[ask]])[potnumber-1]
        }

def findalert():
    mydb = connect()
    pots = mydb["Pots"]
    p = pots.find_one()
    sta = mydb["Status"]
    s = sta.find_one()
    return {
        "tank1_alert": int(not (s["HaveW"][0])),
        "tank2_alert": int(not (s["HaveW"][1]))
    }

def gotsetting():
    mydb = connect()
    pots = mydb["Pots"]
    p = pots.find_one()
    return p

def gotmanual():
    mydb = connect()
    pots = mydb["Manual"]
    p = pots.find_one()
    return p

def gotstatus():
    mydb = connect()
    status = mydb["Status"]
    data = status.find_one()
    return data

def updatestatus(data, utype):
    mydb = connect()
    sta = mydb["Status"]
    if utype == "light":
        newvalues = { "$set": { "Light": data } }
        sta.update_one({}, newvalues)
    elif utype == "fan":
        newvalues = { "$set": { "Temperature": data } }
        sta.update_one({}, newvalues)
    elif utype == "pump":
        newvalues = { "$set": { "HaveW": data } }
        sta.update_one({}, newvalues)

@app.route('/', methods=["GET"])
def home():
    return "Hello"

@app.route('/add_data', methods=["POST"])
def insert():
    body = request.get_json()
    mydb = connect()
    x = mydb["test1"].insert_one(body)
    return "success"


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
    print(data["data"])
    print(type(data["data"]))
    a = setpot(data["data"], potnumber, mode)
    return "ok number one"

@app.route("/status/<potnumber>/<ask>", methods=["GET"])
def ask_status(potnumber, ask):
    res = askstatus(int(potnumber), ask)
    return res

@app.route("/alert", methods=["GET"])
def alert():
    res = findalert()
    return res

## คุมไฟ
@app.route("/light", methods=["GET"])
def light():
    a=datetime.datetime.now().time()
    print(a.hour+(a.minute/100))
    #print(a.minute)
    #print(a.hour)
    t = gotsetting()
    m = gotmanual()
    return {
        "Curenttime": a.hour+(a.minute/100),
        "Settingtime": t["Lighttime"],
        "Manual" : m["light"]
    }

@app.route("/light", methods=["POST"])
def lightup():
    data = request.get_json()
    updatestatus(data["data"], "light")
    a=datetime.datetime.now().time()
    print(a.hour+(a.minute/100))
    #print(a.minute)
    #print(a.hour)
    t = gotsetting()
    m = gotmanual()
    return {
        "Curenttime": a.hour+(a.minute/100),
        "Settingtime": t["Lighttime"],
        "Manual" : m["light"]
    }



@app.route("/fan", methods=["GET"])
def fan():
    t = gotsetting()
    m = gotmanual()
    s = gotstatus()
    return {
        "Currenttemp" : s["Temperature"],
        "SettingTemp" : t["TemperatureLV"],
        "Manual" : m["fan"]
    }

@app.route("/fan", methods=["POST"])
def fan_p():
    data = request.get_json()
    t = gotsetting()
    m = gotmanual()
    s = gotstatus()
    updatestatus(data["data"], "fan")
    return {
        "Currenttemp" : s["Temperature"],
        "SettingTemp" : t["TemperatureLV"],
        "Manual" : m["fan"]
    }

@app.route("/manual_fan/<potnumber>/<do>", methods=["GET"])
def manualfan(potnumber, do):
    dic_do = {
        "on" : 2,
        "off" : 1,
        "auto" : 0
    }
    m = gotmanual()
    if (m["fan"])[int(potnumber)-1] != dic_do[do]:
        setman(dic_do[do],potnumber, "fan")
        return {
            "result" : "Success"
        }
    else:
        return {
            "result" : "error same"
        }

@app.route("/pump", methods=["POST"])
def pumpp():
    data = request.get_json()
    t = gotsetting()
    m = gotmanual()
    updatestatus(data["data"], "pump")
    s = gotstatus()

    setman(0, "all", "pump")

    return {
        "Currenthumid" : s["Humid"],
        "Settinghumid" : t["HumidityLV"],
        "Manual" : m["pump"],
        "Water" : s["HaveW"]
    }

@app.route("/man_pump/<potnumber>", methods=["GET"])
def manpump(potnumber):
    m = gotmanual()
    s = gotstatus()
    if (m["pump"])[int(potnumber)-1] == 1:
        return {
            "result" : "error same"
        }
    print(s["HaveW"][int(potnumber)-1])
    if (s["HaveW"])[int(potnumber)-1] == 1: 
        print("Wait 10s")
        time.sleep(10)
        s = gotstatus()
        if (s["HaveW"])[int(potnumber)-1] != 1:
            return {
                "result" : "low water"
            }
        setman(1, potnumber, "pump")
        return{
            "result" : "Success"
        }
    return {
        "result" : "low water"
    }
    
if __name__ == "__main__":
    # print("hello")
    app.run(debug=True, port=5555)
