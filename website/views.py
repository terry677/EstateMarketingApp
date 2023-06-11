from flask import Blueprint, render_template
from .models import User
from flask_login import login_user, logout_user, login_required, current_user




views  = Blueprint('views', __name__)

@views.route('/')
def landing_page():
    return render_template('landing.html')

@views.route('/dashboard')
@login_required
def dashboard():
    return  render_template("dashboard.html", user=current_user)

@views.route('/home')
def home():
    return render_template('home.html')
