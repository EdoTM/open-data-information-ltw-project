from flask import request
from database import *
from flask_setup import app
from utils.utils import *


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password_hash = data["password"]

    try:
        user = db.get_user_by_email(email)
    except UserNotFoundError:
        return make_error_response("User not found", 404)
    if user["password_md5"] != password_hash:
        return make_error_response("Wrong password", 401)

    return make_login_success_response(user)


@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data["email"]
    username = data["username"]
    password_hash = data["password"]
    birthdate = data["birthdate"]
    try:
        user = db.register_user_and_get_info(email, username, password_hash, birthdate)
        return make_login_success_response(user)
    except EmailAlreadyExistsError:
        return make_error_response("Email already exists", 409)
    except UserAlreadyExistsError:
        return make_error_response("Username already exists", 409)
    except Exception:
        return make_error_response("Unknown error", 500)


@app.route("/userInfo", methods=["GET"])
def get_user_info():
    session_id = request.args.get("sessionID")
    try:
        user = get_user_from_session_id(session_id)
    except UserNotFoundError:
        return make_error_response("User not found", 404)
    return make_login_success_response(user)


def start_app():
    global app
    debug = "DEBUG" in os.environ
    debug = True  # to be removed in production
    host = "127.0.0.1" if "LOCAL" in os.environ else "0.0.0.0"
    port = os.environ.get("PORT", 5000)
    app.run(debug=debug, host=host, port=port)


if __name__ == "__main__":
    db = Database.get_instance()
    start_app()
