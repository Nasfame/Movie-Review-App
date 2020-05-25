create database movie;
use movie;
CREATE TABLE user (
    id INT AUTO_INCREMENT NOT NULL,
    PRIMARY KEY (id),
    name VARCHAR(250) UNIQUE
);
CREATE TABLE category (
    id INT AUTO_INCREMENT NOT NULL,
    PRIMARY KEY (id),
    name VARCHAR(250) UNIQUE
);
CREATE TABLE movie (
    id INT AUTO_INCREMENT NOT NULL,
    PRIMARY KEY (id),
    name VARCHAR(250) UNIQUE,
    user_id INT,
    FOREIGN KEY (user_id)
        REFERENCES user (id),
    category_id INT,
    FOREIGN KEY (category_id)
        REFERENCES category (id)
);
CREATE TABLE review (
    id INT AUTO_INCREMENT NOT NULL,
    PRIMARY KEY (id),
    name VARCHAR(250),
    user_id INT,
    FOREIGN KEY (user_id)
        REFERENCES user (id),
    movie_id INT,
    FOREIGN KEY (movie_id)
        REFERENCES movie (id)
);
desc review;
/*drop database movie;

