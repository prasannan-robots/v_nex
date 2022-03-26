from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
# Creating an SQLAlchemy instance
db = SQLAlchemy()
class Profile(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    
