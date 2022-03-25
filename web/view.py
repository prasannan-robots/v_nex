from flask import Blueprint, render_template, request, flash,redirect,url_for,session,send_file
from werkzeug.utils import secure_filename # for files uploading
import os

view = Blueprint('view',__name__,template_folder='templates') # adding blueprint

@view.route('/')
def home():
    try:
        return render_template(f'home.html')
    except TemplateNotFound:
        abort(404)

@view.route('/login')
def login():
    try:
        return render_template(f'login.html')
    except TemplateNotFound:
        abort(404)

@view.route("/dashboard", methods=['POST', 'GET'])
def dashboard():
    if not 'username' in session and not 'password' in session:
        if request.method == "POST":
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            return render_template("dashboard.html",username=username,password=password)