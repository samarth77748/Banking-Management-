CREATE DATABASE IF NOT EXISTS bankdb;
USE bankdb;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    balance DECIMAL(10,2) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    mobile VARCHAR(20),
    email VARCHAR(100),
    balance DECIMAL(10,2) DEFAULT 0
);

INSERT INTO users (username, password, balance)
VALUES ('admin', 'admin123', 10000);
