import os
from dotenv import find_dotenv, load_dotenv
import flask
from flask_login import (
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
)
from db import db
from db_func import *
import json

load_dotenv(find_dotenv())


app = flask.Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
app.secret_key = os.getenv("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
with app.app_context():
    db.create_all()

@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response

@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return flask.redirect("/login")


@app.route("/login")
def loginpage():
    if current_user.is_authenticated:
        return flask.redirect("/")
    return flask.render_template("login.html")


@app.route("/signup")
def signuppage():
    if current_user.is_authenticated:
        return flask.redirect("/")
    return flask.render_template("signup.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect("/")

@app.route("/login-post", methods=["POST"])
def login():
    entered_name = flask.request.form["username"]
    entered_pw = flask.request.form["password"]
    if not verify_user(entered_name, entered_pw):
        flask.flash("Incorrect username or password.")
        return flask.redirect("/login")
    else:
        login_user(get_user(entered_name))
        return flask.redirect("/")


@app.route("/signup-post", methods=["POST"])
def signup():
    entered_name = flask.request.form["username"]
    entered_pw = flask.request.form["password"]
    entered_sys = flask.request.form["system"]
    this_user = get_user(entered_name)

    if this_user != None:
        flask.flash("Sorry, that username is taken.")
        return flask.redirect("/signup")
    else:
        new_user = set_user(entered_name,entered_pw,entered_sys)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return flask.redirect("/")

@app.route("/")
@login_required
def index():
    message_list = [{"message": get_message(i), "alter": get_alter_name(i.alter_id)} for i in get_messages(current_user.username)]
    alter_list = [get_alter(i) for i in get_alters(current_user.username)]
    return flask.render_template("index.html", sysname=current_user.sysname, alter_list=alter_list, message_list=message_list)

@app.route("/profile")
@login_required
def profile():
    alter_list = [get_alter(i).alter for i in get_alters(current_user.username)]
    return flask.render_template("profile.html", sysname=current_user.sysname, alter_list=alter_list)

@app.route("/save-alter", methods=["POST"])
@login_required
def save_alter():
    alter_name = json.loads(flask.request.data)["alterName"]
    new_alter = set_alter(current_user.username,alter_name)
    db.session.add(new_alter)
    db.session.commit()
    jsonreturn = flask.jsonify({"msg": "Alter added successfully!"})
    return jsonreturn

@app.route("/about")
def about():
    return flask.render_template("about.html")

@app.route("/desc")
def desc():
    return flask.render_template("desc.html")

@app.route("/checklist")
def checklist():
    return flask.render_template("check.html")

@app.route("/post-message", methods=["POST"])
@login_required
def post_message():
    message = json.loads(flask.request.data)["newMessage"]
    alter = json.loads(flask.request.data)["alter"]
    to_archive = set_message(current_user.username,alter,message)
    to_archive.archived = True
    db.session.commit()
    jsonreturn = flask.jsonify({"msg": "Message posted!"})
    return jsonreturn

@app.route("/archive-message", methods=["POST"])
@login_required
def archive_message():
    archive_id = json.loads(flask.request.data)["archiveId"]
    to_archive = get_message(archive_id)
    to_archive.archived = True
    db.session.commit()
    jsonreturn = flask.jsonify({"msg": "Message archived!"})
    return jsonreturn

app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
