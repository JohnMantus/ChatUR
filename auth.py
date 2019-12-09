from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Event
from __init__ import db
import sys
import datetime
from email import send_email
from flask_login import current_user
from flask_mail import Mail, Message

auth = Blueprint('auth', __name__)

@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.blueprint != 'auth' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('auth.login'))
    return render_template('unconfirmed.html')

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=True)

    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.login'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    token = new_user.generate_confirmation_token()
    send_email(new_user.email, 'Confirm Your Account', 'confirm', user = user, token = token)
    flash('A confirmation email has been sent to you by email.')
    return redirect(url_for('auth.login'))


@auth.route('/confirm/<token>"')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('auth.login'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('auth.login'))


@auth.route('/createEvent',methods=['GET','POST'])
def test():
    return render_template('eventCreation.html')

@auth.route('/eventCreated',methods=['POST'])
def createEvent():
    eventName = request.form.get("event")
    eventLocation= request.form.get("location")
    eventDate = request.form.get("date")
    eventType = request.form.get("types")
    eventTime = request.form.get("time")
    eventDescription= request.form.get("description")
    eventCreator = current_user.name

    eventDateTime = datetime.datetime.strptime(eventDate + " " + eventTime,  '%Y-%m-%d %H:%M')
    new_event = Event(name=eventName, type=eventType, description = eventDescription,  location=eventLocation,  creator=eventCreator, datetime=eventDateTime)

    db.session.add(new_event)
    db.session.commit()
    return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
