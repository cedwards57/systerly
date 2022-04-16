from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


class User(db.Model, UserMixin):
    username = db.Column(db.String(30), primary_key="True")
    password = db.Column(db.String(30), nullable=False)
    sysname = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<User %r %r>" % (self.username, self.password)

    def get_id(self):
        return self.username

class System(db.Model):
    id = db.Column(db.Integer, primary_key="True")
    username = db.Column(db.ForeignKey(User.username))
    alter = db.Column(db.String(50))

    def __repr__(self):
        return "<System %r %r %r>" % (self.username, self.alter, self.id)

    def get_alter(self):
        return self.alter

class Message(db.Model):
    id = db.Column(db.Integer, primary_key="True")
    username = db.Column(db.String(15))
    alter_id = db.Column(db.ForeignKey(System.id))
    message = db.Column(db.Text)
    archived = db.Column(db.Boolean)
    datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<Message %r %r %r %r %r %r>" % (self.id, self.username, self.alter_id, self.message, self.archived, self.datetime)

    def get_msg(self):
        return self.msg
    