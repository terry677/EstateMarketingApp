from flask import Blueprint, render_template,request, flash, redirect, url_for
from .models import User, Property, Image
from flask_login import  login_required, current_user
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

def format_price(value):
    return '{:,.2f}'.format(value)


views = Blueprint('views', __name__)

@views.route('/')
def landing_page():
    return render_template("landing.html")


@views.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    user = get_user_data()
    first_name = user.firstname if user else None
    properties = Property.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", user=current_user, first_name=first_name, properties=properties)

@views.route('/upload', methods=['POST','GET'])
@login_required
def upload_form():
    app = create_app() #Import app instance here
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
            photo=f"static/uploads/{photo.filename}",
            user_id=current_user.id  # Set the user_id to the ID of the logged-in user
        )
        db.session.add(property)
        db.session.commit()

        # Save image to the database and upload folder
        filename = secure_filename(photo.filename)
        folder_path = os.path.join(app.root_path, 'static/uploads')  # Get the absolute path to the "uploads" folder
        filepath = os.path.join(folder_path, filename)
        photo.save(filepath)

        image_db = Image(filename=filename, filepath=f'static/uploads/{filename}', property_id=property.id)  # Store the relative path
        db.session.add(image_db)
        db.session.commit()
    
        flash('Property and image uploaded successfully')

    return render_template('upload.html', user=current_user)

@views.route('/home')
def home():
    images = Image.query.all()
    user = get_user_data()
    properties = Property.query.all()

    if user:
        # Retrieve the properties of the user
        properties = user.properties

        # Print the properties to the console
        for property in properties:
            print(f"Title: {property.title}")
            print(f"Description: {property.description}")
            print(f"Price: {property.price}")
            print(f"Location: {property.location}")
            print("")
    return render_template('home.html', user=current_user,properties=properties, images=images)


@views.route('/delete', methods=['GET', 'POST'])
@login_required
def delete_acc():
    user = get_user_data()
    if user:
        # Delete associated properties and images
        properties = user.properties
        for property in properties:
            images = property.images
            for image in images:
                db.session.delete(image)
            db.session.delete(property)
        db.session.delete(user)
        db.session.commit()
        
        flash('Account deleted successfully')
        return redirect(url_for('views.home'))
    else:
        flash('User not found')
        return redirect(url_for('views.dashboard'))
    
@views.route('/delete/<int:property_id>', methods=['POST'])
@login_required
def delete_property(property_id):
    property = Property.query.get(property_id)
    if property:
        if property.user_id == current_user.id:
            # Delete associated images
            images = property.images
            for image in images:
                db.session.delete(image)
            
            db.session.delete(property)
            db.session.commit()
            
            flash('Property deleted successfully')
        else:
            flash('You can only delete your own properties')
    else:
        flash('Property not found')
    
    return redirect(url_for('views.home'))

