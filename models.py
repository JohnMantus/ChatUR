from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from __init__ import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


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
