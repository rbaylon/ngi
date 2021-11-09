from baseapp import db
from flask_login import UserMixin


class Users(UserMixin, db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(150))
    email = db.Column(db.String(50))
    admin = db.Column(db.Boolean)
    group = db.Column(db.String(50))


