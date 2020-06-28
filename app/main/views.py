from . import main
from ..models import db, Users, Hattes, Codes, Relations
from flask import render_template, redirect, url_for, request, flash, session
from sqlalchemy.exc import IntegrityError

def add_hatte(new_message, new_message_pic, current_user):

    new_hatte = Hattes(
        message=new_message, 
        pic=new_message_pic, 
        user_id=current_user.id
        )

    db.session.add(new_hatte)

    try:
        db.session.commit()
        flash("New Hatte sent 😎", "success")
        return redirect(url_for(".user", username=current_user.username))
    except:
        db.session.rollback()
        flash("Something went wrong 😯 with your Hatte", "danger")
        return redirect(url_for(".user", username=currente_user.username))

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
        
        current_user = Users.query.filter_by(id=session["user"]).first()

        if "follow" in request.form: #EL CURRENT USER QUIERE SEGUIR A ALGUIEN

            user_tofollow = request.form["follow"]
            other_user = Users.query.filter_by(id=user_tofollow).first()
            
            if user_tofollow:
                rel = Relations(user_id=current_user.id, followed_id=user_tofollow)

                db.session.add(rel)
                try:
                    db.session.commit()
                    flash("Now you Hatte {}".format(other_user.name), "success")
                except:
                    db.session.rollback()
                    flash("Somethng went wrong 😫", "danger")

        followeds_ids = Relations.query.filter_by(user_id=current_user.id).all() #TODOS LOS IDS DE LOS USUARIOS QUE SIGUE EL CURRENT USER

        f_id = [u.followed_id for u in followeds_ids] #PARA OBTENER SOLO LOS IDS DE LOS USUARIOS QUE SIGUE EL CURRENT USER

        hattes_user = db.session.query(Users, Hattes).order_by(Hattes.created.desc()).filter(Users.id.in_(f_id)).filter(Hattes.user_id.in_(f_id)).all()
        # El query de arriba me trae todos los mensajes de los usuarios que sigue el current user de forma descendente
        
        t= ()
        users_list = []
        for u in hattes_user: # Este ciclo crea una lista de tuplas que tiene usuario con su mensaje de forma descendente
            a, b = u
            if a.id == b.user_id:
                t = a, b
                users_list.append(t)

        if len(hattes_user) == 0: #PARA SABER SI EL USUARIO NO SIGUE A NADIE
            status_msg = 0
        else:
            status_msg = 1

        if request.method == "POST":

            if "unhatte" in request.form: #Para dejar de seguir a un usuario

                unhatte_id = request.form["unhatte"]

                followeds_list = Relations.query.filter_by(user_id=current_user.id).all()

                for u in followeds_list:
                    if u.followed_id == int(unhatte_id):
                        db.session.delete(u)
                        break

                try:
                    db.session.commit()
                    flash("User unHatte 😛", "success")
                    return redirect(url_for(".user", username=username))

                except:
                    db.session.rollback()
                    flash("Something went wrong 😓")
                    return redirect(url_for(".user", username=username))

            if "hatte" in request.form: #PARA AGREGAR UN MENSAJE NUEVO
                new_message = request.form["hatte"]
                new_message_pic = request.form["url_pic"]
                add_hatte(new_message, new_message_pic, current_user)
                return redirect(url_for(".user", username=username))
 
            elif "name" in request.form: #PARA SABER SI EL USUARIO QUIERE EDITAR SU CUENTA

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

        users_id_followed = Relations.query.filter_by(user_id=current_user.id).all()
        no_followeds = Relations.query.filter_by(user_id=current_user.id).count()
        no_followers = Relations.query.filter_by(followed_id=current_user.id).count()

        o_u = [u.followed_id for u in users_id_followed]
        
        o_u.append(current_user.id)

        other_users = db.session.query(Users).filter( Users.id.notin_(o_u) ).all()

        context = {
            "name": current_user.name,
            "username": current_user.username,
            "avatar_url": current_user.avatar_url,
            "bio": current_user.bio,
            "status_msg": status_msg,
            "users_list": users_list,
            "other_users": other_users,
            "no_followeds": no_followeds,
            "no_followers": no_followers
        }

        return render_template("user.html", **context)
    else:
        return redirect(url_for(".login"))



@main.route("/user/<username>/timeline", methods=['POST', 'GET'])
def timeline(username):

    current_user = Users.query.filter_by(id=session["user"]).first()
    user_hattes = Hattes.query.filter_by(user_id=current_user.id).order_by(Hattes.created.desc()).all()
    no_followeds = Relations.query.filter_by(user_id=current_user.id).count()
    no_followers = Relations.query.filter_by(followed_id=current_user.id).count()

    if "hatte" in request.form: #PARA AGREGAR UN MENSAJE NUEVO

        new_message = request.form["hatte"]
        new_message_pic = request.form["url_pic"]

        add_hatte(new_message, new_message_pic, current_user)
        return redirect(url_for(".timeline", username=username))

    context = {
        "username": current_user.username,
        "status_msg": 1,
        "current_user": current_user,
        "user_hattes": user_hattes,
        "no_followeds": no_followeds,
        "no_followers": no_followers
    }

    return render_template("timeline.html", **context)

