from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
from flask_app.models import model_users,model_liked_shows


class Tv_show:
    def __init__(self,data:dict):
        #for every column in table from db, must have an attribute
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']



#validation
    @staticmethod
    def validate(data):
        is_valid = True

        if not data["title"]:
            flash("title required","err_tv_shows_title")
            is_valid=False

        if not data["network"]:
            flash("network required","err_tv_shows_network")
            is_valid=False

        if not data["release_date"] :
            flash("date required","err_tv_shows_release_date")
            is_valid=False

        if len(data["description"]) < 3:
            flash("description must have at least 3 characters.","err_tv_shows_description")
            is_valid=False

        return is_valid

#C
    @classmethod
    def create(cls,data):
        query = "INSERT INTO tv_shows (title, network, release_date,description, user_id) VALUES (%(title)s,%(network)s,%(release_date)s,%(description)s,%(user_id)s);"
        user_id = connectToMySQL(DATABASE).query_db(query, data) 

        return user_id
#R
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM tv_shows WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        
        if not results:
            return False

        return cls(results[0])

    @classmethod
    def get_one_with_creator(cls, data):
        query = "SELECT * FROM tv_shows JOIN users ON users.id = tv_shows.user_id WHERE tv_shows.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)

        for dict in results:
            tv_show_data = {
                'id' :dict['id'],
                'title' :dict['title'],
                'network' :dict['network'],
                'release_date' :dict['release_date'],
                'description' :dict['description'],
                'created_at' :dict['created_at'],
                'updated_at' :dict['updated_at'],
                'user_id' :dict['user_id'],
            }

            user_data = {
                'id' : dict['id'],
                'first_name' : dict['first_name'],
                'last_name' : dict['last_name'],
                'email' : dict['email'],
                'password' : dict['password'],
                'created_at' : dict['created_at'],
                'updated_at' : dict['updated_at'],
            }

            tv_show = Tv_show(tv_show_data)
            tv_show.user = model_users.User(user_data)

        return tv_show

    @classmethod
    def get_all_with_liked(cls):
        query = "SELECT * FROM tv_shows LEFT JOIN liked_shows ON tv_shows.id = tv_show_id JOIN users ON users.id = tv_shows.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        # print(results)
        # 'id': 4,
        #  'title': 'Lucifer',
        #  'network': 'netflix',
        #  'release_date': datetime.date(2023, 1, 4),
        #  'description': 'devil show',
        #  'created_at': datetime.datetime(2023, 1, 26, 11, 48, 56),
        #  'updated_at': datetime.datetime(2023, 1, 26, 11, 59, 42),
        #  'user_id': 1,
        # 
        #  'liked_shows.user_id': 1,
        #  'tv_show_id': 4,

        #  'users.id': 1,
        #  'first_name': 'Jesse',
        #  'last_name': 'Thommes',
        #  'email': 'jt@email.com',
        #  'password': '$2b$12$DexEPjUsoaAJ96cX7sPjjOoAyJzBKTS7m70b5iwUMhoFelBsP2Pva',
        #  'users.updated_at': datetime.datetime(2023, 1, 26, 11, 38, 4),
        #  'users.created_at': datetime.datetime(2023, 1, 26, 11, 38, 4)},

        if not results:
            return []

        all_tv_shows = []
        for dict in results:
            tv_show_data = {
                'id' : dict['id'],
                'title' : dict['title'],
                'network' : dict['network'],
                'description' : dict['description'],
                'release_date' : dict['release_date'],
                'created_at' : dict['created_at'],
                'updated_at' : dict['updated_at'],
                'user_id' : dict['user_id'],
            }
            
            user_data = {
                'id':dict['users.id'],
                'first_name' : dict['first_name'],
                'last_name' : dict['last_name'],
                'email' : dict['email'],
                'password' : dict['password'],
                'created_at' : dict['created_at'],
                'updated_at' : dict['updated_at'],
            }

            liked_data = {
                'user_id':dict['liked_shows.user_id'],
                'tv_show_id': dict['tv_show_id'],
            }

            tv_show = cls(tv_show_data)
            tv_show.users = model_users.User(user_data)
            tv_show.liked = model_liked_shows.Liked_show(liked_data)
            all_tv_shows.append(tv_show)
            
        return all_tv_shows


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM tv_shows"
        results = connectToMySQL(DATABASE).query_db(query)

        all_tv_shows = []
        for dict in results:
            all_tv_shows.append(cls(dict))

        return all_tv_shows

#U
    @classmethod
    def update_one(cls,data):
        query = "UPDATE tv_shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description =%(description)s WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query,data)
#D
    @classmethod
    def delete_one(cls,data):
        query = "DELETE FROM tv_shows WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query,data)