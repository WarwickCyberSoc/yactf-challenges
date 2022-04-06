from flask import Flask, render_template, g, request, flash, redirect, url_for
import sqlite3
import os
import argon2

app = Flask(__name__, static_folder="static", static_url_path="/s/")
app.config["SECRET_KEY"] = os.urandom(64)

DATABASE = "./database.db"

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, isolation_level=None)
        db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def hash_password(password):
    ph = argon2.PasswordHasher()
    return ph.hash(password)

def verify_password(hash, password):
    try:
        ph = argon2.PasswordHasher()
        return ph.verify(hash, password)
    except argon2.exceptions.Argon2Error:
        return False

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Ensure no leaking
@app.after_request
def remove_headers(response):
    response.headers.remove("X-Powered-By")
    return response

@app.route("/")
def index():
    return render_template("index.html", services=query_db("SELECT * FROM services"), conv_rate=144.59)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", None)
    password = request.form.get("password", None)

    if username is None or password is None:
        flash("Missing username or password", "error")
        return redirect(url_for("login"))

    user = query_db("SELECT * FROM users WHERE username = ?", (username,), one=True)

    if user is None:
        flash("Username or password invalid", "error")
        return redirect(url_for("login"))

    if not verify_password(user["password"], password):
        flash("Username or password invalid", "error")
        return redirect(url_for("login"))

    auth_token = os.urandom(32).hex()

    response = redirect(url_for("form"))
    response.set_cookie("s", auth_token)

    query_db("UPDATE users SET auth_token = ? WHERE username = ?", (auth_token, username))

    return response

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username", None)
    password = request.form.get("password", None)

    if username is None or password is None:
        flash("Missing username or password", "error")
        return redirect(url_for("register"))

    existing = query_db("SELECT * FROM users WHERE username = ?", (username,), one=True)

    if existing is not None:
        flash("User already exists", "error")
        return redirect(url_for("register"))

    if not (4 < len(username) < 32) or not(4 < len(password) < 128):
        flash("Username or password invalid, must be longer than 4 characters", "error")
        return redirect(url_for("register"))

    password = hash_password(password)
    query_db("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

    flash("Account created", "success")
    return redirect(url_for("login"))

@app.route("/form", methods=["GET", "POST"])
def form():
    auth_token = request.cookies.get("s", None)
    if not auth_token:
        flash("Must be authenticated", "error")
        return redirect("/login")

    user = query_db("SELECT * FROM users WHERE auth_token = ?", (auth_token,), one=True)
    if user is None:
        flash("Must be authenticated", "error")
        return redirect("/login")
    
    if request.method == "GET":
        return render_template("form.html", services=query_db("SELECT * FROM services"))

    flash("Were currently not accepting new requests, check soon later", "error")
    return redirect(url_for("form"))

@app.route("/logout")
def logout():
    auth_token = request.cookies.get("s", None)
    if not auth_token:
        return redirect("/login")

    response = redirect("/login")
    response.set_cookie("s", "")

    return response

@app.errorhandler(Exception)
def handle_exception(e):
    return render_template("error.html"), 400

if __name__ == "__main__":
    init_db()
    app.run(host='127.0.0.1')