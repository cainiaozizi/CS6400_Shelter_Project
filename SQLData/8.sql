USE cs6400_su20_team07_final;

-- view for dog dashboard
CREATE OR REPLACE VIEW dashboardView AS
  SELECT d.dog_ID, d.dog_name, b.breed_name, d.sex, d.alteration_status, PERIOD_DIFF(EXTRACT(year_month from CURDATE()), EXTRACT(year_month from d.date_of_birth)) as age,
  d.adoptability_status, d.surrender_date
  FROM Dog AS d
  LEFT JOIN(
  SELECT dog_ID, GROUP_CONCAT(breed_name ORDER BY breed_name ASC SEPARATOR "/") AS breed_name
  FROM DogBreed
  GROUP BY dog_ID) AS b
  ON d.dog_ID = b.dog_ID
  WHERE d.adoptability_status != "Adopted"
  ORDER BY d.surrender_date;

 

-- view for expense report
CREATE OR REPLACE VIEW ExpenseAnalysisReportView AS 
  SELECT vendor_name, SUM(amount) AS total FROM Expense GROUP BY vendor_name ORDER BY total DESC;

 


-- TODO: views below are commented for now. Need to double check with Ali for tested report code, since the abstract code in delivered report doesn't reflect all the changes we made during testing

 

-- -- view for animal control report (split in three parts: surrender dog, adopted dog, expense, each part corresponds one column in the report)
CREATE OR REPLACE VIEW AnimalControlReportSurrenderDogsView AS
 SELECT COUNT(*) AS num_of_dogs, EXTRACT(YEAR_MONTH FROM surrender_date) AS year_month_sur 
 FROM Dog WHERE surrendered_by_animal_control = 1 AND PERIOD_DIFF(EXTRACT(YEAR_MONTH FROM CURDATE()), EXTRACT(YEAR_MONTH FROM surrender_date)) <=6 
 GROUP BY year_month_sur;

 

CREATE OR REPLACE VIEW AnimalControlReportExpenseAmountView AS 
  SELECT SUM(Expense.amount) AS expense_amount, EXTRACT(YEAR_MONTH FROM Expense.expense_date) AS year_month_exp
  FROM Expense INNER JOIN Dog ON Expense.dog_ID = Dog.dog_ID 
  WHERE Dog.adoptability_status = 'Adopted' AND Dog.surrendered_by_animal_control = 1 AND 
    PERIOD_DIFF(EXTRACT(YEAR_MONTH FROM CURDATE()),EXTRACT(YEAR_MONTH FROM Expense.expense_date)) <=6 
  GROUP BY year_month_exp;

 

CREATE OR REPLACE VIEW AnimalControlReportOver60DaysView AS 
  SELECT COUNT(*) AS num_of_adopted_dogs_over60days, EXTRACT(YEAR_MONTH FROM Adoption.adoption_date) AS year_month_ado 
  FROM Adoption INNER JOIN Dog ON Adoption.dog_ID = Dog.dog_ID
  WHERE Dog.surrendered_by_animal_control = 1 AND DATEDIFF(Adoption.adoption_date, Dog.surrender_date) >=60 
    AND PERIOD_DIFF(EXTRACT(YEAR_MONTH FROM CURDATE()), EXTRACT(YEAR_MONTH FROM Adoption.adoption_date)) <=6 
  GROUP BY year_month_ado;