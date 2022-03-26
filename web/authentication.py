from flask import Blueprint, render_template, request, flash,redirect,url_for,session,send_file


authentication = Blueprint("authentication",__name__,template_folder='templates_login')

@authentication.route('/login')
def login():
    return render_template('login.html')

@authentication.route("/dashboard", methods=['POST', 'GET'])
def dashboard():
    # if not 'username' in session and not 'password' in session:
    #     if request.method == "POST":
    #         session['username'] = request.form['username']
    #         session['password'] = request.form['password']
    return render_template("dashboard.html")

@authentication.route("/logout")
def logout():
    return "logout"

@authentication.route('/signup')
def signup():
    return render_template('signup.html')