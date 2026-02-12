CREATE DATABASE bank_db;
USE bank_db;

CREATE TABLE accounts (
    account_no INT PRIMARY KEY,
    name VARCHAR(50),
    phone VARCHAR(15),
    balance INT,
    pin INT
);

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_no INT,
    type VARCHAR(10),
    amount INT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
