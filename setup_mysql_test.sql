-- Create a new database 'hbnb_test_db' if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create a user 'hbnb_test' if it doesn't exist, identified by 'hbnb_test_pwd'
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on the 'hbnb_test_db' to the user 'hbnb_test' when connecting from 'localhost'
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant the SELECT privilege on performance_schema to the user 'hbnb_test' when connecting from 'localhost'
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Flush privileges to apply the changes
FLUSH PRIVILEGES;
