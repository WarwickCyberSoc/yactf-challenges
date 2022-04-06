from flask import Flask, request

import subprocess

app = Flask(__name__)


@app.route("/pingsite")
def hello():
    return subprocess.check_output(
        "/bin/ping -c 4 " + request.args.get("site", "8.8.8.8"),
        shell=True,
        timeout=240,
    )
