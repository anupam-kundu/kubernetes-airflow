mysql -u root

CREATE DATABASE airflow;

CREATE USER 'airflow'@'%' IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES ON airflow.* TO 'airflow'@'%';

FLUSH PRIVILEGES;
