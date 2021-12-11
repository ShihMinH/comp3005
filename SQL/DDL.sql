create table publisher
	(id		int		NOT NULL AUTO_INCREMENT, 
	 name		varchar(255), 
     address		varchar(255),
     phone		varchar(255),
     email		varchar(255),
	 banking_account    varchar(255),
	 primary key (id)
	);

create table author
	(id		int		NOT NULL AUTO_INCREMENT, 
	 name		varchar(255), 
     address		varchar(255),
	 primary key (id)
	);

create table book
	(isbn		varchar(255),
	 name		varchar(255),
	 publisher_id		int,
     author_id		int,
     genre		varchar(255),
     pages		int,
     price		numeric(19,0),
     cost		numeric(19,0),
     percentage		varchar(10),
     count		int,
	 primary key (isbn),
     foreign key (publisher_id) references publisher(id)
		on delete cascade,
	 foreign key (author_id) references author(id)
		on delete set null
	);

create table customer
	(id		int		NOT NULL AUTO_INCREMENT, 
	 name		varchar(255), 
     phone		varchar(255),
     email		varchar(255),
	 banking_account    varchar(255),
     billing_address    varchar(255),
     shipping_address   varchar(255),
	 primary key (id)
	);

create table basket
	(id		int		NOT NULL AUTO_INCREMENT,
     customer_id        int,
     place_date		datetime,
     close_date		datetime,
     shipping_address   varchar(255),
     delivery_status    varchar(255),
     total_payment      numeric(19,0),
	 primary key (id),
	 foreign key (customer_id) references customer(id)
		on delete set null
	);

create table basket_book
	(basket_id			int, 
	 isbn		varchar(255),
	 count      int,
	 primary key (basket_id, isbn),
	 foreign key (basket_id) references basket(id)
		on delete cascade,
	 foreign key (isbn) references book(isbn)
		on delete cascade
	);