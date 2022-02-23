from flask import Flask, redirect, render_template, request, session, flash
from flask_app.models.user import User
from flask_app import app
from flask_bcrypt import Bcrypt
from datetime import datetime
bcrypt = Bcrypt(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'Invalid URL.'

@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect('/login')
    return redirect('/dashboard')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect('/login')
    data = {
        'id' : session['user_id']
    }
    user = User.get_user(data)
    return render_template('dashboard.html')

@app.route('/user_register_submit', methods=['POST'])
def user_register_submit():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    if not User.validate_user(request.form['fname'], request.form['lname'], request.form['email'], request.form['dob'], request.form['language_select'], request.form['password'], request.form['pass_confirm']):
        return redirect('/')
    data = {
        'first_name' : request.form['fname'],
        'last_name' : request.form['lname'],
        'email' : request.form['email'],
        'date_of_birth' : request.form['dob'],
        'fav_lang' : request.form['language_select'],
        'password' : pw_hash
    }
    user_id = User.register_new_user(data)
    session['user_id'] = user_id
    session['name'] = f"{request.form['fname']} {request.form['lname']}"
    session['logged_in'] = True
    return redirect('/dashboard')

@app.route('/log_out')
def log_out():
    session.clear()
    return redirect('/')

@app.route('/login_submission', methods=['POST'])
def login_submission():
    data = {
        'email' : request.form['email_login']
    }
    user_in_db = User.get_user(data)
    if not user_in_db:
        flash("Invalid email/password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(str(user_in_db[0]['password']), request.form['pass_login']):
        flash("Invalid email/password", "login")
        return redirect('/')
    session['user_id'] = user_in_db[0]['id']
    session['name'] = f"{user_in_db[0]['first_name']} {user_in_db[0]['last_name']}"
    session['logged_in'] = True
    return redirect('/')