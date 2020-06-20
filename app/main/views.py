from . import main
from flask import render_template, redirect, url_for

@main.route("/")
def index():
    return redirect(url_for(".login"))

@main.route("/login")
def login():
    return render_template("login.html")

@main.route("/signin")
def signin():
    return render_template("signin.html")

@main.route("/user/<user>")
def user(user):
    return render_template("user.html", user=user)
