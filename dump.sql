PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE users (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    username VARCHAR(50) NOT NULL, 
    email VARCHAR(100) NOT NULL, 
    password VARCHAR(255) NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (username), 
    UNIQUE (email)
);

INSERT INTO users (username, email, password) VALUES 
('tanvir.ahamed02', 'tanviralif00020@gmail.com', 'pbkdf2:sha256:600000$PFK2OukH9BYIbHUj$9eb6676bfef0af0181a6286a6982cd10a42c4ee13e13434904129a7e559a8aad');

CREATE TABLE blogposts (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    title VARCHAR(255) NOT NULL, 
    content TEXT NOT NULL, 
    author_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY (author_id) REFERENCES users (id)
);

COMMIT;

CREATE TABLE blogposts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    image_path VARCHAR(255),
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES users(id)
);


CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(200),
    phone_number VARCHAR(20),
    message VARCHAR(300)
);





CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    content TEXT NOT NULL,
    likes INT DEFAULT 0
);

CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    comment TEXT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);





