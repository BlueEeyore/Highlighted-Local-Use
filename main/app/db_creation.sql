DROP TABLE IF EXISTS Comment, Transcript, Lesson, UserClass, Class, `User`;

CREATE TABLE `User` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255),
    password VARCHAR(255),
    firstname VARCHAR(255),
    lastname VARCHAR(255),
    bio TEXT,
    school VARCHAR(255),
    pfp VARCHAR(255),
    notifications VARCHAR(50)
) ENGINE=InnoDB;

CREATE TABLE `Class` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    joincode VARCHAR(255),
    starttime VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE UserClass (
    uid INT,
    cid INT,
    role VARCHAR(50),
    PRIMARY KEY (uid, cid),
    FOREIGN KEY (uid) REFERENCES `User`(id),
    FOREIGN KEY (cid) REFERENCES `Class`(id)
) ENGINE=InnoDB;

CREATE TABLE `Lesson` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    creatorid INT,
    classid INT,
    name VARCHAR(255),
    videofn VARCHAR(255),
    creationtime VARCHAR(255),
    FOREIGN KEY (creatorid) REFERENCES `User`(id),
    FOREIGN KEY (classid) REFERENCES `Class`(id)
) ENGINE=InnoDB;

CREATE TABLE Transcript (
    lid INT,
    timestamp VARCHAR(255),
    text TEXT,
    FOREIGN KEY (lid) REFERENCES `Lesson`(id)
) ENGINE=InnoDB;

CREATE TABLE Comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uid INT,
    lid INT,
    parentid INT NULL,
    content TEXT,
    uploadtime TIMESTAMP,
    anonymous BOOLEAN,
    private BOOLEAN,
    comtype VARCHAR(50),
    tsrange TEXT,
    ts_offset INT,
    length INT,
    FOREIGN KEY (uid) REFERENCES `User`(id),
    FOREIGN KEY (lid) REFERENCES `Lesson`(id),
    FOREIGN KEY (parentid) REFERENCES Comment(id)
) ENGINE=InnoDB;
