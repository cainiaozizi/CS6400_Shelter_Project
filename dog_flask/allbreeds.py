
from flask_restful import Resource, reqparse
from flask import request
from flask_jwt import jwt_required
import mysql.connector
from connection_info import db_con_user, db_con_pass, db_con_host, db_con_db


class allbreeds(Resource):
    def get(self):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        mycursor = connection.cursor()

        sql_query_get_breeds = "SELECT breed_name FROM Breed"
        mycursor.execute(sql_query_get_breeds)
        results = mycursor.fetchall()
        breeds = []
        for breed in results:
            breeds.append(breed[0])
        
        connection.close()
        return breeds   # Note for frontend: GET method is to get all the possible breeds for dropdown list