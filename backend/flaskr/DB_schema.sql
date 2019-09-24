DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS lecturer;
DROP TABLE IF EXISTS module;
DROP TABLE IF EXISTS lecturer_module;
DROP TABLE IF EXISTS student_module;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS markAttendance;

CREATE TABLE student (
    studentNumber TEXT UNIQUE PRIMARY KEY,
    surname TEXT NOT NULL,
    initials TEXT NOT NULL,
    programme TEXT NOT NULL,
    password TEXT NULL
);

CREATE TABLE lecturer (
    lecturerId TEXT UNIQUE NOT NULL PRIMARY KEY,
    surname TEXT NOT NULL,
    initials TEXT NOT NULL,
    password TEXT NULL
);

CREATE TABLE module (
    moduleCode TEXT UNIQUE NOT NULL PRIMARY KEY,
    moduleName TEXT NOT NULL
);

CREATE TABLE lecturer_module (    
    lmId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    lecturerId TEXT NOT NULL,
    moduleCode TEXT NOT NULL,
    FOREIGN KEY (lecturerId) REFERENCES lecturer (lecturerId),
    FOREIGN KEY (moduleCode) REFERENCES module (moduleCode)
);

CREATE TABLE student_module (
    studentNumber TEXT NOT NULL,
    moduleCode TEXT NOT NULL,
    FOREIGN KEY (studentNumber) REFERENCES student (studentNumber),
    FOREIGN KEY (moduleCode) REFERENCES module (moduleCode)
);

CREATE TABLE attendance (
    attendanceId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    attendanceDate DATETIME NOT NULL,
    lecturerId TEXT NOT NULL,
    moduleCode TEXT NOT NULL,
    isOpen BOOLEAN NOT NULL,
    FOREIGN KEY (lecturerId) REFERENCES lecturer (lecturerId),
    FOREIGN KEY (moduleCode) REFERENCES module (moduleCode)
);

CREATE TABLE markAttendance (
     attendanceId INTEGER NOT NULL,
     studentNumber TEXT NOT NULL,
     present BOOLEAN NOT NULL,
     FOREIGN KEY (studentNumber) REFERENCES student (studentNumber),
     FOREIGN key (attendanceId) REFERENCES attendance (attendanceId)
);