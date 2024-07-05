-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS BioMrcDB;

CREATE USER IF NOT EXISTS 'BioMrc' @'localhost' IDENTIFIED BY 'BioMrc2024';

GRANT ALL PRIVILEGES ON `BioMrcDB`.* TO 'BioMrc' @'localhost';

FLUSH PRIVILEGES;
