from flask_restful import Resource, reqparse
from flask import request
from flask_jwt import jwt_required
import mysql.connector
from connection_info import db_con_user, db_con_pass, db_con_host, db_con_db
from datetime import date, datetime


class expense(Resource):
    #@jwt_required()

    def get(self, dog_ID):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        mycursor = connection.cursor()

        #get expense info
        sql_query_get_expense = "SELECT expense_date, vendor_name, amount, description, dog_ID FROM Expense WHERE dog_ID = %s"
        mycursor.execute(sql_query_get_expense, (dog_ID,))
        result_expenses = mycursor.fetchall() #a list of tuples, each tuple is for a expense
        expenses = []
        for expense in result_expenses:

            expenses.append({'expense_date':str(expense[0]), 'vendor_name':expense[1], 'amount':expense[2], 'description':expense[3], 'dog_ID': expense[4]})
        return expenses


    def post(self, dog_ID):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        mycursor = connection.cursor()



        details = request.json
        expense_date = details['expense_date']
        vendor_name = details['vendor_name']
        amount = details['amount']
        description = details['description']
        
        #check uniqueness for (dog, vendor, date)
        sql_query_check_uniqueness = "SELECT IF (EXISTS (SELECT 1 FROM Expense WHERE expense_date = %s AND vendor_name = %s AND dog_ID = %s), 1, 0)"
        mycursor.execute(sql_query_check_uniqueness, (expense_date, vendor_name, dog_ID))
        result_uniqueness = mycursor.fetchone()[0] #return boolean data: 1 or 0 
        if result_uniqueness == 1:
            return {"error message": "Duplicate Expense"}
               
        #validate expense_date for the expense
        sql_query_check_date1 = "SELECT IF ((%s < (SELECT surrender_date FROM Dog WHERE dog_ID = %s)), 1, 0) "
        mycursor.execute(sql_query_check_date1, (expense_date, dog_ID))
        result_date1 = mycursor.fetchone()[0] #return boolean data: 1 or 0 
        if result_date1 == 1:
            return {"error message": "Expense before surrender date is invalid"}
        
        sql_query_check_date2 = "SELECT IF ((EXISTS (SELECT 1 FROM Adoption WHERE dog_ID = %s)) AND \
            (%s > (SELECT adoption_date FROM Adoption WHERE dog_ID = %s)), 1, 0)"
        mycursor.execute(sql_query_check_date2, (dog_ID, expense_date, dog_ID))
        result_date2 = mycursor.fetchone()[0] #return boolean data: 1 or 0 
        if result_date2 == 1:
            return {"error message": "Expense after adoption date is invalid"}
       

        #check if the vendor exist in table Vendor
        sql_query_check_vendor = "SELECT IF (EXISTS (SELECT 1 FROM Vendor WHERE vendor_name = %s), 1, 0)"
        mycursor.execute(sql_query_check_vendor, (vendor_name,))
        result_vendor = mycursor.fetchone()[0] #return boolean data: 1 or 0 
        ## insert vendor to table Vendor if it's a new vendor
        if result_vendor == 0:    
            sql_query_insert_vendor = "INSERT INTO Vendor (vendor_name) VALUES (%s)"
            mycursor.execute(sql_query_insert_vendor, (vendor_name,))
            connection.commit()
        
        #insert expense
        sql_query_insert_expense = "INSERT INTO Expense (dog_ID, vendor_name, expense_date, amount, description) \
            VALUES (%s, %s, %s, %s, %s)"
        mycursor.execute(sql_query_insert_expense, (dog_ID, vendor_name, expense_date, amount, description))
        
        connection.commit()
        connection.close()
        return "success"
   
   # curl -i -H "Content-Type: application/json" -X POST -d \
   #  "{\"dog_ID\":\"2\", \"vendor_name\":\"vendor_3\", \"expense_date\":\"2020-6-11\", \"amount\":\"300\", \"description\":\"dog food\"}" \
   #  http://localhost:5000/api/expense/2

    # curl -i -H "Content-Type: application/json" -X POST -d \
    # "{\"dog_ID\":\"5\", \"vendor_name\":\"vendor_3\", \"expense_date\":\"2020-6-01\", \"amount\":\"500\", \"description\":\"dog food\"}" \
    # http://localhost:5000/api/expense/5


   #  curl -i -H "Content-Type: application/json" -X POST -d \
   #  "{\"dog_ID\":\"5\", \"vendor_name\":\"vendor_1\", \"expense_date\":\"2020-5-01\", \"amount\":\"600\", \"description\":\"dog food\"}" \
   #  http://localhost:5000/api/expense/5

   #  curl -i -H "Content-Type: application/json" -X POST -d \
   #  "{\"dog_ID\":\"6\", \"vendor_name\":\"vendor_1\", \"expense_date\":\"2020-4-01\", \"amount\":\"600\", \"description\":\"dog food\"}" \
   #  http://localhost:5000/api/expense/6

