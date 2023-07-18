-- MySQL server for the project
-- Create a database and a user for the project


CREATE USER IF NOT EXISTS 'eventU'@'localhost' IDENTIFIED BY 'pwd';
GRANT ALL PRIVILEGES ON `events_db`.* TO 'eventU'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'eventU'@'localhost';
FLUSH PRIVILEGES;

In MySQL, a replica is a copy of the data from a primary server (also known as the master) to another server (also known as the slave). Replication in MySQL is a process that allows you to create one or more copies of your database and keep them in sync with each other. It is commonly used for data redundancy, load balancing, and creating backups.

MySQL replication works in a master-slave architecture, where one server acts as the master, and one or more servers act as slaves. The master server continuously records changes to its data in binary log files. The slave server(s) read these binary log files and apply the changes to their own data, making them consistent with the master.

To set up MySQL replication, you need to perform the following steps:

Configure the Master Server:

Enable binary logging on the master server by adding the following line to your MySQL configuration file (typically my.cnf or my.ini):
-- log_bin = /path/to/binary_log_file
Restart the MySQL service after making this change.
Create a Replication User on the Master Server:

Connect to the MySQL server as a privileged user.
Create a new user and grant replication privileges to it:
-- CREATE USER 'replication_user'@'slave_ip_address' IDENTIFIED BY 'password';
-- GRANT REPLICATION SLAVE ON *.* TO 'replication_user'@'slave_ip_address';
-- FLUSH PRIVILEGES;
Replace replication_user with the name of the replication user, and slave_ip_address with the IP address of the slave server.
Note: If you want to allow the slave server to connect from any IP address, you can use the wildcard % instead of the slave IP address.
Obtain the Master's Binary Log Coordinates:

Show the master's binary log coordinates by executing the following on the master server:
-- SHOW MASTER STATUS;
Configure the Slave Server(s):

On each slave server, edit the MySQL configuration file and add the following lines:
-- server-id = unique_integer
-- relay-log = /path/to/relay_log_file
-- read-only = 1

Restart the MySQL service on each slave after making these changes.
Start Replication on the Slave Server(s):

On each slave, connect to the MySQL server and issue the following command:
-- CHANGE MASTER TO MASTER_HOST='master_ip_address', MASTER_USER='replication_user', MASTER_PASSWORD='password', MASTER_LOG_FILE='master_log_file', MASTER_LOG_POS=master_log_position;
Replace 'master_ip_address', 'replication_user', 'password', 'master_log_file', and 'master_log_position' with the corresponding values from the master's SHOW MASTER STATUS output.
Start the Slave(s):

On each slave, issue the following command to start replication:

-- START SLAVE;
Verify Replication:

Check the slave's status using:
-- SHOW SLAVE STATUS;
The Slave_IO_Running and Slave_SQL_Running columns should be Yes if replication is running successfully.

That's it! Now your MySQL replication is set up, and the slave(s) will automatically synchronize with the master as new data changes are made on the master.

--------------------------------------------------------------------------------

To set up MySQL replication with the primary on web-01 and the replica on web-02, follow these steps:

Step 1: Configure the MySQL Primary (web-01)

SSH into web-01 and open the MySQL configuration file for editing:
-- sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
Comment out the bind-address parameter by adding a # at the beginning of the line (this allows MySQL to listen on all interfaces):
Add the following lines to enable binary logging:
-- log_bin = /var/log/mysql/mysql-bin.log
-- binlog_do_db = tyrell_corp

Save and close the file.

Step 2: Restart MySQL on the Primary
Step 3: Configure the MySQL Replica (web-02)

SSH into web-02 and open the MySQL configuration file for editing:
-- sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
Comment out the bind-address parameter by adding a # at the beginning of the line (this allows MySQL to listen on all interfaces):
Add the following lines to enable replication:
-- server-id = 2
-- relay-log = /var/log/mysql/mysql-relay-bin.log
-- read-only = 1

Save and close the file.

Step 4: Restart MySQL on the Replica
Step 5: Set Up Replication on the Replica (web-02)

Connect to the MySQL server on web-02:
-- mysql -u root -p
Issue the following command to configure replication:
-- CHANGE MASTER TO MASTER_HOST='web-01', MASTER_USER='replication_user', MASTER_PASSWORD='your_replication_password', MASTER_LOG_FILE='mysql-bin.000001', MASTER_LOG_POS=107;

Note: Replace 'your_replication_password' with a strong password and adjust the MASTER_LOG_FILE and MASTER_LOG_POS values based on the output of SHOW MASTER STATUS; on the primary.
Start replication on the replica:
-- START SLAVE;
-- exit;

Step 6: Verify Replication

Connect to the MySQL server on web-01:
-- mysql -u root -p
Create a new database and table, and insert some data:
-- CREATE DATABASE tyrell_corp;
-- USE tyrell_corp;
-- CREATE TABLE employees (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50));
-- INSERT INTO employees (name) VALUES ('John Doe');

Verify that the data is being replicated to the replica (web-02):

a. Connect to the MySQL server on web-02:
-- mysql -u root -p

b. Check the data in the replica:
-- USE tyrell_corp;
-- SELECT * FROM employees;

You should see the data you inserted on web-01 in the replica's table.

That's it! MySQL replication is now set up with the primary on web-01 and the replica on web-02. Make sure that UFW or any firewall is allowing connections on port 3306 (default MySQL port) on both servers, as replication requires communication between them on this port.