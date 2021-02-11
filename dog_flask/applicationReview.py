from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
import mysql.connector
from connection_info import db_con_user, db_con_pass, db_con_host, db_con_db



class ApplicationReview(Resource):
    #@jwt_required()

    def get(self):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        cursor = connection.cursor()
        data = request.get_json()

        query = "SELECT AA.application_ID, AA.application_Date, AA.coapplicant_last_name, AA.coapplicant_first_name, AP.email_address, AP.last_name, AP.first_name, AP.street, AP.city, AP.state, AP.zip_code, AP.phone_number" \
                " FROM AdoptionApplication AS AA INNER JOIN Applicant AS AP ON AA.email_address = AP.email_address WHERE AA.application_state = 0;"
        cursor.execute(query)
        result = cursor.fetchall()
        result_dict = []
        connection.commit()
        connection.close()

        for r in result:
            result_dict.append({"application_ID": r[0], "application_Date": str(r[1]), "coapplicant_last_name": r[2], "coapplicant_first_name": r[3], "email_address": r[4], "last_name": r[5], "first_name": r[6], "street": r[7], "city": r[8], "state": r[9], "zip_code": r[10], "phone_number": r[11]})

        return result_dict

class OneApplication(Resource):
    #@jwt_required()

    def get(self, ApplicationID):

        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        cursor = connection.cursor()
        data = request.get_json()

        query = "SELECT AA.application_ID, AA.application_date, AA.coapplicant_last_name, AA.coapplicant_first_name, AP.email_address, AP.last_name, AP.first_name, AP.street, AP.city, AP.state, AP.zip_code, AP.phone_number FROM AdoptionApplication AS AA INNER JOIN Applicant AS AP ON AA.email_address = AP.email_address WHERE AA.application_ID = %s;"
        cursor.execute(query, (ApplicationID,))
        result = cursor.fetchone()
        result_dict = []
        connection.commit()
        connection.close()

        if result:
            return [{'application_ID': result[0],
                     'application_date': str(result[1]),
                     'coapplicant_last_name': result[2],
                     'coapplicant_first_name': result[3],
                     'email_address': result[4],
                     'last_name': result[5],
                     'first_name': result[6],
                     'phone_number': result[7],
                     'street': result[8],
                     'city': result[9],
                     'state': result[10],
                     'zip_code': result[11],
                    }]
        return [{"Message": "Application Not Found"}]

class applicationapprove(Resource):
    #@jwt_required()

    def post(self, ApplicationID):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        cursor = connection.cursor()
        data = request.get_json()

        approve_query = "INSERT INTO ApprovedApplication (application_ID) VALUES (%s);"
        cursor.execute(approve_query, (ApplicationID,))

        update_state_query = "UPDATE AdoptionApplication SET application_state = 1 WHERE application_ID = %s;"
        cursor.execute(update_state_query, (ApplicationID,))

        connection.commit()
        connection.close()


class applicationreject(Resource):
    #@jwt_required()

    def post(self, ApplicationID):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        cursor = connection.cursor()
        data = request.get_json()

        reject_query = "INSERT INTO RejectedApplication (application_ID) VALUES (%s);"
        cursor.execute(reject_query, (ApplicationID,))

        update_state_query = "UPDATE AdoptionApplication SET application_state = 1 WHERE application_ID = %s;"
        cursor.execute(update_state_query, (ApplicationID,))

        connection.commit()
        connection.close()