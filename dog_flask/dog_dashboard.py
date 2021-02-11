from flask_restful import Resource, reqparse
from flask import request
from flask_jwt import jwt_required
import mysql.connector
from connection_info import db_con_user, db_con_pass, db_con_host, db_con_db
from datetime import date, datetime



class dog_dashboard(Resource):
    #@jwt_required()
    
    # current_identity.username # NOTE: should I use current_identity.username to replace email_address?
    def get(self):

            connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                                 host=db_con_host,
                                                 database=db_con_db)

            mycursor = connection.cursor()

            #get all dog info:
            sql_query_get_dogs = "SELECT dog_ID, dog_name, breed_name, sex, alteration_status, age, surrender_date, adoptability_status FROM dashboardView"
            mycursor.execute(sql_query_get_dogs)
            results = mycursor.fetchall() #a list of tuples, each tuple is for a dog
            dogs = []
            print('results', results)

            if results:
                for result in results:
                    dogs.append({'dog_ID':result[0], 'dog_name':result[1], 'breed_name':result[2], 'sex':result[3], 'alteration_status':result[4], 'age':result[5], 'surrender_date':str(result[6]), 'adoptability_status':result[7]  })
                
     
           
            connection.close()
            return dogs # Note for frontend: isAdmin is a boolean data that could be used in frontend to determine if reports/review links are enabled
        




    # Note for frontend: we can use computed variable in VUE to get the available space instead of extra api
    # Note for backend: error "login required" occurs when testing. (all other classes which contain jwt-required() don't run into this error)
 
#curl -i http://localhost:5000/api/dog_dashboard/mo_aefz@gmail.com
    

class dogindex(Resource):
    #@jwt_required()
    
    # current_identity.username # NOTE: should I use current_identity.username to replace email_address?
    def get(self, dog_ID):
        
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        mycursor = connection.cursor()

        sql_query_get_dog = "SELECT dog_ID, dog_name, sex, alteration_status, date_of_birth, description, microchip_ID, surrender_date, \
            surrender_reason, surrendered_by_animal_control, adoptability_status, email_address FROM Dog WHERE dog_ID = %s"
        mycursor.execute(sql_query_get_dog, (dog_ID,))
        result = mycursor.fetchone() #fetchone return a tuple
        
        sql_query_get_breed = "SELECT GROUP_CONCAT(DISTINCT breed_name ORDER BY breed_name ASC SEPARATOR '/') AS BreedNames FROM DogBreed WHERE dog_ID = %s"
        mycursor.execute(sql_query_get_breed, (dog_ID,))
        result_breed = mycursor.fetchone()
        dog_info = []
        print('result_breed', result_breed)

        if result and result_breed:

            dog_info = {'dog_ID':result[0], 'dog_name':result[1], 'sex':result[2], 'alteration_status':result[3], \
                 'date_of_birth':str(result[4]), 'description':result[5], 'microchip_ID':result[6], 'surrender_date':str(result[7]), \
                     'surrender_reason':result[8],'surrendered_by_animal_control':result[9], 'adoptability_status':result[10],\
                         'email_address':result[11], 'breed': result_breed[0]}

            
        connection.close()
        return dog_info


