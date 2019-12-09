from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import User, Event
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/Eat',methods=['GET','POST'])
@login_required
def Eat():
    events = Event.query.filter_by(type="Eat").all()
    return render_template('EventDisplay.html', events=events, curr_time = datetime.now())



@main.route('/Party',methods=['GET','POST'])
@login_required
def Party():
    events = Event.query.filter_by(type="Party").all()
    return render_template('EventDisplay.html', events=events)



@main.route('/Study',methods=['GET','POST'])
@login_required
def Study():
    events = Event.query.filter_by(type="Study").all()
    return render_template('EventDisplay.html', events=events)

    return time  > datetime.now()
