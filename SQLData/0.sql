-- STEP 2: create database. (setup for connection - connection character sets and collation. we can simply use default)
DROP DATABASE IF EXISTS cs6400_su20_team07_final;
-- SET default_storage_engine = InnoDB;
-- SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS cs6400_su20_team07_final;
    -- DEFAULT CHARACTER SET utf8mb4
    -- DEFAULT COLLATE utf8mb4_unicode_ci;
USE cs6400_su20_team07_final;

-- STEP 3: grant all privileges on this database to the USER
DROP USER IF EXISTS 'gatechUser'@'localhost';
CREATE USER 'gatechUser'@'localhost' IDENTIFIED BY '1234';
-- GRANT SELECT, INSERT, UPDATE, DELETE, FILE ON *.* TO 'gatechUser'@'localhost';
GRANT ALL PRIVILEGES ON `gatechuser`.* TO 'gatechUser'@'localhost';
GRANT ALL PRIVILEGES ON `cs6400_su20_team07_final`.* TO 'gatechUser'@'localhost';
FLUSH PRIVILEGES;

-- CREATE DATABASE IF NOT EXISTS cs6400_su20_team07_final;

-- USE cs6400_su20_team07_final;

-- Project Schema

CREATE TABLE User (
	id INTEGER unsigned NOT NULL AUTO_INCREMENT,
    email_address VARCHAR(36) NOT NULL,
    first_name VARCHAR(25) NOT NULL,
    last_name VARCHAR(40) NOT NULL,
    phone_number VARCHAR(12) NOT NULL,
    password VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    INDEX(id),
    PRIMARY KEY(email_address));
    
    CREATE TABLE Mo (
    email_address VARCHAR(36) NOT NULL,
    PRIMARY KEY(email_address),
    FOREIGN KEY (email_address) REFERENCES User (email_address));
    
CREATE TABLE Applicant (
  last_name VARCHAR(40) NOT NULL,
  first_name VARCHAR(25) NOT NULL,
  street VARCHAR(70) NOT NULL,
  city VARCHAR(30) NOT NULL,
  state VARCHAR(2) NOT NULL,
  zip_code VARCHAR(5) NOT NULL,
  phone_number VARCHAR(12) NOT NULL,
  email_address VARCHAR(36) NOT NULL,
  PRIMARY KEY (email_address));
  
  CREATE TABLE AdoptionApplication (
  application_ID INTEGER (6) unsigned NOT NULL AUTO_INCREMENT,
  email_address VARCHAR(36) NOT NULL,
  application_date DATE NOT NULL,
  coapplicant_last_name VARCHAR(40) NULL,
  coapplicant_first_name VARCHAR(40) NULL,
  application_state BOOLEAN NOT NULL,
  PRIMARY KEY (application_ID),
  FOREIGN KEY (email_address) REFERENCES Applicant (email_address));
  
 CREATE TABLE ApprovedApplication (
  application_ID INTEGER(6) unsigned NOT NULL,
  PRIMARY KEY (application_ID),
  FOREIGN KEY (application_ID) REFERENCES AdoptionApplication (application_ID));


CREATE TABLE RejectedApplication (
  application_ID INTEGER (6) unsigned NOT NULL,
  PRIMARY KEY (application_ID),
  FOREIGN KEY (application_ID) REFERENCES AdoptionApplication (application_ID)); 
  
CREATE TABLE Dog (
	dog_ID INTEGER unsigned NOT NULL AUTO_INCREMENT,
	surrender_reason VARCHAR(500) NOT NULL,
	surrender_date DATE NOT NULL,
	surrendered_by_animal_control BOOLEAN NOT NULL,
	microchip_ID VARCHAR (15),
	dog_name VARCHAR(25) NOT NULL,
	date_of_birth DATE NOT NULL,
	sex ENUM('Male', 'Female', 'Unknown') NOT NULL,
	alteration_status BOOLEAN NOT NULL,
	adoptability_status ENUM('Adopted', 'Available', 'Not Available') NOT NULL,
	description VARCHAR(500),
	email_address VARCHAR(36) NOT NULL,
	PRIMARY KEY (dog_ID),
	FOREIGN KEY (email_address) REFERENCES User (email_address));



CREATE TABLE Breed (
breed_name VARCHAR(50) NOT NULL,
PRIMARY KEY (breed_name));


CREATE TABLE DogBreed (
dog_ID INTEGER(4) unsigned NOT NULL,
breed_name VARCHAR(50) NOT NULL,
PRIMARY KEY (dog_ID, breed_name),
FOREIGN KEY (dog_ID) REFERENCES Dog (dog_ID),
FOREIGN KEY (breed_name) REFERENCES Breed (breed_name));


CREATE TABLE Vendor (
  vendor_name VARCHAR(100) NOT NULL,
  PRIMARY KEY (vendor_name));


CREATE TABLE Expense (
  dog_ID INTEGER(4) unsigned NOT NULL,
  vendor_name VARCHAR(100) NOT NULL,
  expense_date DATE NOT NULL,
  amount FLOAT(12) NOT NULL,
  description VARCHAR(500) NULL,
  PRIMARY KEY (dog_ID, vendor_name, expense_date),
  FOREIGN KEY (dog_ID) REFERENCES Dog (dog_ID),
  FOREIGN KEY (vendor_name) REFERENCES Vendor (vendor_name));
  
 CREATE TABLE Adoption (
     dog_ID INTEGER(4) unsigned NOT NULL,
     application_ID INTEGER(6) unsigned NOT NULL,
     adoption_date DATE NOT NULL,
     adoption_fee FLOAT NOT NULL,
     PRIMARY KEY(dog_ID, application_ID),
     FOREIGN KEY(dog_ID) REFERENCES Dog (dog_ID),
     FOREIGN KEY(application_ID) REFERENCES ApprovedApplication (application_ID));
     

  
  