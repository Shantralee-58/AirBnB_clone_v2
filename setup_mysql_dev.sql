-- Prepares MYSQL server for the project

-- Create database for development
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create a new user for development
CREATE USER
       IF NOT EXISTS 'hbnb_dev'@'localhost'
       IDENTIFIED BY 'hbnb_dev_pwd';

GRANT ALL ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT on performance_schema.* TO 'hbnb_dev'@'localhost'
