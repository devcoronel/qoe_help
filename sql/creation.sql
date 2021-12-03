CREATE DATABASE qoehelp;
USE qoehelp;

CREATE TABLE NODES (
ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
PLANO VARCHAR(10) NOT NULL
);

CREATE TABLE STATUS_NODE (
ID_NODE INT NOT NULL,
DEPENDENCIA ENUM('CALIDAD', 'OYM', 'CICSA', 'COTENER', 'IMPEDIMENTO'),
IMPEDIMENTO ENUM('C. COMERCIAL','MERCADO','MÓDULOS','EDIFICIO','PROVINCIA','SEDE CLARO','ZONA RIESGOZA','NINGUNO'),
REVISION DATE,
TIPO ENUM('US','DS','T3'),
PROBLEMA ENUM('RUIDO','MÓDULO RF AVERIADO','RUIDO NOCHE','RUIDO INTERMITENTE','CMs AFECTADOS','AVERIA','PERFORMANCE'),
ESTADO ENUM('POR AGENDAR','ATENDIDO - SOLUCIONADO','ATENDIDO - NO TERMINADO'),
DETALLE VARCHAR(300),
CONSTRAINT FK_ID_NODE_STATUS FOREIGN KEY (ID_NODE) REFERENCES NODES (ID)
);

CREATE TABLE NEW_HOURS (
ID_NODE INT NOT NULL,
CONSTRAINT FK_ID_NODE_HOURS FOREIGN KEY (ID_NODE) REFERENCES NODES (ID)
);

CREATE TABLE NEW_QOE (
ID_NODE INT NOT NULL,
CONSTRAINT FK_ID_NODE_QOE FOREIGN KEY (ID_NODE) REFERENCES NODES (ID)
);

CREATE TABLE AFECTED_DAYS (
ID_NODE INT NOT NULL,
CONSTRAINT FK_ID_NODE_AFECTED FOREIGN KEY (ID_NODE) REFERENCES NODES (ID)
);

CREATE TABLE PERIOD (
ID_NODE INT NOT NULL,
CONSTRAINT FK_ID_NODE_PERIOD FOREIGN KEY (ID_NODE) REFERENCES NODES (ID)
);

CREATE TABLE MODULATION (
ID_NODE INT NOT NULL,
CONSTRAINT FK_ID_NODE_MOD FOREIGN KEY (ID_NODE) REFERENCES NODES (ID)
);

SELECT (SELECT ID FROM NODES WHERE PLANO = 'LMJL155'), ID_NODE FROM NEW_QOE;
SELECT ID FROM NODES WHERE PLANO = 'LMJL155';

ALTER TABLE NEW_QOE
ADD COLUMN `20/11/2021` FLOAT AFTER ID_NODE;

INSERT INTO NEW_QOE (ID_NODE, `20/11/2021`)
VALUES ((SELECT ID FROM NODES WHERE PLANO = 'LMJL155'), 98 );

SELECT `20/11/2021` FROM NEW_QOE
WHERE ID_NODE = (SELECT ID FROM NODES WHERE PLANO = 'LMJL155');
#######################################################################
DROP TABLE NEW_QOE;
DROP TABLE NEW_HOURS;
DROP TABLE STATUS_NODE;
DROP TABLE PERIOD;
DROP TABLE AFECTED_DAYS;
DROP TABLE MODULATION;

ALTER TABLE NEW_QOE
DROP COLUMN `16/11/2021`;
ALTER TABLE NEW_HOURS
DROP COLUMN `16/11/2021`;
ALTER TABLE PERIOD
DROP COLUMN `16/11/2021`;
ALTER TABLE AFECTED_DAYS
DROP COLUMN `16/11/2021`;
ALTER TABLE MODULATION
DROP COLUMN `19/11/2021`;

SELECT * FROM NEW_QOE;
SELECT * FROM NEW_HOURS;
SELECT * FROM PERIOD;
SELECT * FROM AFECTED_DAYS;
SELECT * FROM STATUS_NODE;
SELECT * FROM NODES WHERE PLANO = 'LMIN019';
SELECT * FROM MODULATION;

#SELECT IF ( EXISTS(
#SELECT * FROM information_schema.COLUMNS 
#WHERE TABLE_SCHEMA = 'qoehelp' AND TABLE_NAME = 'hours' 
#AND COLUMN_NAME = '09/11/2021'
#),1,0);

#SELECT `'08/11/2021'`, PLANO FROM HOURS WHERE PLANO = "LMLO069";
#SELECT HOST, USER, PLUGIN FROM MYSQL.USER;

#
#drop database qoehelp;