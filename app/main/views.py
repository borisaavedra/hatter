from . import main
from ..models import db, Users, Hattes, Codes, Relations
from flask import render_template, redirect, url_for, request, flash
from sqlalchemy.exc import IntegrityError

@main.route("/")
def index():
    return redirect(url_for(".login"))

@main.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        login_pass = request.form["password"]
        user_db = Users.query.filter_by(username=username).first()

        if user_db is not None and user_db.verify_password(login_pass):
            
            return redirect(url_for(".user", username=username))

        else:

            flash("Wrong username or password 😖", "danger")
            
    return render_template("login.html")

@main.route("/signin", methods=["POST", "GET"])
def signin():

    if request.method == "POST":

        user_code = request.form["code"]

        if Codes.query.filter_by(code_name=user_code).first():

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
                flash("{}, you're ready to Hatte!".format(username), "success")

                context = {
                    # "user": name,
                    "username": username
                }

                return redirect(url_for(".user", username=username))

            except IntegrityError:

                flash("Sorry, there's someone who took that username 😈", "danger")
                db.session.rollback()
                return render_template("signin.html")

        else:

            flash("That wasn't an invitation code, you punk 🤬", "danger")

    return render_template("signin.html")

@main.route("/user/<username>")
def user(username):

    user = Users.query.filter_by(username=username).first()

    context = {
        "name": user.name,
        "username": username,
        "avatar_url": user.avatar_url,
        "bio": user.bio
    }

    return render_template("user.html", **context)
