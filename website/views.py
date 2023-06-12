from flask import Blueprint, render_template, redirect, url_for, request
from .models import User, Property, Image
from flask_login import login_user, logout_user, login_required, current_user
from . import db, create_app
from werkzeug.utils import secure_filename
import os

def get_user_data():
    if current_user.is_authenticated:
        user_id = current_user.id
        user = User.query.get(user_id)
        return user
    else:
        return None

views = Blueprint('views', __name__)

@views.route('/')
def landing_page():
    return render_template("landing.html")

@views.route('/dashboard')
@login_required
def dashboard():
    user = get_user_data()
    first_name = user.firstname if user else None
    return render_template("dashboard.html", user=current_user, first_name=first_name)

@views.route('/upload', methods=['POST','GET'])
@login_required
def upload_form():
    app = create_app()  # Import app instance here
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        location = request.form['location']
        photo = request.files['photo']

        # Save property to the database
        property = Property(
            title=title,
            description=description,
            price=price,
            location=location,
            photo=photo.filename,
            user_id=current_user.id  # Set the user_id to the ID of the logged-in user
        )
        db.session.add(property)
        db.session.commit()

        # Save image to the database and upload folder
        filename = secure_filename(photo.filename)
        folder_path = os.path.join(app.root_path, 'uploads')  # Get the absolute path to the "uploads" folder
        filepath = os.path.join(folder_path, filename)
        photo.save(filepath)

        image_db = Image(filename=filename, filepath=f'uploads/{filename}', property_id=property.id)  # Store the relative path
        db.session.add(image_db)
        db.session.commit()

        print('Property and image uploaded successfully')

    return render_template('upload.html', user=current_user)