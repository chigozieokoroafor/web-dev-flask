from flask import Flask, request, Response, render_template, jsonify, session, redirect,url_for
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
#from bson import ObjectId
#import uuid
#import jwt
from datetime import date, datetime, timedelta
from functools import wraps
import pymongo
import json



mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=100000)
mongo.server_info()
db = mongo.todo_users
User  = db.users
Notes = db.notes
#login_manager = LoginManager()

app = Flask(__name__)
CORS(app, resources={r"/": {"origin": "*"}})
bcrypt = Bcrypt(app) 
app.config["JWT_SECRET_KEY"] ="youcannotguessit"
app.config["SECRET_KEY"] = "youcanneverguessit"
secret_key = "youcannotguessit"
jwt = JWTManager(app)
#login_manager.init_app(app)





@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    #if "username" in session :
    try:
        if session["logged_in"]==True:
            #return ("welcome " + session["username"], 200)
            access = {"username":session["username"]}
            access_token = create_access_token(identity=access)
            if request.method == "POST":
                note = request.form.get("notes")
                note_dict = {"email":User.find_one({"username":session["username"]})["email"], "notes":note}
                Notes.insert_one(note_dict)
            
                note_list = []
                for note_ in Notes.find({"email":User.find_one({"username":session["username"]})["email"]}):
                    #return (note_["notes"])
                    note_list.append(note_["notes"])
                #return jsonify(note_list)
                return render_template("home.html", template_folder="templates", tasks=note_list)
            return render_template("home.html", template_folder="templates", token=access_token)
            #return Response(json.dumps({"message": "welcome"+" "+f"{session['username']}", "status":"Success", "token":access_token}))
        
        else:
            return render_template("home.html", template_folder="templates")
            #return jsonify({"message": "please login", "status":"neutral"})
    except:
        #return render_template('home.html')
        return "an error occured"
    



@app.route("/signin", methods = ["GET", "POST"]) 
#login_manager.request_loader
def signin():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
            
        check_user = User.find_one({"email":email})
        if check_user: 
            if check_password_hash(check_user["password"],password):
                session["username"] = check_user["username"]
                access_token = create_access_token(identity={"email":email})
                session["logged_in"] = True
                #return json.dumps({"message": "welcome"+" "+check_user["username"], "status":"Success", "token":access_token})
                return redirect(url_for("home"))            
            password_message = json.dumps({"message":"incorrect password", "status":"error"})
            return (password_message)
        message = json.dumps({"message":"user not found", "status":"error"})
        return message

        #return redirect(url_for("signin"))            
    return render_template("signin.html", template_folder="templates")
    #return Response("please signin using postman", 200)
            


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
        access_token = create_access_token(identity={"email":email})
        session["logged_in"] = True
        #return json.dumps({"message": "user created", "status":"Success", "token":access_token})
        return redirect(url_for(endpoint="home"))
        
    return render_template("signup.html")

@app.route("/logout")
def logout():
    if "username" in session:
        session["logged_in"] = False
        return redirect(url_for(endpoint ="home"))
    else:
        return "no user in session", 401
    #return home()
    

@app.route("/test")
@jwt_required()
def test():
    user_jwt = get_jwt_identity()
    print(user_jwt)
    return "Secret Data", 200
    






if __name__ =="__main__":
    
    app.run(debug=True, port=80)