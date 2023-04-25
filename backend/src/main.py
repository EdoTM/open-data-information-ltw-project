from flask import Flask, request, make_response
from flask_cors import CORS
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(32)
CORS(app)

def generate_cookie(input_email):
    cipher = AES.new(app.config["SECRET_KEY"], AES.MODE_ECB)
    session_id = cipher.encrypt(pad(input_email.encode(), AES.block_size)).hex()
    return session_id

def get_user_from_cookie(input_cookie):
    cipher = AES.new(app.config["SECRET_KEY"], AES.MODE_ECB)
    email = unpad(cipher.decrypt(bytes.fromhex(input_cookie)), AES.block_size).decode()
    return email

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password_md5 = data["password"]

    
    resp = make_response()
    session_id = generate_cookie(email)
    resp.set_cookie("sessionID", session_id)

    print(get_user_from_cookie(session_id))

    return resp

    

def start_api():
    global app
    debug = "DEBUG" in os.environ
    debug = True  # to be removed in production
    host = "127.0.0.1" if "LOCAL" in os.environ else "0.0.0.0"
    port = os.environ.get("PORT", 5000)
    app.run(debug=debug, host=host, port=port)


if __name__ == "__main__":
    start_api()
