from flask import Flask, render_template, request, render_template_string
app = Flask(__name__)

@app.route('/', methods = [ 'GET'])
def index():
    if(request.args.get('login')):
        login = request.args.get('login')
        if "{{" in login:
            alert = "<script>alert('Plz no hack. {{ is not allowed >:(')</script>"
        elif "}}" in login:
            alert = "<script>alert('Plz no hack. }} is not allowed >:(')</script>"
        else:
            alert = render_template_string("<script>alert('Username " + login + " does not exist.')</script>")
        return render_template("index.html", alert=alert)
    else:
        return render_template("index.html", alert="")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
