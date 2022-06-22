from flask import Blueprint, render_template, request, flash,redirect,url_for,session,send_file,send_from_directory
from werkzeug.utils import secure_filename
from github_storage_system import git_file_server
from flask import current_app as app
from flask_login import login_required, current_user,login_user,logout_user
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from .models import Image, User,db,Post
from datetime import datetime
import json

user_management = Blueprint("user_management",__name__,template_folder='templates_user_management')

git_api = git_file_server(path_of_upload_folder="file_uploaded")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
SUBJECT_LIST = os.getenv("SUBJECT_LIST")
STANDARD_LIST = os.getenv("STANDARD_LIST")

SUBJECT_LIST = list(SUBJECT_LIST.split(","))
STANDARD_LIST = list(STANDARD_LIST.split(","))
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@user_management.route("/dashboard", methods=['POST', 'GET'])
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user,posts_subject=SUBJECT_LIST,posts_standard=STANDARD_LIST)

@user_management.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST' and request.files.getlist('file[]'):
        print(request.files)
        
        # check if the post request has the file part
        if 'file[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('file[]')
        standard = request.form.get('standardselector')
        subject = request.form.get('subjectselector')
        description = request.form.get('description')
        for i in files:
            if i.filename=="":
                flash('No selected file if you are uploading from gallery (Gallery file upload is not supported please try to upload from file)')
                return redirect(request.url)
            if not i:
                flash('No selected file if you are uploading from gallery (Gallery file upload is not supported please try to upload from file)')
                return redirect(request.url)
            print(i.content_type)
        now = datetime.now()
        unique_id =  str(now)
        new_post = Post(description=description, standard=standard,subject=subject,user_id=current_user.id,username=current_user.name,unique_id=unique_id)
        db.session.add(new_post)
        db.session.commit()
        print(files)
        
        for file in files:
            
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            print(file.filename)
            if file.filename == '':
                flash('No selected file if you are uploading from gallery (Gallery file upload is not supported please try to upload from file)')
                return redirect(request.url)
            if not file:
                flash('No selected file if you are uploading from gallery (Gallery file upload is not supported please try to upload from file)')
                return redirect(request.url)
            else:

                if file and allowed_file(file.filename):
                    filename_pure = file.filename
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
                    p = Post.query.filter_by(description=description, standard=standard,subject=subject,user_id=current_user.id,username=current_user.name,unique_id=unique_id).first()
                    
                    images = Image(link=github_file_link,post_id=p.id,file_name=filename,file_pure_name=filename_pure)
                    # add the new post to the database
                    db.session.add(images)
                
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
            for i in post.images:
                git_api.delete_file(f"file_uploaded/{i.file_name}")
                db.session.delete(i)
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
        if user.id == current_user.id:
            db.session.delete(user)
            db.session.commit()
    return jsonify({})