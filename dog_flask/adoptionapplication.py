from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
import mysql.connector
from connection_info import db_con_user, db_con_pass, db_con_host, db_con_db



class AddApplication(Resource):
    #@jwt_required()

    def post(self, email_address):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        cursor = connection.cursor()
        data = request.get_json()

        query = "INSERT INTO AdoptionApplication (coapplicant_last_name, coapplicant_first_name, application_date, application_state, email_address) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (data['coapplicant_last_name'], data['coapplicant_first_name'], data['application_date'],0 ,email_address))

        connection.commit()
        connection.close()

class LastApplication(Resource):
    #@jwt_required()

    def get(self, email_address):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        cursor = connection.cursor()
        data = request.get_json()

        query = "SELECT MAX(application_ID) FROM AdoptionApplication"
        cursor.execute(query)
        result = cursor.fetchone()

        connection.close()
        if result:
            return [{'ApplicationID': result[0]}]
        return {'message': 'Item Not found'}, 404
