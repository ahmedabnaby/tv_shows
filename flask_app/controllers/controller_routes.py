from flask import render_template,session,redirect
from flask_app import app

#landing page
@app.route('/')
def landing_page():
    if 'uuid' in session:
        user_id = session['uuid']
        return redirect(f'/user/{user_id}')
    return render_template("index.html")
