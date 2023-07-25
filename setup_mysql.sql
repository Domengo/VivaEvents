-- MySQL server for the project
-- Create a database and a user for the project


CREATE USER IF NOT EXISTS 'eventU'@'localhost' IDENTIFIED BY 'pwd';
GRANT ALL PRIVILEGES ON `events_db`.* TO 'eventU'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'eventU'@'localhost';
FLUSH PRIVILEGES;
