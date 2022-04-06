import os
from emails import send_email

from email.utils import formatdate
from flask import Flask, render_template, request, session, g
from flask.helpers import url_for
from flask.wrappers import Response
from werkzeug.utils import redirect

app = Flask(__name__, static_url_path="/assets", static_folder="./assets")
app.secret_key = (
    "TEST_KEY" if os.getenv("FLASK_ENV") == "development" else os.urandom(64)
)

from middleware import is_authenticated


@app.before_request
def before_request_func():
    g.user = None

    if session.get("user_id") is None:
        return

    g.user = query_db(
        "SELECT * FROM users WHERE id = ?",
        (session["user_id"],),
        one=True,
    )


def get_admin_user(magic_code=None):
    if hasattr(g, "user") and g.user is not None and g.user["is_admin"]:
        return g.user

    if magic_code is None:
        return None

    admin_user = query_db(
        "SELECT * FROM users WHERE magic_code = ? AND is_admin = 1",
        (magic_code,),
        one=True,
    )

    return admin_user


@app.route("/")
def index_page():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "GET":
        return render_template("signup.html")

    if request.form.get("username") is None or request.form.get("password") is None:
        return render_template("signup.html", error="Missing username or password")

    username = request.form["username"]
    password = request.form["password"]
    if not username.isalnum() or not (4 <= len(username) <= 32):
        return render_template(
            "signup.html",
            error="Your username must be between alpha-numeric and be between 4 and 32 characters.",
        )

    if not password.isalnum() or not (4 <= len(password) <= 32):
        return render_template(
            "signup.html",
            error="Your password must be between alpha-numeric and be between 4 and 32 characters.",
        )

    existing_user = query_db(
        "SELECT * FROM users WHERE username = ?", (username,), one=True
    )
    if existing_user is not None:
        return render_template(
            "signup.html", error="That username already exists, try another one!"
        )

    # TODO: Remember to hash passwords for production!
    query_db(
        "INSERT INTO users (username, password, is_admin) VALUES (?,?,?)",
        (username, password, 0),
    )

    return redirect(url_for("login_page"))


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        return render_template("login.html")

    if request.form.get("username") is None or request.form.get("password") is None:
        return render_template("login.html", error="Missing username or password")

    username = request.form["username"]
    password = request.form["password"]

    user = query_db(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password),
        one=True,
    )

    if user is None:
        return render_template("login.html", error="Invalid username or password")

    session["user_id"] = user["id"]

    return redirect(url_for("view_blog_page", username=user["username"]))


@app.route("/logout")
def logout_page():
    session.clear()

    return redirect(url_for("index_page"))


@app.route("/blog/<username>")
def view_blog_page(username):

    user = query_db("SELECT * FROM users WHERE username = ?", (username,), one=True)
    if user is None:
        if g.user is not None:
            return redirect(url_for("view_blog_page", username=g.user["username"]))
        else:
            return redirect(url_for("index_page"))

    content = user["blog_content"]
    style = user["blog_styling"]
    is_reviewing = False

    if (
        request.args.get("reviewing")
        and get_admin_user(request.args.get("magic_code")) is not None
    ):
        # if we're reviewing their submission, show their unapproved content instead
        content = user["unapproved_blog_content"]
        style = user["unapproved_blog_styling"]
        is_reviewing = True

    formatted = render_template(
        "blog.html",
        style=style,
        content=content
        or "<h1>It seems like this user hasn't wrote anything yet!</h1>",
        name=username,
        is_reviewing=is_reviewing,
        is_self=hasattr(g, "user")
        and g.user is not None
        and g.user["username"] == username,
        magic_code=request.args.get("magic_code"),
    )

    response = Response(formatted)
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers[
        "Content-Security-Policy"
    ] = "default-src 'none'; style-src * 'self' data: 'unsafe-inline' 'unsafe-hashes'; style-src-elem * 'self' data: 'unsafe-inline' 'unsafe-hashes'; style-src-attr * 'self' data: 'unsafe-inline' 'unsafe-hashes'; img-src *; font-src *; media-src *"

    return response


@app.route("/edit", methods=["GET", "POST"])
@is_authenticated()
def edit_blog_page():
    if request.method == "GET":
        # We do a redirect to avoid that annoying browser prompt, so we set the success message here
        if request.args.get("success", ""):
            success = "Your blog post is now being reviewed by one of our dedicated members of staff. We'll make sure your blog post gets published as soon as possible!"

        return render_template("edit.html", user=g.user, success=success)

    content = request.form.get("content", "")
    style = request.form.get("style", "")

    if g.user["being_reviewed"]:
        return render_template(
            "edit.html",
            user=g.user,
            error="Your last submission is currently being reviewed!",
        )

    query_db(
        "UPDATE users SET unapproved_blog_content = ?, unapproved_blog_styling = ?, being_reviewed = ? WHERE id = ?",
        (content, style, 0, g.user["id"]),
    )

    send_email(
        "new_submission",
        "support_katie",
        {
            "username": g.user["username"],
        },
    )

    # We have to repoll user here to get the updated unapproved blog content and styling
    user = query_db("SELECT * FROM users WHERE id = ?", (g.user["id"],), one=True)

    return redirect(url_for("edit_blog_page", success="1"))


@app.route("/approve/<username>", methods=["POST"])
def approve_change(username):
    user = query_db("SELECT * FROM users WHERE username = ?", (username,), one=True)
    if user is None:
        return "Could not find user"

    admin_user = get_admin_user(request.form.get("magic_code"))
    if admin_user is None:
        return "You must be logged in / provide a valid magic code"

    query_db(
        "UPDATE users SET blog_content = ?, blog_styling = ?, unapproved_blog_content = ?, unapproved_blog_styling = ?, being_reviewed = ?, last_approval_time = ? WHERE username = ?",
        (
            user["unapproved_blog_content"],
            user["unapproved_blog_styling"],
            "",
            "",
            0,
            formatdate(usegmt=True),
            username,
        ),
    )

    query_db(
        "UPDATE users SET magic_code = ? WHERE id = ?",
        (os.urandom(16).hex(), admin_user["id"]),
    )

    return "Updated user page"


@app.route("/disapprove/<username>", methods=["POST"])
@is_authenticated()
def disapprove_change(username):
    user = query_db("SELECT * FROM users WHERE username = ?", (username,), one=True)
    if user is None:
        return "Could not find user"

    admin_user = get_admin_user(request.form.get("magic_code"))
    if admin_user is None:
        return "You must be logged in / provide a valid magic code"

    query_db(
        "UPDATE users SET unapproved_blog_content = ?, unapproved_blog_styling = ?, being_reviewed = ? WHERE username = ?",
        ("", "", 0, username),
    )

    query_db(
        "UPDATE users SET magic_code = ? WHERE id = ?",
        (os.urandom(16).hex(), admin_user["id"]),
    )

    return "Removed user submission"


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    # As we haven't got our mail API access, let support manually reset passwords
    if request.method == "GET":
        return render_template("forgot.html")

    username = request.form.get("username")

    user = query_db("SELECT * FROM users WHERE username = ?", (username,), one=True)
    if user is None:
        return render_template(
            "forgot.html",
            error="Could not find this user",
        )

    send_email(
        "password_reset",
        "support_katie",
        {
            "username": username,
            "new_password": request.form.get("password"),
        },
    )

    return render_template(
        "forgot.html",
        success="One of our support staff will check your details and reset your password ASAP!",
    )


@app.route("/password_reset", methods=["GET", "POST"])
def password_reset():
    if request.remote_addr != "127.0.0.1":
        return "In development, please contact support for password resets.", 401

    username = request.args.get("username")
    new_password = request.args.get("new_password")
    magic_code = request.args.get("magic_code")

    user = query_db("SELECT * FROM users WHERE username = ?", (username,), one=True)
    if user is None:
        return "Could not find user", 404

    admin_user = get_admin_user(magic_code)
    if admin_user is None:
        return "You must be logged in / provide a valid magic code", 401

    query_db(
        "UPDATE users SET password = ? WHERE username = ?", (new_password, username)
    )

    return "Updated password!"


@app.route("/flag")
@is_authenticated()
def get_flag():
    if not g.user["is_admin"]:
        return "You must be admin!"

    if os.path.exists("../flag.txt"):
        with open("../flag.txt", "r") as flag_file:
            return flag_file.read()
    else:
        return "Would have printed flag, but the flag.txt does not exist"


if __name__ == "__main__":
    from database import init_db, query_db

    # Initialise the database
    init_db()

    app.run("0.0.0.0", port=5000, debug=os.getenv("FLASK_ENV") == "development")
