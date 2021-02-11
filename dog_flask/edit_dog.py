from flask_restful import Resource, reqparse
from flask import request
from flask_jwt import jwt_required
import mysql.connector
from datetime import date, datetime
from connection_info import db_con_user, db_con_pass, db_con_host, db_con_db

class edit_dog(Resource):
    # #@jwt_required()

    def get(self, dog_ID):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        mycursor = connection.cursor()

        print('debug 1')

        #get dog info
        sql_query_get_dog = "SELECT dog_ID, dog_name, sex, alteration_status, date_of_birth, description, microchip_ID, surrender_date, \
            surrender_reason, surrendered_by_animal_control, adoptability_status, email_address FROM Dog WHERE dog_ID = %s"
        mycursor.execute(sql_query_get_dog, (dog_ID,))
        result = mycursor.fetchone() #fetchone return a tuple
        
        sql_query_get_breed = "SELECT GROUP_CONCAT(DISTINCT breed_name ORDER BY breed_name ASC SEPARATOR '/') AS BreedNames FROM DogBreed WHERE dog_ID = %s"
        mycursor.execute(sql_query_get_breed, (dog_ID,))
        result_breed = mycursor.fetchone()

        dog_info = []

        if result and result_breed:

            dog_info = {'dog_ID':result[0], 'dog_name':result[1], 'sex':result[2], 'alteration_status':result[3], \
                 'date_of_birth':str(result[4]), 'description':result[5], 'microchip_ID':result[6], 'surrender_date':str(result[7]), \
                     'surrender_reason':result[8],'surrendered_by_animal_control':result[9], 'adoptability_status':result[10],\
                         'email_address':result[11], 'breed': result_breed[0]}

        print("dog_info", dog_info)
        connection.close()
        return {"data" : dog_info} # Note for frontend: isAdmin is a boolean data that could be used in frontend to determine if add_adoption link should be enabled
        



    def put(self, dog_ID):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        mycursor = connection.cursor()

        
        details = request.json

        print("debug 1", details)

        sex = details.get('sex', "") #null if nothing is provided
        alteration_status = details.get('alteration_status', "") #null if nothing is provided
        microchip_ID = details.get('microchip_ID', "") #null if nothing is provided
        breeds = details.get('breed', "") # Confirm with frontend: this could be null or list of breeds

        sql_query_get_dog = "SELECT dog_ID, sex, alteration_status, microchip_ID FROM Dog WHERE dog_ID = %s"
        mycursor.execute(sql_query_get_dog, (dog_ID,))
        result_dog = mycursor.fetchone() #fetchone return a tuple
        original_sex = result_dog[1]
        original_alteration_status = result_dog[2]
        original_microchip_ID = result_dog[3]

        sql_query_get_breed = "SELECT GROUP_CONCAT(DISTINCT breed_name ORDER BY breed_name ASC SEPARATOR '/') AS BreedNames FROM DogBreed WHERE dog_ID = %s"
        mycursor.execute(sql_query_get_breed, (dog_ID,))
        original_breed = mycursor.fetchone()[0]
        
        #update breed
        print("debug 2", breeds)

        if (original_breed == "Unknown" or original_breed == "Mixed") and breeds:
            sql_query_delete_breed = "DELETE FROM DogBreed WHERE dog_ID = %s"
            mycursor.execute(sql_query_delete_breed, (dog_ID,))
            
            sql_query_insert_breed = "INSERT INTO DogBreed (dog_ID, breed_name) VALUES (%s, %s)"

            #insert breeds
            for breed in breeds:
                mycursor.execute(sql_query_insert_breed, (dog_ID, breed))

        #update sex
        if original_sex == "Unknown" and sex:
            sql_query_update_sex = "UPDATE Dog SET sex = %s WHERE dog_ID = %s"
            mycursor.execute(sql_query_update_sex, (sex, dog_ID))

        #update alteration status
        if original_alteration_status == 0 and alteration_status:
            #convert the "yes" or "no" from html to boolean
            if alteration_status == 'yes':
                alteration_status = 1
            if alteration_status == 'no':
                alteration_status = 0

            sql_query_update_alteration_status = "UPDATE Dog SET alteration_status = %s WHERE dog_ID = %s"
            mycursor.execute(sql_query_update_alteration_status, (alteration_status, dog_ID))

        #update microchip_ID
        if (not original_microchip_ID) and microchip_ID:
            sql_query_update_microchip_ID = "UPDATE Dog SET microchip_ID = %s WHERE dog_ID = %s"
            mycursor.execute(sql_query_update_microchip_ID, (microchip_ID, dog_ID))

        #update adoptability_status if either alteration status or microchip_ID is updated above
        if alteration_status or microchip_ID:
            sql_query_updated_dog = "SELECT alteration_status, microchip_ID, sex FROM Dog WHERE dog_ID = %s"
            mycursor.execute(sql_query_updated_dog, (dog_ID,))
            updated_dog = mycursor.fetchone()
            updated_alteration_status = updated_dog[0]
            updated_microchip_ID = updated_dog[1]
            updated_sex = updated_dog[2]
            sql_query_update_adoptability = "UPDATE Dog SET adoptability_status = IF(((%s = 1) AND (%s IS NOT NULL) AND (%s != 'unknown')), 'Available', 'Not Available') \
                WHERE dog_ID = %s"
            
            mycursor.execute(sql_query_update_adoptability, (updated_alteration_status, updated_microchip_ID, updated_sex, dog_ID))

        connection.commit()
      
        connection.close()
        return "success"
   
# curl -i -H "Content-Type: application/json" -X PUT -d \
#     "{\"alteration_status\":\"1\", \"breed\":[\"Golden Retriever\"]}" \
#     http://localhost:5000/api/edit_dog/mo_aefz@gmail.com/9
