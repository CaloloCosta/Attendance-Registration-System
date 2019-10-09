-- DROP TABLE IF EXISTS student;
-- DROP TABLE IF EXISTS lecturer;
-- DROP TABLE IF EXISTS attendance;
-- DROP TABLE IF EXISTS markAttendance;
-- DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);



CREATE TABLE student (
    studentNumber TEXT UNIQUE PRIMARY KEY,
    surname TEXT NOT NULL,
    initials TEXT NOT NULL,
    programme TEXT NOT NULL,
    mode_of_study TEXT NOT NULL,
    password TEXT NULL
);

CREATE TABLE lecturer (
    lecturerId TEXT UNIQUE NOT NULL PRIMARY KEY,
    surname TEXT NOT NULL,
    initials TEXT NOT NULL,
    password TEXT NULL
);



CREATE TABLE attendance (
    attendanceId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    attendanceDate TEXT NOT NULL,
    isOpen BOOLEAN NOT NULL,
    mode_of_study TEXT NOT NULL
);

CREATE TABLE markAttendance (
     attendanceId INTEGER NOT NULL,
     studentNumber TEXT NOT NULL,
     present BOOLEAN NOT NULL,
     FOREIGN KEY (studentNumber) REFERENCES student (studentNumber),
     FOREIGN key (attendanceId) REFERENCES attendance (attendanceId)
);