from baseapp import db


class ChapterPayments(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    received_from = db.Column(db.String(50))
    received_date = db.Column(db.String(10))
    received_amount = db.Column(db.String(7))
    payment_type = db.Column(db.String(50))
    chapter = db.Column(db.String(50))
    cpc = db.Column(db.Boolean)