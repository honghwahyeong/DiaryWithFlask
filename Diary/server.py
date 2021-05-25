from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("mainPage.html")

@app.route("/signUp")
def sign_up():
    return render_template("sign_up.html")

@app.route("/login")
def log_in():
    return render_template("login.html")

if __name__ == "__main__":
    app.run()