from flask import render_template, redirect, session, request
from flask_app import app, bcrypt

from flask_app.models.model_tv_shows import Tv_show #TODO import model file here
from flask_app.models.model_users import User
# from flask_app.models.model_liked_shows import Liked_show

#route to new tv_show form page
@app.route('/tv_show/new')
def tv_show_new():
    if 'uuid' not in session:
        return redirect('/')

    user ={
        'id': session['uuid'],
        'first_name': session['first_name'],
        'last_name': session['last_name'],
        }
    return render_template("tv_show_new.html",user=user)

#route to submit create tv_show form
@app.route('/tv_show/create',methods=['post'])
def tv_show_create():
    if not Tv_show.validate(request.form):
        return redirect('/tv_show/new')

    user_id = session['uuid']
    data = {
        **request.form,
        'user_id': user_id
    }
    
    tv_show_id = Tv_show.create(data)
    
    if tv_show_id == False:
        print("Failed to create tv_show")
    else:
        print(f"tv_show Created at {tv_show_id} id")
        
    return redirect(f'/user/{user_id}')

#route to show individual tv_show
@app.route('/tv_show/<int:id>')
def tv_show_show(id):
    if 'uuid' not in session:
        return redirect('/')

    user ={
        'id': session['uuid'],
        'first_name': session['first_name'],
        'last_name': session['last_name'],
    }

    tv_show = Tv_show.get_one_with_creator({'id': id})
    liked_by = User.liked_users({'id': id})
    user_id = user['id']
    return render_template("tv_show_show.html",user=user,tv_show=tv_show,liked_by=liked_by,user_id=user_id)

#route to edit tv_show form
@app.route('/tv_show/<int:id>/edit')
def tv_show_edit(id):
    if 'uuid' not in session:
        return redirect('/')

    tv_show = Tv_show.get_one({'id': id})

    user ={
        'id': session['uuid'],
        'first_name': session['first_name'],
        'last_name': session['last_name'],
    }
    return render_template("tv_show_edit.html", tv_show=tv_show,user=user)

#route to submit edit form
@app.route('/tv_show/<int:id>/update',methods=['post'])
def tv_show_update(id):
    if not Tv_show.validate(request.form):
        return redirect(f'/tv_show/{id}/edit')

    user_id = session['uuid']
    data = {
        **request.form,
        'id':id
        }
    Tv_show.update_one(data)
    return redirect(f'/user/{user_id}')

#delete tv_show route
@app.route('/tv_show/<int:id>/delete')
def tv_show_delete(id):
    user_id = session['uuid']
    Tv_show.delete_one({'id': id})
    return redirect(f'/user/{user_id}')
