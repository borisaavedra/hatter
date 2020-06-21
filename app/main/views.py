from . import main
from ..models import db, Users, Hattes, Codes, Relations
from flask import render_template, redirect, url_for, request, flash

@main.route("/")
def index():
    return redirect(url_for(".login"))

@main.route("/login")
def login():
    return render_template("login.html")

@main.route("/signin", methods=["POST", "GET"])
def signin():

    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]

        try:
            new_user = Users(
                name=name,
                username=username,
                password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("{}, you're ready to Hatte!".format(username))
            return render_template("user.html", username=username, user=username)
        except:
            flash("Sorry, you're too nice to Hatte")
            return render_template("signin.html")

    return render_template("signin.html")

@main.route("/user/<user>")
def user(user):
    return render_template("user.html", user=user)
