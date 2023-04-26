from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from flask_setup import app
from flask import make_response
from database import Database
from utils.errors import *


def generate_user_session_id(input_email: str):
    cipher = AES.new(app.config["SECRET_KEY"], AES.MODE_ECB)
    session_id = cipher.encrypt(pad(input_email.encode(), AES.block_size)).hex()
    return session_id


def get_user_from_session_id(session_id: str):
    db = Database.get_instance()
    cipher = AES.new(app.config["SECRET_KEY"], AES.MODE_ECB)
    try:
        email = unpad(cipher.decrypt(bytes.fromhex(session_id)), AES.block_size).decode()
    except ValueError as e:
        if "Padding is incorrect" in str(e):
            raise UserNotFoundError()
        if "non-hexadecimal number found in fromhex() arg at position" in str(e):
            raise UserNotFoundError()
        print(e)
        raise ValueError()
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
