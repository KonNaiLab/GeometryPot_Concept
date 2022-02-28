from crypt import methods
from flask import Flask, request, jsonify, make_response
from dotenv import load_dotenv
import pymongo
import os
import certifi

#token auth ###############################################
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from flask_cors import CORS, cross_origin
from flask import Flask, request, abort
##########################################################
load_dotenv(".env")

# MongoDB
MONGODB_ACCOUNT = os.getenv('MONGO_DB')

myclient = pymongo.MongoClient(MONGODB_ACCOUNT, tlsCAFile=certifi.where())
mydb = myclient["Geometry_Pot"]
mycol = mydb["test1"]
status = mydb["Status"]
config = mydb["Config"]
 
# Flask Process
app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
    return "Hello World"


@app.route('/add_data', methods=["POST"])
def insert():
    body = request.get_json()
    x = mycol.insert_one(body)
    return "success"

@app.route("/add_pot", methods=["POST"])
def add_pot():
    data = request.get_json()
    print(data["Name"])
    print(data)

if __name__ == "__main__":
    print(mycol)
    app.run(debug=True, port=5555)
