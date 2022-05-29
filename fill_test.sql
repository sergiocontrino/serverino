CREATE TABLE book (
        book_id SERIAL NOT NULL,
        title VARCHAR(255) NOT NULL,
        year INTEGER,
        author VARCHAR(255),
        PRIMARY KEY (book_id)
)

CREATE TABLE reader (
        reader_id SERIAL NOT NULL,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        address VARCHAR(255) NOT NULL,
        PRIMARY KEY (reader_id)
)

CREATE TABLE loan (
        loan_id SERIAL NOT NULL,
        book_id integer,
        reader_id integer,
        PRIMARY KEY (loan_id),
        UNIQUE (book_id),
        FOREIGN KEY(book_id) REFERENCES book (book_id) ON DELETE CASCADE,
        FOREIGN KEY(reader_id) REFERENCES reader (reader_id)        
)

insert into book (title, year,author) values 
('Red', 1999, 'mann'),
('Blue', 2000, 'svevo'),
('Green', 2020, 'proust'),
('Orange', 2021, 'orwell'),
('Yellow', 2021, 'potter')
;

insert into reader (name, surname, address)  values 
('jim', 'one', 'paris'),
('helen', 'two', 'london'),
('karen', 'tree', 'berlin')
;

insert into loan (book_id, reader_id)  values 
(1,1), (2,2), (3,2), (4,3), (5,2);
