from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Event
from __init__ import db
import sys
import datetime
from flask_login import current_user
from forms import ChangePasswordForm


auth = Blueprint('auth', __name__)


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

    return redirect(url_for('auth.login'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.password = form.password.data
        current_user.password = generate_password_hash(current_user.password, method='sha256')     
        db.session.add(current_user)
        db.session.commit()
        flash('Your password has been updated.')
        return redirect(url_for('main.index'))
    
    return render_template("change_password.html", form=form)


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
