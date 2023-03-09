-- create databases
CREATE DATABASE IF NOT EXISTS db;
CREATE DATABASE IF NOT EXISTS test;

-- create root user and grant rights
-- CREATE USER 'root'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL ON *.* TO 'root'@'localhost';
