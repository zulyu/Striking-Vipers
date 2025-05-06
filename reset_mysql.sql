ALTER USER 'root'@'localhost' IDENTIFIED BY 'CPSC498';
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS StrikingVipers;
USE StrikingVipers;
CREATE TABLE IF NOT EXISTS Teachers (
    TeacherID INT AUTO_INCREMENT PRIMARY KEY,
    TeacherFirstName VARCHAR(255) NOT NULL,
    TeacherLastName VARCHAR(255) NOT NULL,
    TeacherUserName VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS Classes (
    ClassCode VARCHAR(255) PRIMARY KEY,
    ClassGrade INT NOT NULL,
    TeacherID INT NOT NULL,
    FOREIGN KEY (TeacherID) REFERENCES Teachers(TeacherID)
);
CREATE TABLE IF NOT EXISTS Students (
    StudentID INT AUTO_INCREMENT PRIMARY KEY,
    StudentFirstName VARCHAR(255) NOT NULL,
    StudentLastName VARCHAR(255) NOT NULL,
    StudentUserName VARCHAR(255) NOT NULL UNIQUE,
    ClassCode VARCHAR(255) NOT NULL,
    FOREIGN KEY (ClassCode) REFERENCES Classes(ClassCode)
);
INSERT IGNORE INTO Teachers (TeacherFirstName, TeacherLastName, TeacherUserName)
VALUES ('John', 'Doe', 'jdoe');
INSERT IGNORE INTO Classes (ClassCode, ClassGrade, TeacherID)
VALUES ('CS101', 10, 1);
INSERT IGNORE INTO Students (StudentFirstName, StudentLastName, StudentUserName, ClassCode)
VALUES ('Jane', 'Smith', 'jsmith', 'CS101'); 