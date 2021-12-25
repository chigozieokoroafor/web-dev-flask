from flask import Flask, redirect, request, Response, jsonify
#from flask.json import jsonify
from werkzeug.wrappers import response
import json
import pymongo
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from bson import ObjectId



#mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=100000)
mongo = pymongo.MongoClient("mongodb+srv://aptcoder:wonderful.@cluster0.5gyf4.mongodb.net/swep-be?retryWrites=true")
mongo.server_info()
db = mongo.get_database("swep-be")
user_check = db.stage_one_vps
user_info  = db.users


app = Flask(__name__)
CORS(app, resources={r"/": {"origin": "*"}})
bcrypt = Bcrypt(app) 
app.config["SECRET_KEY"] ="youcannotguessit"
secret_key = "youcannotguessit"


@app.route("/", methods=["POST", "GET"])
def card():
    
    if request.method =="GET":
        reg_number = request.form.get("reg_number")
        user_ = user_info.find_one({"registrationNumber":reg_number})
        stage_one = user_check.find_one({"status":"incomplete", "user":ObjectId(user_["_id"])})
        return (json.dumps(user_), 200)
    return "this is the work in progress"


if __name__ =="__main__":
    app.run(debug=True, port=90)