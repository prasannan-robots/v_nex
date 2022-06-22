from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from datetime import datetime

# Creating an SQLAlchemy instance
db = SQLAlchemy()
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    posts = db.relationship('Post')
    
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    unique_id = db.Column(db.String(100),unique=True)
    description = db.Column(db.String(100))
    standard = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    username = db.Column(db.String(100))
    images = db.relationship('Image')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100))
    link = db.Column(db.String(600),unique=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    file_pure_name = db.Column(db.String(100))