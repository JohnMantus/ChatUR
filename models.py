from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000))
    type = db.Column(db.String(10))
    # date = db.Column(db.DateTime(100)) # might be DateTime.date or DateTime.datetime
    location = db.Column(db.String(100))
    creator = db.Column(db.String(1000))
    # time = db.Column(db.Integer(100)) # maybe improve using date time later
    description = db.Column(db.String())
    datetime = db.Column(db.DateTime())


def init_db():
    db.create_all()


if __name__ == '__main__':
    init_db()
