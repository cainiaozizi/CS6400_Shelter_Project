USE cs6400_su20_team07_final;

-- Additional Original data transform	
    alter table Orig_Applications
		ADD application_state INT AS (
			CASE
				WHEN is_rejected = 0 AND is_approved = 0 THEN 0
                ELSE 1
			END );
            
alter table Orig_Dog
	ADD DOB DATE AS (
    DATE_ADD(surrender_date, INTERVAL -age_months MONTH )
    );
    
CREATE VIEW dashboardView AS
  SELECT d.dog_name, b.breed_name, d.sex, d.alteration_status, (CURDATE() - d.date_of_birth) as age,
  d.adoptability_status, d.surrender_date
  FROM Dog AS d
  LEFT JOIN(
  SELECT dog_ID, GROUP_CONCAT(breed_name) AS breed_name
  FROM DogBreed
  GROUP BY dog_ID) AS b
  ON d.dog_ID = b.dog_ID
  WHERE d.adoptability_status != "Adopted"
  ORDER BY d.surrender_date;



INSERT INTO User (email_address,first_name,last_name,phone_number,password,start_date) SELECT email,u_f_name,u_l_name,phone,password,start_date FROM Orig_Users;
INSERT INTO Mo (email_address) SELECT email FROM Orig_Users WHERE Volunteer = 0;

INSERT INTO Applicant(last_name, first_name, street, city, state, zip_code, phone_number, email_address)
	SELECT DISTINCT a_l_name,a_f_name, a_street_addr, a_city, a_state, a_postal_code, a_phone,a_email FROM Orig_Applications;

INSERT INTO AdoptionApplication(application_ID, email_address, application_date, coapplicant_last_name, coapplicant_first_name, application_state)
	SELECT app_num,a_email, app_date, coapp_l_name, coapp_f_name, application_state FROM Orig_Applications;

INSERT INTO ApprovedApplication(application_ID) 
	SELECT app_num FROM Orig_Applications WHERE is_approved = 1;
    
INSERT INTO ApprovedApplication(application_ID) 
	SELECT app_num FROM Orig_Applications WHERE is_rejected = 1;

INSERT INTO Dog(dog_ID, surrender_reason, surrender_date , surrendered_by_animal_control, microchip_ID, dog_name, date_of_birth, sex , alteration_status, adoptability_status, description, email_address)
	SELECT DISTINCT dog_id, surrender_reason, surrender_date, animal_control, microchip, dog_name, DOB, sex, alt_status, 'Available', description, email FROM Orig_Dog;

INSERT INTO Breed(breed_name)
	SELECT DISTINCT breed_name FROM Orig_Dog;

INSERT INTO DogBreed(dog_ID,breed_name)
	SELECT dog_id, breed_name FROM Orig_Dog;

INSERT INTO Vendor(vendor_name)
	SELECT DISTINCT vendor_name FROM Orig_Expenses;

INSERT INTO Expense(dog_ID, vendor_name, expense_date, amount, description)
	SELECT dog_id, vendor_name, date_expense, amount_expense, description FROM Orig_Expenses;
	
INSERT INTO Adoption(application_ID, dog_ID, adoption_date, adoption_fee)
	SELECT app_num, dog_id, adoption_date,0 FROM Orig_Adoption;


CREATE VIEW feeView AS
	SELECT CASE 
		WHEN surrendered_by_animal_control = 1 THEN adoption_expense * 0.15 
        WHEN surrendered_by_animal_control = 0 THEN adoption_expense *1.15 
        END AS adoption_fee, fee.dog_ID, fee.surrendered_by_animal_control 
    FROM (SELECT SUM(EXP.amount) AS adoption_expense, EXP.dog_ID , DG.surrendered_by_animal_control 
    FROM Expense AS EXP 
    INNER JOIN Dog AS DG ON DG.dog_ID = EXP.dog_ID
    GROUP BY DG.dog_ID) AS fee;


UPDATE Adoption INNER JOIN feeView ON Adoption.dog_ID = feeView.dog_ID
	SET Adoption.adoption_fee = feeView.adoption_fee;

DROP VIEW feeView;

UPDATE Dog SET adoptability_status = 'Available'
	WHERE (alteration_status =1 AND microchip_ID IS NOT NULL AND dog_ID <> 0);
    
UPDATE Dog SET adoptability_status = 'Not Available'
	WHERE (alteration_status =0 OR microchip_ID IS NULL) AND dog_ID <> 0;

CREATE VIEW AdoptedDogs AS 
	SELECT DISTINCT dog_ID, 'Adopted' AS adoptability_status
    FROM Adoption;

UPDATE Dog INNER JOIN AdoptedDogs ON Dog.dog_ID = AdoptedDogs.dog_ID
SET Dog.adoptability_status = AdoptedDogs.adoptability_status;

drop view AdoptedDogs;

drop table Orig_Dog;
drop table Orig_Adoption;
drop table Orig_Applications;
drop table Orig_Expenses;
drop table Orig_Users;
