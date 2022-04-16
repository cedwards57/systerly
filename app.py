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
import datetime

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
    messages = get_messages(current_user.username)
    message_list = [{
            "messageid": get_message(i).id,
            "messagetext": get_message(i).message,
            "alter": get_alter_name(get_message(i).alter_id),
            "datetime": get_message(i).datetime.strftime("%I:%M:%S %m/%d/%y")
        } for i in messages]
    alter_list = [get_alter(i) for i in get_alters(current_user.username)]
    return flask.render_template("index.html", sysname=current_user.sysname, alter_list=alter_list, message_list=message_list)

@app.route("/post-message", methods=["POST"])
@login_required
def post_message():
    message = json.loads(flask.request.data)["newMessage"]
    alter = json.loads(flask.request.data)["alter"]
    now = datetime.datetime.now()
    to_post = set_message(current_user.username,get_alter_id(current_user.username,alter),message,now)
    db.session.add(to_post)
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

@app.route("/profile")
@login_required
def profile():
    alter_list = [{"name": get_alter(i).alter, "id": get_alter(i).id} for i in get_alters(current_user.username)]
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

@app.route("/remove-alter", methods=["POST"])
@login_required
def remove_alter():
    alter_id = json.loads(flask.request.data)["alterId"]
    rm_messages = get_messages_from(current_user.username,alter_id)
    for message_id in rm_messages:
        message = get_message(message_id)
        db.session.delete(message)
    rm_alter = get_alter(alter_id)
    db.session.delete(rm_alter)
    db.session.commit()
    jsonreturn = flask.jsonify({"msg": "Alter removed successfully!"})
    return jsonreturn

@app.route("/about")
def about():
    return flask.render_template("about.html")

@app.route("/desc")
def desc():
    return flask.render_template("desc.html")

@app.route("/checklist")
def checklist():
    return flask.render_template("checklist.html")


app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
