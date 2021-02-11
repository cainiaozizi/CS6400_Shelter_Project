from flask_restful import Resource
from flask import request
from flask_jwt import jwt_required
import mysql.connector
from connection_info import db_con_user, db_con_pass, db_con_host, db_con_db


class EligibleApplication(Resource):
    #@jwt_required()


    def get(self, last_name):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        cursor = connection.cursor()

        select_query = "SELECT DISTINCT AP.last_name, AP.first_name,AP.email_address, AP.street, AP.city, AP.state, AP.zip_code, AP.phone_number, AA.coapplicant_last_name, AA.coapplicant_first_name " \
                       "FROM Applicant AS AP" \
                       " INNER JOIN AdoptionApplication AS AA ON AA.email_address = AP.email_address" \
                       " WHERE (AA.coapplicant_last_name LIKE %s OR AP.last_name LIKE %s) AND AA.application_ID IN ( SELECT application_ID FROM ApprovedApplication);"

        cursor.execute(select_query, ("%"+last_name+"%", "%"+last_name+"%"))
        applicant = cursor.fetchall()
        applicant_dict = []

        for applicant in applicant:
            applicant_dict.append({'last_name': applicant[0],
                    'first_name': applicant[1],
                    'email_address': applicant[2],
                    'phone_number': applicant[3],
                    'street': applicant[4],
                    'city': applicant[5],
                    'state': applicant[6],
                    'zip_code': applicant[7],
                    'coapplicant_last_name': applicant[8],
                    'coapplicant_first_name': applicant[9],
                    })


        if applicant:
            return applicant_dict
        return {'message': 'No Match'}, 404

        connection.close()

class LatestApplication(Resource):
    #@jwt_required()


    def get(self, Applicant_email):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        cursor = connection.cursor()

        find_query = "SELECT MAX(application_ID) FROM AdoptionApplication" \
                       " WHERE email_address = %s AND application_ID IN" \
                       " (SELECT application_ID FROM ApprovedApplication);"

        cursor.execute(find_query, (Applicant_email,))
        applicationID = cursor.fetchone()

        select_query = "SELECT AA.application_ID, AA.application_date, AP.last_name, AP.first_name, AP.email_address, AA.coapplicant_last_name, AA.coapplicant_first_name " \
                       "FROM Applicant AS AP " \
                       "INNER JOIN AdoptionApplication AS AA ON AA.email_address = AP.email_address" \
                       " WHERE AA.application_ID = %s;"

        cursor.execute(select_query, (applicationID[0],))
        latestapp = cursor.fetchone()
        return {    'application_ID': latestapp[0],
                    'application_date':str(latestapp[1]),
                    'last_name': latestapp[2],
                    'first_name': latestapp[3],
                    'email_address': latestapp[4],
                    'coapplicant_last_name': latestapp[5],
                    'coapplicant_first_name': latestapp[6],
                    }
        connection.close()

class SelectedDogFee(Resource):
    #@jwt_required()


    def get(self, dog_ID):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        cursor = connection.cursor()

        find_query = "SELECT dog_ID, dog_name FROM Dog WHERE dog_ID = %s;"

        cursor.execute(find_query, (dog_ID,))
        dog = cursor.fetchone()

        dog_dict = [{"dog_name": dog[0]}]

        select_query = "SELECT CASE" \
                       " WHEN surrendered_by_animal_control = 1 THEN adoption_expense * 0.15" \
                       " WHEN surrendered_by_animal_control = 0 THEN adoption_expense *1.15" \
                       " END AS adoption_fee " \
                       "FROM " \
                       "(SELECT SUM(EXP.amount) AS adoption_expense, EXP.dog_ID, DG.surrendered_by_animal_control " \
                       "FROM Expense AS EXP " \
                       "INNER JOIN Dog AS DG ON DG.dog_ID = EXP.dog_ID " \
                       "WHERE DG.dog_ID = %s GROUP BY DG.dog_ID)" \
                       " AS fee;"

        cursor.execute(select_query, (dog_ID,))
        dog_fee = cursor.fetchone()
        dog_dict[0]["adoption_fee"] = dog_fee[0]
        return dog_dict

        connection.close()

class SubmitAdoption(Resource):
    #@jwt_required()

    def post(self):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        cursor = connection.cursor()
        data = request.get_json()

        adoption_query = "INSERT INTO Adoption (adoption_date, adoption_fee, dog_ID, application_ID) VALUES (%s, %s, %s, %s);"
        cursor.execute(adoption_query, (data["adoption_date"], data["adoption_fee"], data["dog_ID"], data["application_ID"]))

        update_state_query = "UPDATE Dog SET adoptability_status = 'Adopted' WHERE dog_ID = %s"
        cursor.execute(update_state_query, (data["dog_ID"],))

        connection.commit()
        connection.close()