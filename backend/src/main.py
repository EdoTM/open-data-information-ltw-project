from flask import request
from database import *
from flask_setup import app
from utils.utils import *
from hashlib import md5


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password_hash = data["password"]

    try:
        user = db.get_user_by_email(email)
    except UserNotFound:
        return make_error_response("User not found", 404)
    if user["password_md5"] != password_hash:
        return make_error_response("Wrong password", 401)

    return make_login_success_response(user)


@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    email = data["email"]
    username = data["username"]
    password_hash = data["password"]
    birthdate = data["birthdate"]
    profile_pic = f"https://www.gravatar.com/avatar/{md5(email.encode()).digest().hex()}?d=retro"
    try:
        user = db.register_user_and_get_info(email, username, password_hash, birthdate, profile_pic)
        return make_login_success_response(user)
    except EmailAlreadyExists:
        return make_error_response("Email already exists", 409)
    except UserAlreadyExists:
        return make_error_response("Username already exists", 409)
    except Exception:
        return make_error_response("Unknown error", 500)


@app.route("/api/userInfo", methods=["GET"])
def get_user_info():
    session_id = request.cookies.get("sessionID")

    try:
        user = get_user_from_session_id(session_id)
    except UserNotFound:
        resp = make_error_response("User not found", 404)
        resp.set_cookie("sessionID", "", expires=0)
        return resp
    except WrongSignature:
        resp = make_error_response("Wrong signature", 401)
        resp.set_cookie("sessionID", "", expires=0)
        return resp
    return make_login_success_response(user)


@app.route("/api/getPosts", methods=["GET"])
def get_posts():
    try:
        user = get_user_from_session_id(request.cookies.get("sessionID"))
        email = user["email"]
    except (UserNotFound, WrongSignature):
        email = ""

    posts = db.get_posts_for_user(email)
    ret = []
    for post in posts:
        author_user = db.get_user_by_email(post["author_email"])
        ret.append({
            "id": post["id"],
            "title": post["title"],
            "content": post["content"],
            "score": post["score"],
            "authorUsername": author_user["username"],
            "authorProfilePic": author_user["profile_pic"],
            "postImage": post["img"],
            "userVote": post["userVote"],
            "starred": bool(post["starred"]),
            "timestamp": post["timestamp"]
        })
    return ret


@app.route("/api/createPost", methods=["POST"])
def create_post():
    data = request.json
    session_id = request.cookies.get("sessionID")
    try:
        user = get_user_from_session_id(session_id)
    except (UserNotFound, WrongSignature):
        return make_error_response("User not found", 404)
    title = data["title"]
    content = data["content"]
    img = data["postImage"]

    db.create_post(user["email"], title, content, img)
    return make_response("Post created", 200)


@app.route("/api/votePost", methods=["POST"])
def vote_post():
    data = request.json
    session_id = request.cookies.get("sessionID")
    try:
        user = get_user_from_session_id(session_id)
    except (UserNotFound, WrongSignature):
        return make_error_response("User not found", 404)
    post_id = data["postID"]
    vote = data["vote"]

    db.vote_post(user["email"], post_id, vote)
    return make_response("Post voted", 200)

@app.route("/api/plot/meetings", methods=["POST"])
def plot_meetings():
    response = {
        'xAxisValues': [],
        'elements': []
    }
    elements = request.json.get("elements")
    index = request.json.get("index")
    if index == "nation":
        all_nations = [x["nation"] for x in db.get_all_nations()]
    else:
        all_nations = [x["company"] for x in db.get_all_companies()]

    response['xAxisValues'] = all_nations
    
    for element in elements:
        name = element["name"]
        color = element["color"]
        category = element["currentCategory"] # da sistemare
        wg = parse_category(category)
        data = db.count_meetings(index, wg)
        data = {x[index]: x["cnt"] for x in data}
        data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}

        response['elements'].append({
            'name': name,
            'color': color,
            'data': [data.get(x, 0) for x in all_nations]
        })
    return response
        

@app.route("/api/starPost", methods=["POST"])
def star_post():
    data = request.json
    session_id = request.cookies.get("sessionID")
    try:
        user = get_user_from_session_id(session_id)
    except (UserNotFound, WrongSignature):
        return make_error_response("User not found", 404)
    post_id = data["postID"]
    starred = data["starred"]
    db.star_post(user["email"], post_id, starred)
    return make_response("Post starred", 200)


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
