-- Create a new database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create a user 'hbnb_dev' if it doesn't exist, identified by 'hbnb_dev_pwd'
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privileges on the 'hbnb_dev_db' to the user 'hbnb_dev' when connecting from 'localhost'
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Grant the SELECT privilege on performance_schema to the user 'hbnb_dev' when connecting from 'localhost'
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Flush privileges to apply the changes
FLUSH PRIVILEGES;
