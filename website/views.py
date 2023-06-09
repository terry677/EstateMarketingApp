from flask import Blueprint, render_template
from .models import User
from flask_login import login_user, logout_user, login_required, current_user




views  = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return  render_template("home.html")

@views.route('/users')
def view_users():
    # Retrieve all users from the database
    users = User.query.all()

    # Get the current authenticated user, if any
    user = current_user if current_user.is_authenticated else None

    # Render a template to display the user data
    return render_template('users.html', user=user)
