from flask import Blueprint, render_template, flash, redirect, url_for
from flask import request
from .models import User, db
from werkzeug.security import generate_password_hash, check_password_hash







auth  = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@auth.route('logout')
def logout():
    return "<h1>Logout</h1>"

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')



        if len(email) < 4:
            flash('Email must be greater then 3 character.', category='error')
        elif len(firstname) < 2:
            flash('First name must be greater than 2 characters.', category='error')
        elif len(lastname) < 2:
            flash('First name must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
          new_user = User(email=email, firstname=firstname, lastname=lastname, password=generate_password_hash(password1, method='Sha256'))
          db.session.add(new_user)
          db.session.commit()
          flash('Account created!', category='success')
          return redirect(url_for('views.home'))

    return render_template('sign_up.html')