CREATE DATABASE qoehelp;
USE qoehelp;

CREATE TABLE HOURS (
ID INT NOT NULL auto_increment primary key,
PLANO VARCHAR(10) NOT NULL,
constraint UH_PLANO unique(PLANO)
);

CREATE TABLE QOE (
ID INT NOT NULL auto_increment primary key,
PLANO VARCHAR(10) NOT NULL,
constraint UQ_PLANO unique(PLANO)
);

CREATE TABLE REGISTRO (
ID INT NOT NULL auto_increment primary key,
PLANO_ID INT NOT NULL,
CONSTRAINT FK_PLANO FOREIGN KEY (PLANO_ID) REFERENCES HOURS(ID),
ESTADO VARCHAR(10) NOT NULL,
SOLUCION VARCHAR(60) NOT NULL
);

#######################################################################

#ALTER TABLE HOURS
#DROP COLUMN `09/11/2021`;

#SELECT * FROM QOE;
#SELECT * FROM HOURS;

#SELECT IF ( EXISTS(
#SELECT * FROM information_schema.COLUMNS 
#WHERE TABLE_SCHEMA = 'qoehelp' AND TABLE_NAME = 'hours' 
#AND COLUMN_NAME = '09/11/2021'
#),1,0);

#SELECT `'08/11/2021'`, PLANO FROM HOURS WHERE PLANO = "LMLO069";
#SELECT HOST, USER, PLUGIN FROM MYSQL.USER;