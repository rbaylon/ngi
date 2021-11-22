from models import NgiPerson, Person
from baseapp import db


class NgiPersonController:
    def add(self, person):
        existing = NgiPerson.query.filter_by(pseudonym=person['pseudonym']).first()
        if not existing:
            new_person = NgiPerson()
            new_person.person = Person()
            new_person.pseudonym = person['pseudonym']
            new_person.address = person['address']
            new_person.contact_number = person['contact_number']
            new_person.ngi_number = person['ngi_number']
            new_person.member_since = person['member_since']
            new_person.rank = person['rank']
            new_person.chapter = person['chapter']
            new_person.person.FirstName = person['first_name']
            new_person.person.LastName = person['last_name']
            new_person.person.MiddleName = person['middle_name']
            new_person.person.dob = person['dob']
            new_person.person.gender = person['gender']
            db.session.add(new_person)
            db.session.commit()
            return True

        return False

    def edit(self, person):
        existing_person = NgiPerson.query.filter_by(id=person['id']).first()
        if existing_person:
            existing_person.pseudonym = person['pseudonym']
            existing_person.address = person['address']
            existing_person.contact_number = person['contact_number']
            existing_person.ngi_number = person['ngi_number']
            existing_person.member_since = person['member_since']
            existing_person.rank = person['rank']
            existing_person.chapter = person['chapter']
            existing_person.person.FirstName = person['first_name']
            existing_person.person.LastName = person['last_name']
            existing_person.person.MiddleName = person['middle_name']
            existing_person.person.dob = person['dob']
            existing_person.person.gender = person['gender']
            db.session.commit()
            return True

        return False

    def delete(self, person):
        existing_person = NgiPerson.query.filter_by(id=person['id']).first()
        if existing_person:
            person = Person.query.filter_by(id=existing_person.person.id).first()
            db.session.delete(existing_person)
            db.session.delete(person)
            db.session.commit()
            return True

        return False
