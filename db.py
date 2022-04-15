from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model, UserMixin):
    username = db.Column(db.String(15), primary_key="True")
    password = db.Column(db.String(15), nullable=False)
    sysname = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<UserLogin %r %r>" % (self.username, self.password)

    def get_id(self):
        return self.username

class System(db.Model):
    username = db.Column(db.String(15), primary_key="True", db.ForeignKey("user.username"))
    alter = db.Column(db.String(50), primary_key="True")

    def __repr__(self):
        return "<LikesArtist %r %r>" % (self.username, self.alter)

    def get_alter(self):
        return self.alter

class Message(db.Model):
    id = db.Column(db.Integer, primary_key="True")
    username = db.Column(db.String(15))
    alter = db.Column(db.String(50), db.ForeignKey("system.alter"))
    message = db.Column(db.Text)
    archived = db.Column(db.Boolean)

    def __repr__(self):
        return "<LikesArtist %r %r>" % (self.username, self.alter)

    def get_msg(self):
        return self.msg