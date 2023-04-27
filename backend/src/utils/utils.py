from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import bytes_to_long, long_to_bytes 
from hashlib import sha256
from flask_setup import app
from flask import make_response
from database import Database
from utils.errors import *
import os


def generate_user_session_id(input_email: str):
    IV = os.urandom(16)
    cipher = AES.new(app.config["SECRET_KEY"], IV=IV, mode=AES.MODE_CBC)
    rsa_priv_key = app.config["RSA_PRIV_KEY"]

    session_id_plaintext = input_email
    session_id_ciphertext = IV.hex() + cipher.encrypt(pad(session_id_plaintext.encode(), AES.block_size)).hex()
    
    hashed_msg = bytes_to_long(sha256(session_id_plaintext.encode()).digest())
    
    signature = pow(hashed_msg, rsa_priv_key.d, rsa_priv_key.n)

    return  session_id_ciphertext + '-' + long_to_bytes(signature).hex()


def get_user_from_session_id(session_id: str):
    db = Database.get_instance()
    try:
        IV = bytes.fromhex(session_id[:32])
        cipher = AES.new(app.config["SECRET_KEY"], IV=IV, mode=AES.MODE_CBC)

        session_id_ciphertext = session_id[32:].split('-')[0]
        signature = session_id[32:].split('-')[1]

        session_id_plaintext = unpad(cipher.decrypt(bytes.fromhex(session_id_ciphertext)), AES.block_size).decode()

        hashed_msg = bytes_to_long(sha256(session_id_plaintext.encode()).digest())
        rsa_pub_key = app.config["RSA_PRIV_KEY"].publickey()
        if pow(bytes_to_long(bytes.fromhex(signature)), rsa_pub_key.e, rsa_pub_key.n) != hashed_msg:
            raise UserNotFoundError()


    except ValueError as e:
        if "Padding is incorrect" in str(e):
            raise UserNotFoundError()
        if "non-hexadecimal number found in fromhex() arg at position" in str(e):
            raise UserNotFoundError()
        print(e)
        raise ValueError()
    
    email = session_id_plaintext
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
