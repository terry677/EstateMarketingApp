from flask import Blueprint, render_template,redirect,url_for
from .models import User
from flask_login import login_user, logout_user, login_required, current_user


def get_user_data():
    if current_user.is_authenticated:
        user_id = current_user.id
        user = User.query.get(user_id)
        return user
    else:
        return None

views  = Blueprint('views', __name__)

@views.route('/')
def landing_page():
    return render_template("landing.html")

@views.route('/dashboard')
@login_required
def dashboard():
    user = get_user_data()
    first_name = user.firstname if user else None
    return  render_template("dashboard.html", user=current_user, first_name=first_name)

@views.route('/upload', methods=['GET'])
def upload_form():
    return render_template('upload.html', user=current_user)

@views.route('/home')
def home():
    
    return render_template("home.html", user=current_user)
