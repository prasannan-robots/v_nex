from flask import Flask,blueprints
import os
from . import models


# Create app function to create app
def create_app():
    from .view import view
    from .authentication import authentication
    app = Flask(__name__)
    # adding configuration for using a sqlite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY_FOR_FLASK")# for session
    models.db.init_app(app)
    models.db.create_all(app=app)
    app.register_blueprint(view, url_prefix='/')# added blueprint of view.py to show the page
    app.register_blueprint(authentication,url_prefix="/auth")
    return app