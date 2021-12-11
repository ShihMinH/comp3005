select * from book;

select book.isbn, book.name, publisher.name, author.name, book.genre, book.price, book.pages from book 
left join author on book.author_id = author.id left join publisher on book.publisher_id = publisher.id;

select book.isbn, book.name, publisher.name, author.name, book.genre, book.price, book.pages 
    from book left join author on book.author_id = author.id left join publisher on book.publisher_id = publisher.id 
    where isbn = 'isbn-11111';

select book.isbn, book.name, publisher.name, author.name, book.genre, book.price, book.pages from book 
left join author on book.author_id = author.id left join publisher on book.publisher_id = publisher.id where book.name = 'DB2';

select book.isbn, book.name, publisher.name, author.name, book.genre, book.price, book.pages from book 
left join author on book.author_id = author.id left join publisher on book.publisher_id = publisher.id where author.name = 'DB2';

select book.isbn, book.name, publisher.name, author.name, book.genre, book.price, book.pages from book 
left join author on book.author_id = author.id left join publisher on book.publisher_id = publisher.id where publisher.name = 'DB2';

select book.isbn, book.name, publisher.name, author.name, book.genre, book.price, book.pages from book 
left join author on book.author_id = author.id left join publisher on book.publisher_id = publisher.id where book.genre = 'Computer';

select * from author where id = 1;

select * from author;

select * from publisher where id = 1;

select * from publisher;

select * from customer where id = 1;

select * from customer where email = 'oooms';

select * from basket where customer_id =1;

select * from basket where id = 1;

INSERT INTO customer (name, phone, email, billing_address, shipping_address, banking_account) VALUES ('name','123','email@address','billing','shipping','1234');

INSERT INTO basket (customer_id, shipping_address) VALUES ('1', 'shipping');

INSERT INTO basket_book VALUES('1','2','1');

INSERT INTO author (name, address) VALUES ('a', 'address');

INSERT INTO publisher (name, phone, email, address, banking_account) VALUES ('name','123','email@address','billing','1234');

select * from author where name = 'name' or address = 'address';

select * from publisher where name = 'name' or address = 'address';

INSERT INTO book (isbn, name, publisher_id, author_id, genre, pages, price, cost, percentage, count) VALUES ('isbn-11111', 'name', '1233', '1234', 'abcd', '12', '12', '11', '4', '2');

DELETE FROM book WHERE isbn = 'isbn-11111';

select * from basket_book where basket_id ='1';

UPDATE basket SET place_date = '2021-12-09', shipping_address = 'address', total_payment = '12' Where id = '1';

select SUM('12') from basket where place_date IS NOT NULL;

select SUM(cost * count + cost * count * percentage) from book ;

select sum(distinct b.total_payment), bo.genre from basket as b inner join basket_book as bb on b.id = bb.basket_id inner join book as bo on bb.isbn = bo.isbn group by bo.genre ;

select sum(distinct b.total_payment), a.name from basket as b inner join basket_book as bb on b.id = bb.basket_id inner join book as bo on bb.isbn = bo.isbn inner join author as a on bo.author_id = a.id group by bo.author_id;

select sum(distinct b.total_payment), p.name from basket as b inner join basket_book as bb on b.id = bb.basket_id inner join book as bo on bb.isbn = bo.isbn inner join publisher as p on bo.publisher_id = p.id group by p.id;
