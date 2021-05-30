from flask import Flask, render_template, redirect, url_for, request, flash, session
from DB_handler import DBModule
from werkzeug.utils import secure_filename
import os
import tempfile

app = Flask(__name__)
app.secret_key = "ghdghkgudsksmsghdghkgud"
DB = DBModule()


@app.route("/")
def index():
    if "uid" in session:
        user = session["uid"]
    else:
        user = "Login"
    return render_template("index.html", user=user)


@app.route("/list")
def post_list():
    post_list = DB.post_list()
    if "uid" in session:
        user = session["uid"]
    else:
        user = "Login"
    if post_list == None:
        length = 0
        return redirect(url_for("index"))
    else:
        length = len(post_list)
    return render_template(
        "post_list.html", post_list=post_list.items(), length=length, user=user
    )


@app.route("/post/<string:pid>")
def post(pid):
    if "uid" in session:
        user = session["uid"]
    else:
        user = "Login"
    post, post_id = DB.post_detail(pid)
    image = DB.get_image(pid)
    return render_template(
        "post_detail.html", post=post, image=image, post_id=post_id, user=user
    )


@app.route("/delete_post/<string:pid>")
def delete_post(pid):
    post, post_id = DB.post_detail(pid)
    if session["uid"] == post["uid"]:
        DB.delete_post(pid)
        return redirect(url_for("post_list"))
    else:
        print("작성자가 아님")
        return redirect(url_for("post", pid=pid))


@app.route("/logout")
def logout():
    if "uid" in session:
        session.pop("uid")
        return redirect(url_for("post_list"))
    else:
        return redirect(url_for("post_list"))
    return redirect("login.html")


@app.route("/login")
def login():
    if "uid" in session:
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/login_done", methods=["get"])
def login_done():
    uid = request.args.get("id")
    pwd = request.args.get("pwd")
    if DB.login(uid, pwd):
        session["uid"] = uid
        return redirect(url_for("post_list"))
    else:
        flash("아이디가 없거나 비밀번호가 틀립니다.")
        return redirect(url_for("login"))


@app.route("/signin")
def signin():
    if "uid" in session:
        user = session["uid"]
    else:
        user = "Login"
    return render_template("signin.html", user=user)


@app.route("/signin_done", methods=["get"])
def signin_done():
    email = request.args.get("email")
    uid = request.args.get("id")
    pwd = request.args.get("pwd")
    name = request.args.get("name")
    if DB.signin(uid, pwd, name, email):
        return redirect(url_for("post_list"))
    else:
        flash("이미 존재하는 아이디 입니다.")
        return redirect(url_for("signin"))


@app.route("/user/<uid>")
def user(uid):
    pass


@app.route("/write")
def write():
    if "uid" in session:
        user = session["uid"]
        return render_template("write_diary.html", user=user)
    else:
        return redirect(url_for("login"))


@app.route("/write_done", methods=["POST"])
def write_done():
    title = request.form.get("title")
    contents = request.form.get("contents")
    uid = session.get("uid")
    file = request.files["file"]
    temp = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp.name)
    DB.write_post(title, contents, uid, temp.name)
    os.remove(temp.name)
    return redirect(url_for("post_list"))


@app.route("/edit_post/<string:pid>")
def edit_post(pid):
    if "uid" in session:
        user = session["uid"]
    else:
        user = "Login"
    post, post_id = DB.post_detail(pid)
    if user == post["uid"]:
        return render_template("edit_post.html", post=post, post_id=post_id, user=user)
    else:
        return redirect(url_for("post", pid=post_id))


@app.route("/edit_done/<string:pid>", methods=["POST"])
def edit_done(pid):
    title = request.form.get("title")
    contents = request.form.get("contents")
    file = request.files["file"]
    temp = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp.name)
    DB.edit_post(title, contents, pid)
    return redirect(url_for("post_list"))


if __name__ == "__main__":
    app.run(debug=True)
