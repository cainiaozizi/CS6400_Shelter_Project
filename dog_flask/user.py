import mysql.connector
from connection_info import db_con_user, db_con_pass, db_con_host, db_con_db

# User.Is_Admin(current_identity.username)

class User:
    def __init__(self,_id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, email_address):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)
        cursor = connection.cursor()

        select_query = "SELECT id,email_address,password FROM User WHERE email_address=%s"

        cursor.execute(select_query, (email_address,))
        result = cursor.fetchone()

        if result:
            user = cls(result[0], result[1],result[2])
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)
        cursor = connection.cursor()

        select_query = "SELECT id,email_address,password FROM user WHERE id=%s"

        cursor.execute(select_query, (_id,))
        result = cursor.fetchone()

        if result:
            user = cls(result[0], result[1],result[2])
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def Is_Admin(cls, username):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)
        cursor = connection.cursor()

        select_query = "SELECT email_address FROM Mo WHERE email_address=%s"

        cursor.execute(select_query, (username,))
        result = cursor.fetchone()

        if result:
            return {"Admin":"True"}
        return {"Admin" : "False"}



