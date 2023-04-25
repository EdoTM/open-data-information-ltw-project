from flask import Flask, request, make_response
from flask_cors import CORS
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from database import *

app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(32)
CORS(app, supports_credentials=True, origins=["http://localhost:*"])


def generate_cookie(input_email: str):
    cipher = AES.new(app.config["SECRET_KEY"], AES.MODE_ECB)
    session_id = cipher.encrypt(pad(input_email.encode(), AES.block_size)).hex()
    return session_id


def get_user_from_cookie(input_cookie: str):
    cipher = AES.new(app.config["SECRET_KEY"], AES.MODE_ECB)
    email = unpad(cipher.decrypt(bytes.fromhex(input_cookie)), AES.block_size).decode()
    return email

def generate_success_resp(user):
    resp_data = {
        "status": "success",
        "email":  user["email"],
        "username": user["username"],
    }

    resp = make_response(resp_data)
    session_id = generate_cookie(user["email"])
    resp.set_cookie("sessionID", session_id)
    return resp

def make_error_resp(error):
    resp_data = {"status": "error", "error": error}
    return make_response(resp_data, 401)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password_md5 = data["password"]

    try:
        user = db.get_user_by_email(email)
    except UserNotFoundError:
        return make_error_resp("User not found")
        
    
    if user["password_md5"] != password_md5:
        return make_error_resp("Wrong password")
    
    return generate_success_resp(user)
    


@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data["email"]
    username = data["username"]
    password_md5 = data["password"]
    birthday = data["birthday"]
    user = db.store_user(email, username, password_md5, birthday)

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
