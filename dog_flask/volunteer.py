from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
import mysql.connector
from connection_info import db_con_user, db_con_pass, db_con_host, db_con_db


class Volunteer(Resource):
    #@jwt_required()

    def get(self, searchname):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        cursor = connection.cursor()

        select_query = "SELECT first_name,last_name,email_address,phone_number FROM user WHERE last_name LIKE %s OR first_name LIKE %s"
        cursor.execute(select_query, ("%"+searchname+"%", "%"+searchname+"%"))
        volunteer = cursor.fetchall()
        volunteer_dict =[]

        for volunteer in volunteer:
            volunteer_dict.append({'first_name': volunteer[0],
                    'last_name': volunteer[1],
                    'email_address': volunteer[2],
                    'phone_number': volunteer[3]
                    })

        if volunteer:
            return volunteer_dict
        return {'message': 'Volunteer Not found'}, 404

        connection.close()

