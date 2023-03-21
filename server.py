from flask_app import app
from flask_app.controllers import controller_liked_shows, controller_routes, controller_tv_shows, controller_users

if __name__ == "__main__":
    app.run(debug=True)