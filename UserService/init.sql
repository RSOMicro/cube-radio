CREATE USER 'auth_service'@'%' IDENTIFIED WITH mysql_native_password BY 'LivinOnLove';

CREATE DATABASE user_service;

GRANT ALL PRIVILEGES ON user_service.* TO 'auth_service'@'%';

USE user_service;

CREATE TABLE teenant (
    teenant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    size INT NOT NULL
);

CREATE TABLE users (
    user_id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(64) NOT NULL,
    name VARCHAR(30) NOT NULL,
    lastname VARCHAR(30) NOT NULL,
    company_id INT NULL,
    FOREIGN KEY (company_id) REFERENCES teenant(teenant_id)
);

INSERT INTO teenant (teenant_id, name, size) VALUES (1, 'DEFAULT_PUBLIC', '999');
INSERT INTO teenant (teenant_id, name, size) VALUES (2, 'ACME D.O.O ', 10);

INSERT INTO `users` (`user_id`, `email`, `name`, `lastname`, `company_id`) VALUES
('7ecb758c-1cdc-4580-8fab-7c2de78d3948', 'testni_uporabnik1@gmail.com', 'Janez', 'Novak', 1),
('bcf08366-39e9-4611-bc2d-18ddaefdec9b', 'testni_uporabnik2@gmail.com', 'Micka', 'Novak', 2);
