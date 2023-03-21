from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

from flask_app.models import model_users

class Liked_show:
    def __init__(self,data:dict):
        #for every column in table from db, must have an attribute
        self.user_id = data['user_id']
        self.tv_show_id = data['tv_show_id']

#C
    @classmethod
    def create(cls,data):
        query = "INSERT INTO liked_shows (user_id, tv_show_id) VALUES (%(user_id)s,%(tv_show_id)s);"
        liked_show_id = connectToMySQL(DATABASE).query_db(query, data) 
        return liked_show_id

    @classmethod
    def delete(cls,data):
        print(data)
        query = "DELETE FROM liked_shows WHERE (user_id = %(user_id)s )and(tv_show_id = %(tv_show_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)
