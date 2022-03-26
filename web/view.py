from flask import Blueprint, render_template, request, flash,redirect,url_for,session,send_file
from werkzeug.utils import secure_filename # for files uploading
import os

view = Blueprint('view',__name__,template_folder='templates') # adding blueprint

@view.route('/')
def home():
    return render_template('home.html')