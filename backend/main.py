from flask import Flask, request
from dotenv import load_dotenv
import pymongo
import os
import certifi

load_dotenv(".env")

# MongoDB
MONGODB_ACCOUNT = os.getenv('MONGO_DB')

myclient = pymongo.MongoClient(MONGODB_ACCOUNT, tlsCAFile=certifi.where())
mydb = myclient["Geometry_Pot"]
mycol = mydb["test1"]


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


if __name__ == "__main__":
    print(mycol)
    app.run(debug=True, port=5555)
