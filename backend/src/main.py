from functools import wraps
from hashlib import md5

from flask import request

from utils.utils import *


def get_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session_id = request.cookies.get("sessionID")
        try:
            user = get_user_from_session_id(session_id)
        except (UserNotFound, WrongSignature):
            return func(None, *args, **kwargs)

        return func(user, *args, **kwargs)

    return wrapper


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
    except Exception as e:
        return make_error_response(f"Unknown error {str(e)}", 500)


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


@app.route("/api/profile/<username>", methods=["GET"])
def get_user_by_username(username):
    username = username.replace("@", "")
    try:
        user = db.get_user_by_username(username)
    except UserNotFound:
        return make_error_response("User not found", 404)
    posts = get_user_posts(user["email"])
    score = db.get_user_score(user["email"])
    user["posts"] = posts
    user["postCount"] = len(posts)
    user["score"] = score
    return make_response(user, 200)

@app.route("/api/getAllUsers", methods=["GET"])
def get_all_users():
    users = db.get_all_users()
    return make_response(users, 200)

@app.route("/api/editUser", methods=["POST"])
@get_user
def edit_user(user):
    if user is None:
        return make_error_response("User not found", 404)
    data = request.json
    birthdate = data.get("birthdate", user["birthday"])
    bio = data.get("bio", user["bio"])
    cv = data.get("cv", user["cv"])

    db.edit_user(user["email"], birthdate, bio, cv)
    return make_response("User edited", 200)


def get_user_posts(email):
    posts = db.get_user_posts(email)
    return wrap_posts(posts)


@app.route("/api/getPosts", methods=["GET"])
@get_user
def get_posts(user):
    email = ""
    if user is not None:
        email = user["email"]

    posts = db.get_posts_for_user(email)
    return wrap_posts(posts)


@app.route("/api/getFavoritePosts", methods=["GET"])
@get_user
def get_favorite_posts(user):
    email = ""
    if user is not None:
        email = user["email"]

    posts = db.get_favorite_posts_for_user(email)
    return wrap_posts(posts)


@app.route("/api/getHiddenPosts", methods=["GET"])
@get_user
def get_hidden_posts(user):
    email = ""
    if user is not None:
        email = user["email"]

    posts = db.get_hidden_posts_for_user(email)
    return wrap_posts(posts)


def wrap_posts(posts):
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
            "timestamp": post["timestamp"],
            "hidden": bool(post["hidden"]),
            "commentCount": post["comment_count"]
        })
    return ret


@app.route("/api/createPost", methods=["POST"])
@get_user
def create_post(user):
    data = request.json
    if user is None:
        return make_error_response("User not found", 404)
    title = data["title"]
    content = data["content"]
    img = data["postImage"]

    db.create_post(user["email"], title, content, img)
    return make_response("Post created", 200)


@app.route("/api/votePost", methods=["POST"])
@get_user
def vote_post(user):
    data = request.json
    if user is None:
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
    elif index == "company":
        all_nations = [x["company"] for x in db.get_all_companies()]
    else:
        return make_error_response("Invalid index", 404)

    is_sorted = False
    for element in elements:
        name = element["name"]
        color = element["color"]
        category = element["currentCategory"]  # da sistemare
        wg = parse_category(category)
        data = db.count_meetings(index, wg)
        data = {x[index]: x["cnt"] for x in data}

        if not is_sorted:
            all_nations = sorted(all_nations, key=lambda x: data.get(x, 0), reverse=True)
            is_sorted = True

        response['elements'].append({
            'name': name,
            'color': color,
            'data': [data.get(x, 0) for x in all_nations]
        })

    response['xAxisValues'] = all_nations

    return response


@app.route("/api/plot/tdocs", methods=["POST"])
def plot_tdocs():
    elements = request.json.get("elements")
    index = request.json.get("index")
    response = {
        'xAxisValues': [],
        'elements': []
    }
    if index == "nation":
        all_nations = [x["nation"] for x in db.get_all_nations()]
    elif index == "company":
        all_nations = [x["company"] for x in db.get_all_companies()]
    else:
        return make_error_response("Invalid index", 404)

    is_sorted = False
    for element in elements:
        name = element["name"]
        color = element["color"]
        tdoc_filter = element["tdocFilter"]
        wg = parse_category(element["currentCategory"])
        data = db.count_tdocs(index, tdoc_filter, wg)
        data = {x[index]: x["cnt"] for x in data}
        data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
        if not is_sorted:
            all_nations = sorted(all_nations, key=lambda x: data.get(x, 0), reverse=True)
            is_sorted = True
        response['elements'].append({
            'name': name,
            'color': color,
            'data': [data.get(x, 0) for x in all_nations]
        })

    response['xAxisValues'] = all_nations
    return response


@app.route("/api/starPost", methods=["POST"])
@get_user
def star_post(user):
    data = request.json
    if user is None:
        return make_error_response("User not found", 404)
    post_id = data["postID"]
    starred = data["starred"]
    db.star_post(user["email"], post_id, starred)
    return make_response("Post starred", 200)


@app.route("/api/hidePost", methods=["POST"])
@get_user
def hide_post(user):
    data = request.json
    if user is None:
        return make_error_response("User not found", 404)
    post_id = data["postID"]
    hidden = data["hidden"]
    db.hide_post(user["email"], post_id, hidden)
    return make_response("Post hidden", 200)


@app.route("/api/newComment", methods=["POST"])
@get_user
def comment(user):
    data = request.json
    if user is None:
        return make_error_response("User not found", 404)
    post_id = data["postID"]
    content = data["content"]
    db.comment(user["email"], post_id, content)
    return make_response("Comment created", 200)


@app.route("/api/getComments/<int:post_id>", methods=["GET"])
@get_user
def get_comments(user, post_id):
    email = ''
    if user is not None:
        email = user["email"]
    comments = db.get_comments_for_post(post_id, email)
    return comments, 200


@app.route("/api/like/<int:comment_id>", methods=["GET"])
@get_user
def like_comment(user, comment_id):
    if user is None:
        return make_error_response("User not found", 404)
    db.like_comment(user["email"], comment_id)
    return make_response("Comment liked", 200)


@app.route("/api/unlike/<int:comment_id>", methods=["GET"])
@get_user
def unlike_comment(user, comment_id):
    if user is None:
        return make_error_response("User not found", 404)
    db.unlike_comment(user["email"], comment_id)
    return make_response("Comment unliked", 200)


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
