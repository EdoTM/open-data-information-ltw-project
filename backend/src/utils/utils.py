from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import bytes_to_long, long_to_bytes 
from hashlib import sha256
from flask_setup import app
from flask import make_response
from database import Database
from utils.errors import *
import os

def __check_signature(message, signature):
    rsa_key = app.config["RSA_PRIV_KEY"]
    hashed_msg = bytes_to_long(sha256(message.encode()).digest())

    return pow(bytes_to_long(bytes.fromhex(signature)), rsa_key.e, rsa_key.n) == hashed_msg

def __sign_message(message):
    rsa_key = app.config["RSA_PRIV_KEY"]
    hashed_msg = bytes_to_long(sha256(message.encode()).digest())
    return long_to_bytes(pow(hashed_msg, rsa_key.d, rsa_key.n)).hex()

def generate_user_session_id(input_email: str):
    IV = os.urandom(16)
    cipher = AES.new(app.config["SECRET_KEY"], IV=IV, mode=AES.MODE_CBC)

    session_id_plaintext = input_email
    session_id_ciphertext = cipher.encrypt(pad(session_id_plaintext.encode(), AES.block_size)).hex()
    
    return IV.hex() + session_id_ciphertext + '-' + __sign_message(session_id_ciphertext)


def get_user_from_session_id(session_id: str):
    if session_id is None:
        raise UserNotFound()
    db = Database.get_instance()
    IV = bytes.fromhex(session_id[:32])
    session_id_ciphertext = session_id[32:].split('-')[0]
    signature = session_id.split('-')[1]

    if not __check_signature(session_id_ciphertext, signature):
        raise WrongSignature()

    try:
        cipher = AES.new(app.config["SECRET_KEY"], IV=IV, mode=AES.MODE_CBC)
        session_id_plaintext = unpad(cipher.decrypt(bytes.fromhex(session_id_ciphertext)), AES.block_size).decode()

    except ValueError as e:
        if "Padding is incorrect" in str(e):
            raise UserNotFound()
        if "non-hexadecimal number found in fromhex() arg at position" in str(e):
            raise UserNotFound()
        raise e
    
    email = session_id_plaintext
    user = db.get_user_by_email(email)
    return user


def make_login_success_response(user):
    resp_data = {
        "status": "success",
        "email": user["email"],
        "username": user["username"],
        "profilePic": user["profile_pic"]
    }

    resp = make_response(resp_data)
    session_id = generate_user_session_id(user["email"])
    resp.set_cookie("sessionID", session_id)
    return resp


def make_error_response(error_msg, error_code):
    resp_data = {"status": "error", "error": error_msg}
    return make_response(resp_data, error_code)


def check_filter_validity(filters):
    for filter in filters:
            if filter.key not in ["meetingID", "tsg", "wg", "tdoc"]: # whitelistiamo i filtri che vogliamo accettare
                raise InvalidFilterKey()
            
def wrap_graph(graph, elements):
    """
    From [{"tsg1": 10, "tsg2": 7, ...},{"tsg1": 3, "tsg2": 4, ...}, ...]
    Output is [{"key":"tsg1", "elementName1": 10, "elementName2": 7, ...}, ...]
    """
    keys = set()
    for i in graph:
        keys.update(i.keys())
    output = {}
    for group in keys:
        output[group] = {"key": group}
        for i, element in enumerate(elements):
            output[group][element.elementName] = 0

    for i, element in enumerate(elements):
        elementName = element.elementName
        for group in graph[i].keys():
            output[group][elementName] = graph[i][group]

    # alphabetical order on first element value
    output = dict(sorted(output.items(), key=lambda item: item[1][elements[0].elementName], reverse=True))
    return list(output.values())

