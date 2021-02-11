from flask_restful import Resource, reqparse
from flask import request
from flask_jwt import jwt_required, current_identity
import mysql.connector
from connection_info import db_con_user, db_con_pass, db_con_host, db_con_db

class add_dog(Resource):
    #@jwt_required()
    
    def post(self):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        mycursor = connection.cursor()
            
        #frontend already validate input format

        details = request.get_json()

        print(details)
       
        dog_name = details['dog_name']
        surrender_reason = details['surrender_reason']
        sex = details['sex']  #ENUM

        print("debug 1: details", details)

        surrendered_by_animal_control = details['surrendered_by_animal_control'] #boolean
        alteration_status = details['alteration_status'] #boolean

        surrender_date = details['surrender_date']
        date_of_birth = details['date_of_birth']


        microchip_ID = details.get('microchip_ID', "") #null if nothing is provided
        description = details.get('description', "") #null if nothing is provided

        print("debug 2: info", dog_name, surrender_date)
        
        #check dog_name, which can't be "Uga"
        if dog_name =='Uga':
            return {'error message': "Dog's name can't be Uga"}

        #check microchip_ID uniqueness except for null value
        if microchip_ID:
            sql_query_check_microchip_ID = "SELECT IF (EXISTS (SELECT 1 FROM Dog WHERE microchip_ID = %s), 1, 0) "
            mycursor.execute(sql_query_check_microchip_ID, (microchip_ID,))
            micro_ID_Uniq = mycursor.fetchone()[0]
            if micro_ID_Uniq == 1:
                connection.close()
                return {'error message': 'the microchip_ID exists'}
        

        #convert the "yes" or "no" from html to boolean #TODO: check if it works the same way with VUE
        if alteration_status == 'yes':
            alteration_status = 1
        if alteration_status == 'no':
            alteration_status = 0
        if surrendered_by_animal_control == 'yes':
            surrendered_by_animal_control = 1
        if surrendered_by_animal_control == 'no':
            surrendered_by_animal_control = 0


        #calculate adoptability_status
        if alteration_status == 1 and microchip_ID:
            adoptability_status = "Available"
        else:
            adoptability_status = "Not Available"


        
        print("debug 3: info", alteration_status)

        #insert info except for breed
        sql_query = "INSERT INTO Dog (dog_name, sex, alteration_status, date_of_birth, description, \
                microchip_ID, surrender_date, surrender_reason, surrendered_by_animal_control, \
                email_address, adoptability_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        vals = (dog_name, sex, alteration_status, date_of_birth, description, microchip_ID,\
        surrender_date, surrender_reason, surrendered_by_animal_control, current_identity.username, adoptability_status)
        mycursor.execute(sql_query, vals)

        #get the dog_ID for the inserted dog
        sql_query_get_dogID = "SELECT max(dog_ID) FROM Dog"
        mycursor.execute(sql_query_get_dogID)
        dog_ID = mycursor.fetchone()[0] #fetchone return a tuple

        #insert dog breeds
        breeds = details['breed']  # Note for frontend: only allow one choice one time, check if the breed is "unknow" or "mixed" to determine if the add_breed should be enabled
        sql_query_breed = "INSERT INTO DogBreed (dog_ID, breed_name) VALUES (%s, %s)"

        print("debug 4: info", dog_ID, breeds)
 
        for breed in breeds:
            mycursor.execute(sql_query_breed, (dog_ID, breed))

        connection.commit()
        print(mycursor.rowcount, "record inserted.")
        connection.close()
        return "success"
    

##test command for GET method (show a empty form):
    # curl -i http://localhost:5000/add_dog

##test command for POST method (add a dog including all the three lines):
    # curl -i -H "Content-Type: application/json" -X POST -d \
    # "{\"dog_name\":\"test4\", \"sex\":\"Female\", \"alteration_status\":\"1\", \"date_of_birth\":\"2019-12-01\", \"description\":\"she is beautiful\", \"microchip_ID\":\"12345678\", \"surrender_date\":\"2020-06-01\", \"surrender_reason\":\"I dont know\", \"surrendered_by_animal_control\":\"1\", \"breed\":[\"Collie\", \"Boxer\"]}" \
    # http://localhost:5000/api/add_dog/mo_aefz@gmail.com







