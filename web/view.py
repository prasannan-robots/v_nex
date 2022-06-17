from flask import Blueprint, render_template, request, flash,redirect,url_for,session,send_file
from werkzeug.utils import secure_filename # for files uploading
import os
from flask_login import login_required, current_user
from .models import Post

view = Blueprint('view',__name__,template_folder='templates') # adding blueprint

@view.route('/about')
def home():
    post = [post.category for post in Post.query.all()]
    post = list(set(post))
    return render_template('home.html',user=current_user,post=post)

@view.route('/',methods=['POST'])
def look_image():
    subject=request.form.get("subjectselector")
    standard=request.form.get("standardselector")
    if subject == "":
        post = [i for i in Post.query.filter_by(standard=standard).all()]
    elif standard == "":
        post = [i for i in Post.query.filter_by(subject=subject).all()]
    else:
        post = [i for i in Post.query.filter_by(subject=subject,standard=standard).all()]
    post_no = len(post)
    #https://raw.githubusercontent.com/gagaan-tech/v_nex_data/main/file_uploaded/Marshanicky.png
    posts_subject = [post.subject for post in Post.query.all()]
    posts_standard = [post.standard for post in Post.query.all()]
    posts_subject = list(set(posts_subject))
    posts_standard = list(set(posts_standard))
    return render_template('looks.html',post=post,post_no=post_no,posts_standard=posts_standard,posts_subject=posts_subject)
    

@view.route('/')
def look():
    posts_subject = [post.subject for post in Post.query.all()]
    posts_standard = [post.standard for post in Post.query.all()]
    posts_subject = list(set(posts_subject))
    posts_standard = list(set(posts_standard))
    return render_template('looks.html',posts_standard=posts_standard,posts_subject=posts_subject,category="Select Category ->")
