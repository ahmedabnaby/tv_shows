from flask import render_template,redirect,request
from flask_app import app

from flask_app.models.model_liked_shows import Liked_show

@app.route('/liked_show/user/create',methods=["post"])
def liked_show_user_create():
    data = request.form
    Liked_show.create(data)
    return redirect(f'/user/{data["user_id"]}')

@app.route('/liked_show/tv_show/create',methods=["post"])
def liked_show_tv_show_create():
    data = request.form
    Liked_show.create(data)
    return redirect(f'/tv_show/{data["tv_show_id"]}')

@app.route('/liked_show/user/delete',methods=["post"])
def liked_show_user_delete():
    data = request.form
    Liked_show.delete(data)
    return redirect(f'/user/{data["user_id"]}')