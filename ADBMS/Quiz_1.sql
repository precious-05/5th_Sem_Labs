CREATE DATABASE Bills;
USE Bills;
CREATE TABLE Electricity(
     cid INT PRIMARY KEY AUTO_INCREMENT,
     cname VARCHAR(30),
     qty DOUBLE,
     price DOUBLE
);
ALTER TABLE Electricity AUTO_INCREMENT=1001;
INSERT INTO Electricity(cname,qty,price) VALUES('C1',350,15);
INSERT INTO Electricity(cname,qty,price) VALUES('C2',250,20);
INSERT INTO Electricity(cname,qty,price) VALUES('C3',200,22);
INSERT INTO Electricity(cname,qty,price) VALUES('C4',400,25);
INSERT INTO Electricity(cname,qty,price) VALUES('C5',300,27);

SELECT cid,cname FROM Electricity WHERE qty<400 AND qty>=200; 

ALTER TABLE Electricity ADD bill INT;
UPDATE Electricity SET bill=qty*price;
SELECT * FROM Electricity;


SELECT cid,cname,bill FROM Electricity WHERE bill>50
ORDER BY qty DESC; 