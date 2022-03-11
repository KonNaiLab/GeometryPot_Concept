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

@app.route('/add_data', methods=["POST"])
def insert():
    body = request.get_json()
    mydb = connect()
    x = mydb["test1"].insert_one(body)
    return "sus"

@app.route("/add_pot", methods=["POST"])
def add_pot():
    data = request.get_json()
    print(data["Name"])
    print(data)
    print("add to mongo")
    d = addpots(data)
    print(d)
    return "ok"

@app.route("/addpot", methods=["POST"])
def set_time_light():
    body = request.get_json()
    mydb = connect()
    mydb["Pots"].insert_one(body)
    default = {"Name":body["Name"],"Fan":"off","Pump":"off"}
    mydb["Status"].insert_one(default)
    return "k"

@app.route("/patch_pot", methods=["PATCH"])
def patch_pot():
    body = request.get_json()
    mydb = connect()
    mydb["Pots"].find_one_and_replace({"Name":body["Name"]},body)
    return "k"

@app.route("/patch_status", methods=["PATCH"])
def patch_status():
    body = request.get_json()
    mydb = connect()
    mydb["Status"].find_one_and_replace({"Name":body["Name"]},body)
    return "k"

if __name__ == "__main__":
    # print("hello")
    app.run(debug=True, port=5555)
