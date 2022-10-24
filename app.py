"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'fruitsmell378917'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

@app.route('/')
def show_home():
    """Shows Home Page"""

    return render_template('home.html')

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

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """Returns page the shows the details for a particular user"""
    selected_user = User.query.get(user_id)
    return render_template('user-details.html', user=selected_user)

@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """Returns page the shows the form to edit a user"""
    selected_user = User.query.get(user_id)
    return render_template('edit-user.html', user=selected_user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Handles form submission to update user information"""
    edited_user = User.query.get(user_id)
    edited_user.first_name = request.form['first-name']
    edited_user.last_name = request.form['last-name']
    edited_user.image_url = request.form['image-url']
    db.session.add(edited_user)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Deletes a user after delete button press on user detail page. Also, deletes the user's posts."""

    user_to_delete = User.query.get(user_id)
    if user_to_delete.posts:
        for post in user_to_delete.posts:
            db.session.delete(post)
        db.session.commit()
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Displays the form to create a new post"""

    selected_user = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template('new-post.html', user=selected_user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_new_post(user_id):
    """Handles a new post submission"""

    tags = []
    for tag in Tag.query.all():
        if request.form.get(tag.name):
            tags.append(tag)
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content, user_id=user_id, tags=tags)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Shows a post and allows user to edit or delete it"""

    selected_post = Post.query.get(post_id)
    author = User.query.get(selected_post.user_id)

    return render_template('post-details.html', post=selected_post, author=author)

@app.route('/posts/<int:post_id>/edit')
def post_edit_form(post_id):
    """Shows a form to edit a post"""

    selected_post = Post.query.get(post_id)
    author = User.query.get(selected_post.user_id)
    checked_tags = []
    for tag in selected_post.tags:
        checked_tags.append(tag.name)
    all_tags = Tag.query.all()

    return render_template('edit-post.html', post=selected_post, author=author, checked_tags=checked_tags, all_tags=all_tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    """Handles post edit submission"""

    tags = []
    for tag in Tag.query.all():
        if request.form.get(tag.name):
            tags.append(tag)
    edited_post = Post.query.get(post_id)
    edited_post.title = request.form['title']
    edited_post.content = request.form['content']
    edited_post.tags = tags
    db.session.add(edited_post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Deletes selected post"""

    selected_post = Post.query.get(post_id)
    author = User.query.get(selected_post.user_id)
    db.session.delete(selected_post)
    db.session.commit()

    return redirect(f'/users/{author.id}')

@app.route('/tags')
def tags_list():
    """Shows a list of tags"""

    tags= Tag.query.all()

    return render_template('tags-list.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """Shows tag details and a list of posts associated with that tag"""

    selected_tag = Tag.query.get(tag_id)
    tag_posts = selected_tag.posts

    return render_template(f'posts-by-tag.html', tag=selected_tag, posts=tag_posts)

@app.route('/tags/new')
def new_tag_form():
    """Displays the page with the form to create a new tag"""

    return render_template('new-tag.html')

@app.route('/tags/new', methods=['POST'])
def new_tag_form_submit():
    name = request.form['name']
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    selected_tag = Tag.query.get(tag_id)

    return render_template('edit-tag.html', tag=selected_tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag_form_submit(tag_id):
    edited_tag = Tag.query.get(tag_id)
    edited_tag.name = request.form['name']
    db.session.add(edited_tag)
    db.session.commit()

    return redirect(f'/tags/{edited_tag.id}')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag_to_delete = Tag.query.get(tag_id)
    db.session.delete(tag_to_delete)
    db.session.commit()

    return redirect('/tags')