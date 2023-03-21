from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import DATABASE, bcrypt
import re
from flask_app.models import model_tv_shows

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data:dict):
        #for every column in table from db, must have an attribute
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = []
        if 'password'in data:
            self.password = data['password']
        else:
            self.password = []
        self.created_at = []
        self.updated_at = []

#validation
    @staticmethod
    def validate(data):
        is_valid = True
        pwd = data["password"]

        if len(data["first_name"]) < 2:
            flash("First name must be at least 2 characters.","err_users_first_name")
            is_valid=False

        if len(data["last_name"]) < 2:
            flash("Last name must be at least 2 characters.","err_users_last_name")
            is_valid=False

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!!!","err_users_email")
            is_valid=False

        else:
            temp_user = User.get_one_by_email({'email': data['email']})
            # print(temp_user)
            if temp_user:
                flash("Email already taken.","err_users_email")
                is_valid=False

        if len(pwd) < 8:
            flash("Password must be at least 8 characters.","err_users_password")
            is_valid=False
        elif not re.search('[0-9]', pwd or not re.search('[A-Z]', pwd)):
            flash("password must contain 1 number and uppercase letter","err_users_password")

        if data["password_confirm"] != pwd:
            flash("Passwords do not match.","err_users_password_confirm")
            is_valid=False

        return is_valid

    @staticmethod
    def validate_login(data,user):
        is_valid = True
        
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!!!","err_users_login")
            is_valid=False
        else:
            if not user:
                flash("Email is not registered","err_users_login")
                is_valid = False
            else:
                password_check = bcrypt.check_password_hash(user.password, data['password'])
                if not password_check:
                    flash ("Incorrect Password","err_users_login_pw")
                    is_valid = False

        if len(data["password"]) < 8:
            flash("Password must be at least 8 characters.","err_users_login_pw")
            is_valid=False

        return is_valid

#C
    @classmethod
    def create(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        user_id = connectToMySQL(DATABASE).query_db(query, data) 

        return user_id
#R
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        
        if not results:
            return False

        return cls(results[0])

    @classmethod
    def skeptical_users(cls,data):
        query = "SELECT * FROM users WHERE users.id NOT IN (SELECT user_id FROM liked_shows WHERE tv_show_id = %(id)s);"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if not results:
            return []

        all_users = []
        for dict in results:
            all_users.append(cls(dict))

        return all_users

    @classmethod
    def liked_users(cls,data):
        query = "SELECT * FROM users LEft JOIN liked_shows ON users.id = liked_shows.user_id WHERE liked_shows.tv_show_id =%(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if not results:
            return []
            
        all_users = []
        for dict in results:
            all_users.append(cls(dict))

        return all_users

    @classmethod
    def get_one_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        
        if not results:
            return False

        return cls(results[0])

    # @classmethod
    # def get_one_with_sighting(cls, data):
    #     query = "SELECT * FROM sightings JOIN users ON users.id = sightings.user_id WHERE sightings.id = %(id)s;"
    #     results = connectToMySQL(DATABASE).query_db(query,data)        
    #     if not results:
    #         return False
    #     user = cls(results[0])
    #     all_sightings = []
    #     for dict in results:
    #         sighting_data ={
    #             'id' : dict['id'],
    #             'name' : dict['name'],
    #             'under_30' : dict['under_30'],
    #             'instructions' : dict['instructions'],
    #             'description' : dict['description'],
    #             'date_made' : dict['date_made'],
    #             'created_at' : dict['created_at'],
    #             'updated_at' : dict['updated_at'],
    #             'user_id' : dict['user_id'],
    #         }
    #         sighting = model_sightings.Sighting(sighting_data)
    #         all_sightings.append(sighting)

    #     user.sighting = all_sightings
    #     return user

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL(DATABASE).query_db(query)

        all_users = []
        for dict in results:
            all_users.append(cls(dict))

        return all_users

#U
    @classmethod
    def update_one(cls,data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query,data)
#D
    @classmethod
    def delete_one(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query,data)