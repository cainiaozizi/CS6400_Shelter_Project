from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required, current_identity
import mysql.connector
from connection_info import db_con_user, db_con_pass, db_con_host, db_con_db

##Testing IsAdmin:
from user import User


class Applicant(Resource):
    #@jwt_required()


    def get(self, email_address):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        cursor = connection.cursor()

        select_query = "SELECT last_name, first_name, email_address,phone_number, street, city, state, zip_code FROM applicant WHERE email_address = %s"
        cursor.execute(select_query, (email_address,))
        applicant = cursor.fetchone()

        if applicant:
            return [{'last_name': applicant[0],
                    'first_name': applicant[1],
                    'email_address': applicant[2],
                    'phone_number': applicant[3],
                    'street': applicant[4],
                    'city': applicant[5],
                    'state': applicant[6],
                    'zip_code': applicant[7],
                    }]
        return {'message': 'User Not Found'}, 404

        connection.close()

    def post(self, email_address):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        cursor = connection.cursor()
        data = request.get_json()

        query = "INSERT INTO applicant(email_address,last_name, first_name, street, city, state, zip_code, phone_number) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (email_address, data['last_name'], data['first_name'], data['street'], data['city'], data['state'], data['zip_code'], data['phone_number']))

        connection.commit()
        connection.close()

class ApplicantList(Resource):
    #@jwt_required()
    def get(self):
        pass