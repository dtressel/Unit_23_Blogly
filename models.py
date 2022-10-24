"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
        )
    first_name = db.Column(
        db.String,
        nullable=False
        )
    last_name = db.Column(
        db.String,
        nullable=False
        )
    image_url = db.Column(db.String)

    posts = db.relationship('Post')

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
        )
    title = db.Column(
        db.String(50),
        nullable=False
        )
    content = db.Column(
        db.String,
        nullable=False
        )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now
        )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    user = db.relationship('User')

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
        )
    name = db.Column(
        db.String(15),
        nullable=False
    )

    posts = db.relationship('Post', secondary='post_tag', backref='tags')

class PostTag(db.Model):
    __tablename__ = 'post_tag'

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True
    )
    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tags.id'),
        primary_key=True
    )