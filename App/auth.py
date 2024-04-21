from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user= User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully!')
                login_user(user, remember = True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, try again.')
        else:
            flash('Username does not exist.')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))    

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user= User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', category='error')
        elif len(username) < 3:
            flash('Username too short', category='error')
        elif len(email) < 4:
            flash('Invalid Email', category='error')
        elif len(password1) < 6 or len (password2) < 6:
            flash('Password is too short', category= 'error')            
        elif password1 != password2:
            flash('Passwords dont match', category= 'error')
        else:
            new_user = User(username=username,email=email,password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))
            #add user to database

    return render_template("signup.html", user=current_user)  