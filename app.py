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
from db import db, User

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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


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
        return flask.redirect("/userpage")
    return flask.render_template("signup.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect("/")

@app.route("/login", methods=["POST"])
def login():
    entered_name = flask.request.form["username"]
    entered_pw = flask.request.form["password"]
    this_user = User.query.filter_by(username=entered_name).first()
    if not this_user or (this_user.password != entered_pw):
        flask.flash("Incorrect username or password.")
        return flask.redirect("/")
    else:
        login_user(this_user)
        return flask.redirect("/userpage")


@app.route("/signup", methods=["POST"])
def signup():
    entered_name = flask.request.form["username"]
    entered_pw = flask.request.form["password"]
    this_user = User.query.filter_by(username=entered_name).first()

    if this_user:
        flask.flash("This username is taken.")
        return flask.redirect("/create")
    else:
        new_user = User(username=entered_name, password=entered_pw)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return flask.redirect("/")

@app.route("/")
def index():
    return flask.render_template("index.html", myvar=5)



app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
