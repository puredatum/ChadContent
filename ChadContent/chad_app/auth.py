from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint("auth", __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        new_user = User(name=name, password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()

    return render_template("register.html", user=current_user)


# New route for user login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        input_name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(name=input_name).first()

        if user and check_password_hash(user.password, password):
        	flash('Logged in successfully!', category='success')
        	login_user(user, remember=True)
        else:
            return "Invalid credentials. Please try again."

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
	flash('Logout in successful!', category='success')
	logout_user()
	return redirect(url_for('auth.login'))