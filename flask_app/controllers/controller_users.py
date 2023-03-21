from flask import render_template, redirect, session, request
from flask_app import app, bcrypt

from flask_app.models.model_users import User #TODO import model file here
from flask_app.models.model_tv_shows import Tv_show
from flask_app.models.model_liked_shows import Liked_show



#route to submit create user form
@app.route('/user/create',methods=['post'])
def user_create():
    if not User.validate(request.form):
        return redirect('/')
    
    hash_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hash_pw
    }

    user_id = User.create(data)    
    if user_id == False:
        print("Failed to create user")
    else:
        print(f"User Created at {user_id} id")

    session['uuid'] = user_id
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']

    return redirect(f'/user/{user_id}')

#login
@app.route('/user/login', methods = ['post'])
def user_login():
    data = request.form
    user = User.get_one_by_email({'email':data['email']})

    if not User.validate_login(data,user):
        return redirect('/')

    session['uuid'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name

    return redirect(f'/user/{user.id}')

#route to show individual user
@app.route('/user/<int:id>')
def user_show(id):
    if 'uuid' not in session:
        return redirect('/')
    user = {
        'id': session['uuid'],
        'first_name': session['first_name'],
        'last_name': session['last_name'],
    }
    tv_shows = Tv_show.get_all_with_liked()

    return render_template("user_show.html",user=user,tv_shows=tv_shows)

#logout
@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')
