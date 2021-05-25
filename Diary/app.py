from flask import Flask, render_template, redirect, url_for, request
from DB_handler import DBModule

app = Flask(__name__)
DB = DBModule()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/list")
def post_list():
    pass


@app.route("/post/<int:pid>")
def post(pid):
    pass


@app.route("/login")
def login():
    pass


@app.route("/signin")
def signin():
    return render_template("signin.html")


@app.route("/signin_done", methods=["get"])
def signin_done():
    email = request.args.get("email")
    uid = request.args.get("id")
    pwd = request.args.get("pwd")
    name = request.args.get("name")
    if DB.signin(uid, pwd, name, email):
        return redirect(url_for("index"))
    else:
        return redirect(url_for("signin"))


@app.route("/user/<uid>")
def user(uid):
    pass


@app.route("/write")
def write():
    pass


@app.route("/write_done", methods=["GET"])
def write_done():
    pass


if __name__ == "__main__":
    app.run(debug=True)
