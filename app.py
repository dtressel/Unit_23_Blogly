"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from sqlalchemy import delete

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'fruitsmell378917'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

@app.route('/')
def show_home():
    """Redirects to /users"""
    return redirect('/users')

@app.route('/users')
def show_users():
    """Returns page that shows list of current users"""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def show_create_user():
    """Returns page with form to create a new user"""
    return render_template('new-user.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():
    """Adds new user on form submit"""
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/user/<int:user_id>')
def show_user_details(user_id):
    """Returns page the shows the details for a particular user"""
    selected_user = User.query.get(user_id)
    return render_template('user-details.html', user=selected_user)

@app.route('/user/<user_id>/edit')
def show_edit_user(user_id):
    """Returns page the shows the form to edit a user"""
    selected_user = User.query.get(user_id)
    return render_template('edit-user.html', user=selected_user)

@app.route('/user/<user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Handles form submission to update user information"""
    edited_user = User.query.get(user_id)
    edited_user.first_name = request.form['first-name']
    edited_user.last_name = request.form['last-name']
    edited_user.image_url = request.form['image-url']
    db.session.add(edited_user)
    db.session.commit()
    print(f'/users/{user_id}')
    return redirect(f'/user/{user_id}')

@app.route('/user/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Deletes a user after delete button press on user detail page"""
    print(user_id)
    User.query.filter_by(id=user_id).delete()
    # User.query.get(user_id).delete() ***didn't work for some reason
    db.session.commit()
    return redirect('/users')