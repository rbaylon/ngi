from baseapp import db


class Chapter(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100))
    founder = db.Column(db.String(50))
    founded = db.Column(db.String(10))