from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import re

auth = Blueprint('auth', __name__)



@auth.route('/', methods=['GET', 'POST'])
def login():


    if current_user.is_authenticated:

        return redirect(url_for('views.home'))
        

    if request.method == 'POST':
        

        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')


    return render_template("login.html")

@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    if current_user.is_authenticated:

        return redirect(url_for('views.home'))

    if request.method == 'POST':
        username = request.form.get('new_username')
        password1 = request.form.get('new_password')
        password2 = request.form.get('confirm_password')
        
        if is_valid_password(password1) and is_equal_passwords(password1, password2) and is_repeating_username(username):

            new_user = User(username=username, password=password1)
            db.session.add(new_user)
            db.session.commit()

            flash('Account created', category='success')
            login_user(new_user, remember=True)
            #redirect to main menu
            return redirect(url_for('views.home'))
        else:

            pass

    return render_template("signup.html")






def is_repeating_username(username):

    user = User.query.filter_by(username=username).first()
    if user:
        flash('Username already exists.', category='error')
        return False
    else:
        return True


def is_valid_password(password):

    if len(password) < 7:

        flash('Password must be at least 8 characters', category='error')
        return False
    else:

        return True

def is_equal_passwords(password1, password2):

    if password1 != password2:

        flash('Passwords do not match', category='error')
        return False
    
    else:

        return True
    

