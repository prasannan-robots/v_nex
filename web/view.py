from flask import Blueprint, render_template, request, flash,redirect,url_for,session,send_file
from werkzeug.utils import secure_filename # for files uploading
import os
from flask_login import login_required, current_user
from .models import Post

view = Blueprint('view',__name__,template_folder='templates') # adding blueprint

@view.route('/')
def home():
    post = [post.category for post in Post.query.all()]
    post = list(set(post))
    return render_template('home.html',user=current_user,post=post)

@view.route('/look',methods=['POST'])
def look_image():
    category=request.form.get("categoryselector")
    print(category)
    post = [i for i in Post.query.filter_by(category=category).all()]
    post_no = len(post)
    print(post_no)
    #https://raw.githubusercontent.com/gagaan-tech/v_nex_data/main/file_uploaded/Marshanicky.png
    posts_category = [post.category for post in Post.query.all()]
    return render_template('looks.html',posts_category=post,post=posts_category,post_no=post_no)
    

@view.route('/look')
def look():
    post = [post.category for post in Post.query.all()]
    return render_template('looks.html',post=post)
