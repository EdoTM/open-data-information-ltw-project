from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from flask_setup import app
from flask import make_response
from database import Database


def generate_user_session_id(input_email: str):
    cipher = AES.new(app.config["SECRET_KEY"], AES.MODE_ECB)
    session_id = cipher.encrypt(pad(input_email.encode(), AES.block_size)).hex()
    return session_id


def get_user_from_session_id(session_id: str):
    db = Database.get_instance()
    cipher = AES.new(app.config["SECRET_KEY"], AES.MODE_ECB)
    email = unpad(cipher.decrypt(bytes.fromhex(session_id)), AES.block_size).decode()
    user = db.get_user_by_email(email)
    return user


def make_login_success_response(user):
    resp_data = {
        "status": "success",
        "email": user["email"],
        "username": user["username"],
    }

    resp = make_response(resp_data)
    session_id = generate_user_session_id(user["email"])
    resp.set_cookie("sessionID", session_id)
    return resp


def make_error_response(error_msg, error_code):
    resp_data = {"status": "error", "error": error_msg}
    return make_response(resp_data, error_code)
