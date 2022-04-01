from flask import Blueprint, render_template, request, flash,redirect,url_for,session,send_file,send_from_directory
from werkzeug.utils import secure_filename
from github_storage_system import git_file_server
from flask import current_app as app
from flask_login import login_required, current_user,login_user,logout_user
import os
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User,db,Post
from datetime import datetime
import json

user_management = Blueprint("user_management",__name__,template_folder='templates_user_management')

git_api = git_file_server("file_uploaded")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@user_management.route("/dashboard", methods=['POST', 'GET'])
@login_required
def dashboard():

    return render_template("dashboard.html", user=current_user)

@user_management.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        category = request.form.get('category')
        name = request.form.get('name')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            now = datetime.now()
            filename =  str(now)+filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #filepath = os.path.abspath(f"file_uploaded/{filename}")
            try:
                git_api.push_file(f"file_uploaded/{filename}")
            except:
                git_api.delete_file(f"file_uploaded/{filename}")
                git_api.push_file(f"file_uploaded/{filename}")
            
            github_file_link = git_api.pull_absolute_file_link(f"file_uploaded/{filename}")
            new_post = Post(github_link=github_file_link, name=name, filename=filename, category=category,user_id=current_user.id,username=current_user.name)

            # add the new post to the database
            db.session.add(new_post)
            db.session.commit()
            flash(f"Uploaded {filename}")
            return redirect(url_for("user_management.dashboard"))
    flash("No file selected")        
    return redirect(url_for("user_management.dashboard"))

@user_management.route('/settings')
@login_required
def settings():
    
    return render_template('settings.html',user=current_user)

@user_management.route('/settings',methods=['POST'])
@login_required
def settings_post():
    username = request.form.get('username')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    user = User.query.filter_by(email=current_user.email).first()
    if not user or not check_password_hash(user.password, old_password):
        flash('Your Old password is wrong')
        return redirect(url_for('user_management.settings')) # if the user doesn't exist or password is wrong, reload the page
    user.name=username
    
    if not new_password == "":
        user.password=generate_password_hash(new_password, method='sha256')
    db.session.commit()
    flash('Updated Successfully')
    return redirect(url_for('user_management.settings'))

@user_management.route('/delete-post', methods=['POST'])
@login_required
def delete_post():
    note = json.loads(request.data)
    PostId = note['noteId']
    post = Post.query.get(PostId)
    if post:
        if post.user_id == current_user.id:
            db.session.delete(post)
            db.session.commit()

    return jsonify({})

@user_management.route("/delete-user",methods=['POST'])
@login_required
def delete_user():
    user_json = json.loads(request.data)
    UserId = user_json['userId']
    user = User.query.get(UserId)
    if user:
        print(user)
        if user.id == current_user.id:
            db.session.delete(user)
            db.session.commit()