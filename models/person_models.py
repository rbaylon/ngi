from baseapp import db


class Person(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    MiddleName = db.Column(db.String(50))
    dob = db.Column(db.String(10))
    gender = db.Column(db.String(10))


class NgiPerson(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    pseudonym = db.Column(db.String(50))
    address = db.Column(db.String(200))
    contact_number = db.Column(db.String(15))
    ngi_number = db.Column(db.String(20))
    member_since = db.Column(db.String(10))
    rank = db.Column(db.String(10))
    chapter = db.Column(db.String(50))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=True)
    person = db.relationship('Person', backref=db.backref('NgiPerson', lazy=True))
