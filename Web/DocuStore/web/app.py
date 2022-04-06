from pydoc import doc
from flask import Flask, render_template, redirect, request, g, flash, send_from_directory, url_for, session
from werkzeug.utils import secure_filename

import os
import sqlite3
import datetime
import hashlib
import exiftool

DATABASE = './database.db'

app = Flask(__name__)
app.config["SECRET_KEY"] = "HGKJQNBWEFIUGBVQWUHYDCZAHDGAGYWHUYIDAUYWGYIAQ"
app.config["UPLOAD_FOLDER"] = os.path.abspath("./uploads")
app.config['MAX_CONTENT_LENGTH'] = 2 * 1000 * 1000
app.permanent_session_lifetime = datetime.timedelta(days=3000)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

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

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.before_request
def load_user():
    g.user = None

    if session.get("user_id") is not None:
        g.user = query_db("SELECT * FROM users WHERE id = ?", args=(session["user_id"],), one=True)

@app.after_request
def set_csp(response):
    response.headers["Content-Security-Policy"] = "default-src 'self';"
    return response

@app.template_filter('dt')
def _jinja2_filter_datetime(date, fmt="%c"):
    return datetime.datetime.fromtimestamp(date, tz=datetime.timezone.utc).strftime(fmt)

@app.route("/file/<string:document_id>")
def download_file(document_id):
    if g.user is None:
        return "", 401
    
    document = query_db("SELECT * FROM documents WHERE id = ?", args=(document_id,), one=True)

    if document is None:
        return "", 404

    shared_entry = query_db("SELECT * FROM shared_documents WHERE document_id = ? AND shared_with = ?", args=(document_id, g.user["id"]), one=True)

    if shared_entry is None and document["owner"] != g.user["id"]:
        return "", 401

    return send_from_directory(os.path.join(app.config["UPLOAD_FOLDER"], str(document["owner"])), document["file_name"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if g.user is not None:
        return redirect(url_for("documents"))
        
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if username is None or password is None:
        flash("You must provide a username and password", "danger")
        return redirect(url_for("register"))
    
    existing_user = query_db("SELECT * FROM users WHERE username = ? AND password = ?", args=(username,password), one=True)

    if existing_user is None:
        flash("Invalid username and password!", "danger")
        return redirect(url_for("register"))

    session.permanent = True
    session["user_id"] = existing_user["id"]

    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if g.user is not None:
        return redirect(url_for("documents"))
        
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if username is None or password is None:
        flash("You must provide a username and password", "danger")
        return redirect(url_for("register"))
    
    if not (4 <= len(username) <= 32) or not (4 <= len(password) <= 32):
        flash("Your username/password must be between 4 and 32 characters.", "danger")
        return redirect(url_for("register"))
    
    existing_user = query_db("SELECT * FROM users WHERE username = ?", args=(username,), one=True)

    if existing_user is not None:
        flash("This username already exists!", "danger")
        return redirect(url_for("register"))

    query_db("INSERT INTO users (username, password) VALUES (?, ?)", args=(username, password))

    flash("You can now login!", "success")
    return redirect(url_for("login"))

@app.route("/documents/upload", methods=["GET", "POST"])
def upload_document():
    if g.user is None:
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("upload.html")

    # check if the post request has the file part
    if "file" not in request.files:
        flash("You must include a file!", "danger")
        return redirect(url_for("upload_document"))

    file = request.files["file"]

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if not file or file.filename == "":
        flash("You must include a file!", "danger")
        return redirect(url_for("upload_document"))

    file_id = hashlib.md5(os.urandom(32)).hexdigest()

    orig_name = secure_filename(file.filename)
    file_name = file_id + "_" + orig_name

    os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], str(g.user["id"])), exist_ok=True)

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(g.user["id"]), file_name)
    file.save(file_path)

    metadata = ""

    try:
        with exiftool.ExifTool() as et:
            et_data = et.get_metadata(file_path)
            
            for parameter, value in et_data.items():
                if not isinstance(value, (str, int, float)):
                    continue

                if isinstance(value, str) and ("exiftool" in value.lower()):
                    continue
                
                if parameter.startswith("File:"):
                    continue
                
                metadata += f"{parameter}: {value}<br>"
                    
    except Exception as e:
        print(e)
        pass

    query_db("INSERT INTO documents (id, file_name, orig_name, owner, metadata, uploaded_at) VALUES (?, ?, ?, ?, ?, ?)", args=(
        file_id, file_name, orig_name, g.user["id"], metadata, datetime.datetime.utcnow().timestamp()
    ))
    return redirect(url_for("view_document", document_id=file_id))

@app.route("/documents")
def documents():
    if g.user is None:
        return redirect(url_for("login"))

    documents = query_db("SELECT * FROM documents WHERE owner = ?", args=(g.user["id"],))
    return render_template("documents.html", documents=documents)

@app.route("/documents/shared")
def shared_documents():
    if g.user is None:
        return redirect(url_for("login"))

    documents = query_db("SELECT * FROM shared_documents INNER JOIN documents ON documents.id = shared_documents.document_id, users ON documents.owner = users.id WHERE shared_with = ? ORDER BY shared_at DESC LIMIT 10", args=(g.user["id"],))
    return render_template("shareddocuments.html", documents=documents)

@app.route("/viewdocument/<string:document_id>")
def view_document(document_id):
    if g.user is None:
        return redirect(url_for("login"))

    document = query_db("SELECT * FROM documents WHERE id = ?", args=(document_id,), one=True)

    if document is None:
        flash("This document does not exist!", "danger")
        return redirect(url_for("documents"))

    shared_entry = query_db("SELECT * FROM shared_documents WHERE document_id = ? AND shared_with = ?", args=(document_id, g.user["id"]), one=True)

    if shared_entry is None and document["owner"] != g.user["id"]:
        flash("You are not allowed to view this document!", "danger")
        return redirect(url_for("documents"))

    file_extension = document["file_name"].split(".")[-1]

    owner = g.user if g.user["id"] == document["owner"] else query_db("SELECT * FROM users WHERE id = ?", args=(document["owner"],), one=True)

    shared_entries = []

    if shared_entry is not None:
        query_db("UPDATE shared_documents SET viewed = 1 WHERE id = ?", args=(shared_entry["id"],))
    else:
        shared_entries = query_db("SELECT * FROM shared_documents INNER JOIN users ON shared_documents.shared_with = users.id WHERE document_id = ? ORDER BY shared_at DESC LIMIT 10", args=(document_id,))

    return render_template("viewdocument.html", file_extension=file_extension, document=document, owner=owner, shared_entries=shared_entries)

@app.post("/share/<string:document_id>")
def share_document(document_id):
    if g.user is None:
        return redirect(url_for("login"))

    document = query_db("SELECT * FROM documents WHERE owner = ? AND id = ?", args=(g.user["id"], document_id), one=True)

    if document is None:
        return redirect(url_for("documents"))

    share_with = request.form.get("username")
    if share_with is None:
        flash("You must provide a username to share this document with!", "danger")
        return redirect(url_for("view_document", document_id=document_id))

    share_user = query_db("SELECT * FROM users WHERE username = ?", args=(share_with,), one=True)
    if share_user is None:
        flash("This user doesn't exist!", "danger")
        return redirect(url_for("view_document", document_id=document_id))

    if share_user["id"] == g.user["id"]:
        flash("You can't share documents with yourself!", "danger")
        return redirect(url_for("view_document", document_id=document_id))

    existing_entry = query_db("SELECT * FROM shared_documents WHERE document_id = ? AND shared_with = ?", args=(
        document_id,
        share_user["id"]
    ), one=True)

    if existing_entry is not None:
        flash("You've already shared this document with that user!", "danger")
        return redirect(url_for("view_document", document_id=document_id))

    query_db("INSERT INTO shared_documents (document_id, shared_with, shared_at, viewed) VALUES (?, ?, ?, 0)", args=(
        document_id, share_user["id"], datetime.datetime.utcnow().timestamp()
    ))

    flash("Successfully shared this document with " + share_user["username"], "success")
    return redirect(url_for("view_document", document_id=document_id))

@app.get("/logout")
def logout():
    session.clear()
    
    return redirect(url_for("index"))