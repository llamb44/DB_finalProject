
CREATE TABLE Authors
(
	name VARCHAR(250) PRIMARY KEY,
	yearOfDeath INTEGER
);

CREATE TABLE Publishers
(
	name VARCHAR(250) PRIMARY KEY,
	stillAround VARCHAR(4)
);

CREATE TABLE Books
(
	authorName VARCHAR(250) NOT NULL,
	title VARCHAR(250) PRIMARY KEY,
	averageRating FLOAT DEFAULT NULL,
	link VARCHAR(500) UNIQUE NOT NULL,
	FOREIGN KEY (authorName) REFERENCES Authors (name)
);



CREATE TABLE Readers
(
	username VARCHAR(250) PRIMARY KEY,
	password VARCHAR(250) NOT NULL,
	favoriteBookTitle VARCHAR(250) DEFAULT NULL,
	favoriteBookAuthor VARCHAR(250) DEFAULT NULL,
	favoriteAuthor VARCHAR(250) DEFAULT NULL,
	FOREIGN KEY (favoriteAuthor) REFERENCES Authors (name),
	FOREIGN KEY (favoriteBookTitle) REFERENCES Books(title),
	FOREIGN KEY (favoriteBookAuthor) REFERENCES Authors(name)
);


CREATE TABLE Reading
(
	username VARCHAR(250),
	authorName VARCHAR(250),
	title VARCHAR(250),
	FOREIGN KEY (username) REFERENCES Readers(username)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (authorName) REFERENCES Authors(name),
	FOREIGN KEY (title) REFERENCES Books(title)
);
DROP TABLE Reading;

CREATE TABLE Rate
(
	username VARCHAR(250),
	authorName VARCHAR(250),
	title VARCHAR(250),
	rating FLOAT,
	FOREIGN KEY (username) REFERENCES Readers(username)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (authorName) REFERENCES Authors(name),
	FOREIGN KEY (title) REFERENCES Books(title)
);

ALTER TABLE rate DROP CONSTRAINT rate_ibfk_1;

ALTER TABLE rate ADD CONSTRAINT rate_ibfk_1
FOREIGN KEY (username) REFERENCES Readers(username)
		ON DELETE CASCADE
		ON UPDATE CASCADE;

CREATE TABLE Publishes
(
	authorName VARCHAR(250),
	title VARCHAR(250),
	publisherName VARCHAR(250),
	yearOfPublication INTEGER,
	location VARCHAR(200),
	FOREIGN KEY (authorName) REFERENCES Authors(name),
	FOREIGN KEY (title) REFERENCES Books(title),
	FOREIGN KEY (publisherName) REFERENCES Publishers(name)
);

delimiter //
CREATE TRIGGER nullVals1
BEFORE UPDATE on readers
FOR EACH ROW
BEGIN
	IF NEW.favoriteAuthor= "None" THEN
		SET NEW.favoriteAuthor= NULL;
	END IF;
END//

CREATE TRIGGER nullVals2
BEFORE UPDATE on readers
FOR EACH ROW
BEGIN
	IF NEW.favoriteBookAuthor= "None" THEN
			SET NEW.favoriteBookAuthor= NULL;
	END IF;
END//


CREATE TRIGGER nullVals3
BEFORE UPDATE on readers
FOR EACH ROW
BEGIN	
	IF NEW.favoriteBookTitle= "None" THEN
		SET NEW.favoriteBookTitle= NULL;
	END IF;
END//
delimiter ;

/* CREATE TRIGGER rating1
AFTER INSERT on rate
FOR EACH ROW 
BEGIN
	
	
	 INSERT INTO books(averageRating) 
		(SELECT val
		FROM
				(SELECT books.authorName, books.title, AVG(rating) as val 
				FROM books 
				INNER JOIN Rate on rate.title= books.title AND rate.authorName= books.authorName 
				GROUP BY books.authorName, books.title) AS temp, NEW
		WHERE NEW.authorName= temp.authorName AND NEW.title= temp.title);
		
	UPDATE  books SET averageRating = 
		SELECT temp.val 
		FROM 
			(SELECT books.authorName, books.title, AVG(rating) as val 
				FROM books 
				INNER JOIN Rate on rate.title= books.title AND rate.authorName= books.authorName 
				GROUP BY books.authorName, books.title) AS temp  
		WHERE NEW.authorName= temp.authorName AND NEW.title= temp.title;
END; */

ALTER TABLE Books
DROP COLUMN averageRating;


delimiter //
CREATE TRIGGER nullVals4
BEFORE INSERT on readers
FOR EACH ROW
BEGIN
	IF NEW.favoriteAuthor= "None" THEN
		SET NEW.favoriteAuthor= NULL;
	END IF;
END//

CREATE TRIGGER nullVals5
BEFORE INSERT on readers
FOR EACH ROW
BEGIN
	IF NEW.favoriteBookAuthor= "None" THEN
			SET NEW.favoriteBookAuthor= NULL;
	END IF;
END//


CREATE TRIGGER nullVals6
BEFORE INSERT on readers
FOR EACH ROW
BEGIN	
	IF NEW.favoriteBookTitle= "None" THEN
		SET NEW.favoriteBookTitle= NULL;
	END IF;
END//
delimiter ;

ALTER TABLE authors ADD COLUMN yearOfBirth INTEGER;


INSERT INTO authors VALUES("Charles Dickens", 1812, 1870);

ALTER TABLE Publishers MODIFY COLUMN stillAround VARCHAR(4);

