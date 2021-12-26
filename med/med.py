from flask import Flask, redirect, request, Response, jsonify, send_file  
import cv2
#from flask.json import jsonify
from werkzeug.wrappers import response
import json
import pymongo
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from bson import ObjectId
from PIL import Image


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
        user= user_info.find_one({"registrationNumber":reg_number})
        stage_one = user_check.find_one({"user":(user.get("_id"))})
        #return (json.dumps(stage_one), 200)
        if stage_one["status"].upper=="COMPLETE" :
            #img  =  cv2.imread("4.jpg")
            #img = Image.open(open("4.jpg").stream)
            
            #img = send_file(stage_one["passport"])
            #print(img.shape)
            message = {"status":stage_one["status"], "name":user["firstName"], "registrationNumber":user["registrationNumber"], "passport":stage_one["passport"]}
            return json.dumps(message), 200
        return("error in verification", 401)
    return "this is the work in progress"


if __name__ =="__main__":
    app.run(debug=True, port=90)