from flask import Blueprint, render_template, request, flash,redirect,url_for,session,send_file,send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .models import User,db,Post
from flask_login import login_required, current_user,login_user,logout_user
from flask import current_app as app
import os
from github_storage_system import git_file_server

authentication = Blueprint("authentication",__name__,template_folder='templates_login')
github_tokens = "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"
github_repos = "gagaan-tech/v_nex_data"
git_api = git_file_server("file_uploaded",github_tokens,github_repos,"main")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@authentication.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        category = request.form.get('category')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #filepath = os.path.abspath(f"file_uploaded/{filename}")
            git_api.push_file(f"file_uploaded/{filename}")
            
            github_file_link = git_api.pull_absolute_file_lin(f"file_uploaded/{filename}")

            new_post = Post(github_link=github_file_link, name=filename, category=category,user_id=current_user.id)

            # add the new post to the database
            db.session.add(new_post)
            db.session.commit()
            flash(f"Uploaded {filename}")
            return redirect(url_for("authentication.dashboard"))
    flash("No file selected")        
    return redirect(url_for("authentication.dashboard"))

@authentication.route('/downloadfile/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

@authentication.route('/login')
def login():
    return render_template('login.html')

@authentication.route("/dashboard", methods=['POST', 'GET'])
@login_required
def dashboard():
    return render_template("dashboard.html", name=current_user.name)

@authentication.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('view.home'))

@authentication.route('/signup')
def signup():
    return render_template('signup.html')

@authentication.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('authentication.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('authentication.login'))

@authentication.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('authentication.login')) # if the user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    
    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('authentication.dashboard'))