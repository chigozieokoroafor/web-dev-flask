from flask import Flask, request, Response, render_template, jsonify, session, redirect,url_for
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
import uuid
import jwt
from datetime import datetime, timedelta
from functools import wraps
import pymongo
import json



mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=100000)
mongo.server_info()
db = mongo.todo_users
User  = db.users
#manager = LoginManager()

app = Flask(__name__)
CORS(app, resources={r"/": {"origin": "*"}})
bcrypt = Bcrypt(app) 
app.config["SECRET_KEY"] ="youcannotguessit"
secret_key = "youcannotguessit"
#manager.init_app(app)



#@manager.user_loader
#def load_user(_id):
#    return 


@app.route("/home")
#@login_required
def home():
    if "email" in session:
        return Response("welcome " + session["username"], 200)
    return render_template("home.html", template_folder="templates")



@app.route("/signin", methods = ["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        check_user = User.find_one({"email":email})
        if check_user:
            if check_password_hash(check_user["password"],password):
                #return Response(json.dumps({"message":"continue with this id", "status":"success"}), 200)
                session["username"] = check_user["username"]
                print(check_user["username"])
                return redirect(url_for("home"))
    return render_template("signin.html", template_folder = "templates")            
            


@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method =="POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        time = datetime.utcnow()
        hashed = generate_password_hash(password)
        new_user = {"email":email, "username": username, "password":hashed, "time created":time}
        access = {"email":email, "password":password}
        dbResponse = db.users.insert_one(new_user)
        return Response(json.dumps({"message": "user created", "status":"Success", "token":jwt.encode(access, secret_key, algorithm="HS256")}))
        #login_user(access)
    return render_template("signup.html")












if __name__ =="__main__":
    
    app.run(debug=True, port=80)