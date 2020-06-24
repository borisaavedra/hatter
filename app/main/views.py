from . import main
from ..models import db, Users, Hattes, Codes, Relations
from flask import render_template, redirect, url_for, request, flash, session
from sqlalchemy.exc import IntegrityError

@main.route("/", methods=["GET", "POST"])
def index():
    session.clear()
    return redirect(url_for(".login"))

@main.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        login_pass = request.form["password"]
        user_db = Users.query.filter_by(username=username).first()

        if user_db is not None and user_db.verify_password(login_pass):

            session["user"] = user_db.id
            
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

@main.route("/user/<username>", methods=["POST", "GET"])
def user(username):

    if "user" in session:

        hattes_user = Hattes.query.filter_by(user_id=session["user"]).all()
        
        if len(hattes_user) == 0:
            status_msg = 0
        else:
            status_msg = 1

        if request.method == "POST":

            if "hatte" in request.form:

                new_message = request.form["hatte"]
                new_message_pic = request.form["url_pic"]

                new_hatte = Hattes(
                    message=new_message, 
                    pic=new_message_pic, 
                    user_id=session["user"])

                db.session.add(new_hatte)

                try:
                    db.session.commit()
                    flash("New Hatte sent 😎", "success")
                    return redirect(url_for(".user", username=username))
                except:
                    db.session.rollback()
                    flash("Something went wrong 😯 with your Hatte", "danger")
                    return redirect(url_for(".user", username=username))
 
            elif "name" in request.form:

                name = request.form["name"]
                bio = request.form["bio"]
                avatar_url = request.form["avatar_url"]

                user_toedit = Users.query.filter_by(username=username).first()

                user_toedit.name = name
                user_toedit.bio = bio
                user_toedit.avatar_url = avatar_url

                try:

                    db.session.commit()
                    flash("Account edited", "success")
                    return redirect(url_for(".user", username=username))

                except:

                    db.session.rollback()
                    flash("Something went wrong 😯", "danger")
                    return redirect(url_for(".user", username=username))

        user = Users.query.filter_by(username=username).first()
        context = {
            "name": user.name,
            "username": username,
            "avatar_url": user.avatar_url,
            "bio": user.bio,
            "status_msg": status_msg,
            "hattes_user": hattes_user
        }

        return render_template("user.html", **context)
    else:
        return redirect(url_for(".login"))
