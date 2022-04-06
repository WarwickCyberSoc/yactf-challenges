from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "stockcheck"
app.config["MYSQL_PASSWORD"] = "57r0n6357_club_0n_c4mpu5"
app.config["MYSQL_DB"] = "stockcheck"

mysql = MySQL(app)


@app.route("/", methods=["POST", "GET"])
def login():
    query = "SELECT * FROM stock"
    arguments = []
    if request.method == "POST" and request.form.get("product_name") is not None:
        query = "SELECT * FROM stock WHERE name LIKE %s"
        arguments = ["%" + request.form.get("product_name") + "%"]

    cur = mysql.connection.cursor()
    cur.execute(query, arguments)
    rv = cur.fetchall()

    print(rv)

    return render_template("stock.html", products=rv)


app.run(host="127.0.0.1", port=5000, debug=True)
