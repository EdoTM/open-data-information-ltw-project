from flask import Flask, request
import os
from database import *
from flask_setup import app
from utils.utils import generate_success_resp, make_error_resp, get_user_from_cookie



@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password_md5 = data["password"]

    try:
        user = db.get_user_by_email(email)
    except UserNotFoundError:
        return make_error_resp("User not found", 404)
        
    
    if user["password_md5"] != password_md5:
        return make_error_resp("Wrong password", 401)
    
    return generate_success_resp(user)
    


@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data["email"]
    username = data["username"]
    password_md5 = data["password"]
    birthdate = data["birthdate"]
    try:
        user = db.store_user(email, username, password_md5, birthdate)
        return generate_success_resp(user)
    except EmailAlreadyExistsError:
        return make_error_resp("Email already exists", 409)
    except UserAlreadyExistsError:
        return make_error_resp("Username already exists", 409)
    except:
        return make_error_resp("Unknown error", 500)


@app.route("/userInfo", methods=["GET"])
def get_user_info():
    sessionID = request.args.get("sessionID")
    user = get_user_from_cookie(sessionID)
    return generate_success_resp(user)



def start_api():
    global app
    debug = "DEBUG" in os.environ
    debug = True  # to be removed in production
    host = "127.0.0.1" if "LOCAL" in os.environ else "0.0.0.0"
    port = os.environ.get("PORT", 5000)
    app.run(debug=debug, host=host, port=port)


if __name__ == "__main__":
    db = Database()
    start_api()
