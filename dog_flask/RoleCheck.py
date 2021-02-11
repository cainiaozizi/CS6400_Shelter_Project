import mysql.connector
from connection_info import db_con_user, db_con_pass, db_con_host, db_con_db

from flask_jwt import current_identity
from flask_jwt import jwt_required
from flask_restful import Resource



class Admin(Resource):
    #@jwt_required()
    def get(self):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                         host=db_con_host,
                                         database=db_con_db)
        cursor = connection.cursor()

        select_query = "SELECT email_address FROM Mo WHERE email_address=%s"
        # cursor.execute(select_query, (current_identity.username,))
        cursor.execute(select_query, (current_identity.username,))
        result = cursor.fetchone()

        if result:
            return {"Admin": "True"}
        return {"Admin": "False"}