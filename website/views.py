from flask import Blueprint, render_template,redirect,url_for,request
from .models import User, Property, Image
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from werkzeug.utils import secure_filename
import os

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

@views.route('/upload', methods=['GET','POST'])
def upload_form():
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        location = request.form['location']
        image = request.files['image']

        # Save property to the database
        property = Property(title=title, description=description, price=price, location=location)
        db.session.add(property)
        db.session.commit()

        # Save image to the database and upload folder
        filename = secure_filename(image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)

        image_db = Image(filename=filename, filepath=filepath, property_id=property.id)
        db.session.add(image_db)
        db.session.commit()

        print('Property and image uploaded successfully') 

    return render_template('upload.html', user=current_user)

@views.route('/home')
def home():
    
    return render_template("home.html", user=current_user)
