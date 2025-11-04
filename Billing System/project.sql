CREATE DATABASE billing_system;
USE billing_system;

CREATE TABLE bills (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    date_time DATETIME,
    items TEXT,
    total_amount FLOAT
);