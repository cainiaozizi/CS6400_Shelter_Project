from flask_restful import Resource, reqparse
from flask import request
from flask_jwt import jwt_required
import mysql.connector
from connection_info import db_con_user, db_con_pass, db_con_host, db_con_db
from datetime import date
import datetime


# from dateutil.relativedelta import relativedelta
from collections import defaultdict


class animal_control_report(Resource):
    # #@jwt_required()

    def get(self):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        mycursor = connection.cursor()



        cur_year_month = int(date.today().strftime('%Y%m'))
        total_months = [cur_year_month]
        for i in range(6):
            previous_month = date.today() - datetime.timedelta(days = 30*i)
            total_months.append(int(previous_month.strftime('%Y%m')))

        report_summary = defaultdict(list)



        sql_query_animal_control_report_col1 = "SELECT num_of_dogs, year_month_sur FROM AnimalControlReportSurrenderDogsView"
        mycursor.execute(sql_query_animal_control_report_col1)
        results1 = mycursor.fetchall() #a list of tuples, each tuple is for a dog
        # SurrenderedDogs = []
        # for _result in results1:
        #     SurrenderedDogs.append({'year_month_sur':_result[1], 'num_of_dogs':_result[0]})

        SurrenderedDogs = defaultdict()
        for _result in results1:
            SurrenderedDogs[str(_result[1])] = _result[0]

        for month in total_months:
            if str(month) in SurrenderedDogs.keys():
                report_summary[str(month)].append(SurrenderedDogs[str(month)])
            else:
                report_summary[str(month)].append(0)



        
        sql_query_animal_control_report_col2 = "SELECT num_of_adopted_dogs_over60days, year_month_ado FROM AnimalControlReportOver60DaysView"
        mycursor.execute(sql_query_animal_control_report_col2)
        results2 = mycursor.fetchall() #a list of tuples, each tuple is for a dog
        # AdoptedDogs = []
        # for _result in results2:
        #     AdoptedDogs.append({'year_month_ado':_result[1], 'num_of_adopted_dogs_over60days':_result[0]})

        AdoptedDogs = defaultdict()
        for _result in results2:
            AdoptedDogs[str(_result[1])] = _result[0]

        for month in total_months:
            if str(month) in AdoptedDogs.keys():
                report_summary[str(month)].append(AdoptedDogs[str(month)])
            else:
                report_summary[str(month)].append(0)



        sql_query_animal_control_report_col3 = "SELECT expense_amount, year_month_exp FROM AnimalControlReportExpenseAmountView"
        mycursor.execute(sql_query_animal_control_report_col3)
        results3 = mycursor.fetchall() #a list of tuples, each tuple is for a dog
        # ExpenseTotal = []
        # for _result in results3:
        #     ExpenseTotal.append({'year_month_exp':_result[1], 'expense_amount':_result[0]})

        ExpenseTotal = defaultdict()
        for _result in results3:
            ExpenseTotal[str(_result[1])] =round(float(_result[0]),2)

        for month in total_months:
            if str(month) in ExpenseTotal.keys():
                report_summary[str(month)].append(ExpenseTotal[str(month)])
            else:
                report_summary[str(month)].append(0)
        
        seven_month_summary = []
        for year_month, monthly_summary in dict(report_summary).items():
            seven_month_summary.append({'year_month': year_month, 'monthly_summary':monthly_summary}) 

            
        connection.commit()
        connection.close()
        return seven_month_summary # NOTE for frontend: monthly_summary is list of number [SurrenderedDogs, AdoptedDogs, ExpenseTotal]



class animal_control_detail_1(Resource):
    # #@jwt_required()

    def get(self, year_month):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        mycursor = connection.cursor()

        sql_query_animal_control_report_detail1 = "SELECT d.dog_ID, d.sex, d.alteration_status, d.microchip_ID, d.surrender_date, db.breed_name \
                                                    FROM Dog AS d INNER JOIN ( \
                                                    SELECT dog_ID, GROUP_CONCAT(breed_name ORDER BY breed_name ASC SEPARATOR '/') AS breed_name \
                                                  FROM DogBreed \
                                                  GROUP BY dog_ID ) AS db ON d.dog_ID = db.dog_ID \
                                                WHERE d.surrendered_by_animal_control = 1 AND EXTRACT(YEAR_MONTH FROM d.surrender_date) = %s  \
                                                 ORDER BY d.dog_ID ASC"

        # sql_query_animal_control_report_detail1 = "SELECT dog_ID, sex, alteration_status, microchip_ID, surrender_date, breed_name FROM AnimalControlReportDetailView1"
        mycursor.execute(sql_query_animal_control_report_detail1, (int(year_month),))
        results = mycursor.fetchall() #a list of tuples, each tuple is for a dog
        SurrenderedDogsDetail = []
        
        if results:
            for _result in results:
                if isinstance(_result[4], (datetime.datetime, date)):
                    surrender_date = _result[4].isoformat()

                SurrenderedDogsDetail.append({'dog_ID':_result[0], 'sex':_result[1], 'alteration_status':_result[2], 'microchip_ID':_result[3], 'surrender_date':surrender_date, 'breed_name':_result[5] })
            connection.commit()
            connection.close()
            return SurrenderedDogsDetail

        # return {'message': 'Detail Not found'}, 404
        return {'message': 'Detail Not found'}

class animal_control_detail_2(Resource):
    # #@jwt_required()

    def get(self, year_month):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        mycursor = connection.cursor()

        sql_query_animal_control_report_detail2 = "SELECT d.dog_ID, d.sex, d.alteration_status, d.microchip_ID, d.surrender_date, db.breed_name,\
                                                    DATEDIFF(Adoption.adoption_date, d.surrender_date) AS days_in_rescue \
                                                      FROM Dog AS d LEFT JOIN (\
                                                          SELECT dog_ID, GROUP_CONCAT(breed_name ORDER BY breed_name ASC SEPARATOR '/') AS breed_name\
                                                          FROM DogBreed\
                                                          GROUP BY dog_ID ) AS db\
                                                      ON d.dog_ID = db.dog_ID INNER JOIN Adoption On d.dog_ID = Adoption.dog_ID\
                                                      WHERE d.surrendered_by_animal_control = 1 AND EXTRACT(YEAR_MONTH FROM Adoption.adoption_date) = %s \
                                                       AND DATEDIFF(Adoption.adoption_date, d.surrender_date) >=60 \
                                                      ORDER BY days_in_rescue DESC, d.dog_ID DESC"

        # sql_query_animal_control_report_detail2 = "SELECT dog_ID, sex, alteration_status, microchip_ID, surrender_date, breed_name, days_in_rescue FROM AnimalControlReportDetailView2"
        mycursor.execute(sql_query_animal_control_report_detail2, (int(year_month),))
        results = mycursor.fetchall() #a list of tuples, each tuple is for a dog
        AdoptedDogsDetail = []

        
        if results:
            for _result in results:
                if isinstance(_result[4], (datetime.datetime, date)):
                    surrender_date = _result[4].isoformat()

                AdoptedDogsDetail.append({'dog_ID':_result[0], 'sex':_result[1], 'alteration_status':_result[2], 'microchip_ID':_result[3], 'surrender_date':surrender_date, 'breed_name':_result[5], 'days_in_rescue':_result[6] })
            connection.commit()
            connection.close()

            return AdoptedDogsDetail


        # return {'message': 'Detail Not found'}, 404
        return {'message': 'Detail Not found'}

class adoption_report(Resource):
    # #@jwt_required()

    def get(self):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        mycursor = connection.cursor()

        sql_query_adoption_report = """ SELECT EXTRACT(YEAR_MONTH FROM adoption_date) AS adoption_month, db.breed_name, COUNT(d.dog_ID) AS num_of_dog_surrender, 
                                      COUNT(a.dog_ID) AS num_of_dog_adopted, SUM(e.total_expense) AS sum_dog_expense, SUM(a.adoption_fee) AS sum_adoption_fee, (SUM(a.adoption_fee) - SUM(e.total_expense)) 
                                      AS net_profit 
                                      FROM Dog AS d INNER JOIN (
                                          SELECT dog_ID, GROUP_CONCAT(breed_name ORDER BY breed_name ASC SEPARATOR '/') AS breed_name
                                          FROM DogBreed
                                          GROUP BY dog_ID) AS db ON d.dog_ID = db.dog_ID 
                                      INNER JOIN Adoption AS a ON d.dog_ID = a.dog_ID
                                      INNER JOIN (
                                        SELECT dog_ID, SUM(amount) as total_expense
                                        FROM Expense
                                        GROUP BY dog_ID) AS e ON d.dog_ID = e.dog_ID 
                                      WHERE PERIOD_DIFF(EXTRACT(YEAR_MONTH FROM CURDATE()), EXTRACT(YEAR_MONTH FROM a.adoption_date)) <=12 
                                      GROUP BY adoption_month, db.breed_name
                                      ORDER BY adoption_month, db.breed_name ASC;"""
        mycursor.execute(sql_query_adoption_report)
        results = mycursor.fetchall() #a list of tuples, each tuple is for a dog
        AdoptedReport = []
        for _result in results:
            AdoptedReport.append({'adoption_month':_result[0], 'breed_name':_result[1], 'num_of_dog_surrender':_result[2], \
                'num_of_dog_adopted':_result[3], 'sum_dog_expense':round(float(_result[4]),2), 'sum_adoption_fee':round(float(_result[5]),2), 'net_profit':round(float(_result[6]),2) })
        connection.commit()
        connection.close()


        return AdoptedReport


class expense_report(Resource):
    # #@jwt_required()

    def get(self):
        connection = mysql.connector.connect(user=db_con_user, password=db_con_pass,
                                             host=db_con_host,
                                             database=db_con_db)

        mycursor = connection.cursor()

        sql_query_expense_report = "SELECT vendor_name, total FROM ExpenseAnalysisReportView"
        mycursor.execute(sql_query_expense_report)
        results = mycursor.fetchall() #a list of tuples, each tuple is for a dog
        expenses = []
        for result in results:
            expenses.append({'vendor_name':result[0], 'total':round(float(result[1]), 2)})
        
        connection.commit()
        connection.close()

        return expenses
