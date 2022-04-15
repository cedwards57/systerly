from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model, UserMixin):
    username = db.Column(db.String(15), primary_key="True")
    password = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return "<UserLogin %r %r>" % (self.username, self.password)

    def get_id(self):
        return self.username

