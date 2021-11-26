from models import Users
from baseapp import db
from werkzeug.security import generate_password_hash

class UsersController:
    def add(self, user):
        hashed_password = generate_password_hash(user['password'], method='pbkdf2:sha256:260000', salt_length=16)
        existing = Users.query.filter_by(username=user['username']).first()
        if not existing:
            new_user = Users(username=user['username'], password=hashed_password,admin=False, group=user['group'],
                             email=user['email'])
            db.session.add(new_user)
            db.session.commit()
            return True

        return False

    def edit(self, user):
        existing_user = Users.query.filter_by(id=user['id']).first()
        if existing_user:
            existing_user.username = user['username']
            existing_user.email = user['email']
            existing_user.group = user['group']
            db.session.commit()
            return True

        return False
    
    def delete(self, user):
        existing_user = Users.query.filter_by(id=user['id']).first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
            return True

        return False

    def resetpw(self, user):
        existing_user = Users.query.filter_by(id=user['user_id']).first()
        if existing_user:
            hashed_password = generate_password_hash(user['password'], method='pbkdf2:sha256:260000', salt_length=16)
            existing_user.password = hashed_password
            db.session.commit()
            return True

        return False

