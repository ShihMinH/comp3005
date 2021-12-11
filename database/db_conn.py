import mysql.connector
from datetime import datetime

def connection():

    config = {
        "user": "root",
        "password": "12345678",
        "host": "localhost",
        "port": 3306,
        "database": "book_store"
    }
    try:
        c = mysql.connector.connect(**config)
        return c
    except:
        print ("connection error")
        exit(1)

def get_books(): 
    cn = connection()
    cur = cn.cursor()
    cur.execute("select book.isbn, book.name, publisher.name, author.name, book.genre, book.price, book.pages from book left join author on book.author_id = author.id left join publisher on book.publisher_id = publisher.id")
    return (cur.fetchall())

def get_books_by_owner(): 
    cn = connection()
    cur = cn.cursor()
    cur.execute("select * from book ")
    return (cur.fetchall())

def get_book(isbn): 
    cn = connection()
    cur = cn.cursor()
    cur.execute("select book.isbn, book.name, publisher.name, author.name, book.genre, book.price, book.pages \
    from book left join author on book.author_id = author.id left join publisher on book.publisher_id = publisher.id \
    where isbn = %s", (isbn,))
    
    return (cur.fetchone())

def get_books_by(isbn=None, name=None, author=None,genre=None, publisher=None): 
    cn = connection()
    cur = cn.cursor()
    if isbn:
        get_book(isbn)
        
    elif name:
        cur.execute("select book.isbn, book.name, publisher.name, author.name, book.genre, book.price, book.pages from book left join author on book.author_id = author.id left join publisher on book.publisher_id = publisher.id where name = %s", (name,))
    elif author:
        cur.execute("select book.isbn, book.name, publisher.name, author.name, book.genre, book.price, book.pages from book left join author on book.author_id = author.id left join publisher on book.publisher_id = publisher.id \
        where author.name = %s", (author,))
    elif genre:
        cur.execute("select book.isbn, book.name, publisher.name, author.name, book.genre, book.price, book.pages from book left join author on book.author_id = author.id left join publisher on book.publisher_id = publisher.id where genre = %s", (genre,))
    elif publisher:
        cur.execute("select book.isbn, book.name, publisher.name, author.name, book.genre, book.price, book.pages from book left join author on book.author_id = author.id left join publisher on book.publisher_id = publisher.id \
        where publisher.name = %s", (publisher,))
   
    # for x in cur.fetchall():
    #     print(x)
    return (cur.fetchall())


def get_author(id):
    cn = connection()
    cur = cn.cursor()
    cur.execute("select * from author where id = %s", (id,))
    return (cur.fetchone())

def get_authors():
    cn = connection()
    cur = cn.cursor()
    cur.execute("select * from author")
    return (cur.fetchall())

def get_publisher(id):
    cn = connection()
    cur = cn.cursor()
    cur.execute("select * from publisher where id = %s", (id,))
    return (cur.fetchone())

def get_publishers():
    cn = connection()
    cur = cn.cursor()
    cur.execute("select * from publisher")
    return (cur.fetchall())

def get_customer(id):
    cn = connection()
    cur = cn.cursor()
    cur.execute("select * from customer where id = %s", (id,))
    return (cur.fetchone())


def get_customer_by_email(email):
    cn = connection()
    cur = cn.cursor()
    cur.execute("select * from customer where email = %s", (email,))
    return (cur.fetchone())

def get_baskets_by_customer_id(customer_id):
    cn = connection()
    cur = cn.cursor()
    cur.execute("select * from basket where customer_id = %s", ((customer_id),))
    return (cur.fetchall())  

def get_basket(id):
    cn = connection()
    cur = cn.cursor()
    cur.execute("select * from basket where id = %s", (id,))
    return (cur.fetchone())           

def add_customer(name, phone, email, billing_address, shipping_address, banking_account):
    cn = connection()
    cur = cn.cursor()
    val = (name, phone, email, billing_address, shipping_address, banking_account)
    cur.execute("INSERT INTO customer (name, phone, email, billing_address, shipping_address, banking_account) VALUES\
         (%s, %s, %s, %s, %s, %s)", val)
    cn.commit()
    print('New Customer created')

def add_basket(customer_id, shipping_address):
    cn = connection()
    cur = cn.cursor()
    cur.execute("INSERT INTO basket (customer_id, shipping_address) VALUES (%s, %s)", (customer_id, shipping_address))
    cn.commit()
    print('New Basket created')

def add_to_basket(basket_id, isbn, count):
    cn = connection()
    cur = cn.cursor()
    val = (basket_id, isbn, count)
    cur.execute("INSERT INTO basket_book VALUES (%s, %s, %s)", val)
    cn.commit()
    print('Added book(s) to basket')



def get_delivery_status(basket_id):
    order = get_basket(basket_id)
    if order.place_date:
        return get_basket(basket_id).delivery_status
    else:
        return 'The order has not been placed yet'


#owners
def add_author(name, address):
    cn = connection()
    cur = cn.cursor()
    val = (name, address)
    cur.execute("INSERT INTO author (name, address) VALUES (%s, %s)", val)
    cn.commit()
    print('New Author created')

def add_publisher(name, email, phone=None, address=None, banking_account=None):
    cn = connection()
    cur = cn.cursor()
    val = (name, phone, email, address, banking_account)
    cur.execute("INSERT INTO publisher (name, phone, email, address, banking_account) VALUES\
         (%s, %s, %s, %s, %s)", val)
    cn.commit()
    print('New Publisher created')

def get_author_by_name_address(name, address):
    cn = connection()
    cur = cn.cursor()
    cur.execute("select * from author where name = %s or address = %s", (name,address,))
    return (cur.fetchone())

def get_publisher_by_name_email(name, email):
    cn = connection()
    cur = cn.cursor()
    cur.execute("select * from publisher where name = %s or address = %s", (name,email,))
    return (cur.fetchone())

def add_book(isbn, name, author, author_address, publisher, publisher_email, 
        genre, pages, price, cost, percentage, count):
    cn = connection()
    cur = cn.cursor()

    #get author id by author name and address
    if get_author_by_name_address(author, author_address):

        author_id = get_author_by_name_address(author, author_address)[0]
    else:
    # TODO: if not found:
        add_author(name, author_address)
        author_id = get_author_by_name_address(author, author_address)[0]

    #get publisher id by ...
    if get_publisher_by_name_email(publisher, publisher_email):
        publisher_id = get_publisher_by_name_email(publisher, publisher_email)[0]
    else:
        add_publisher(publisher, publisher_email)
        publisher_id = get_publisher_by_name_email(publisher, publisher_email)[0]

    # insert 
    val = (isbn, name, publisher_id, author_id, genre, pages, price, cost, percentage, count)
    cur.execute("INSERT INTO book (isbn, name, publisher_id, author_id, genre, pages, price, cost, percentage, count) VALUES\
         (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", val)
    cn.commit()
    print('New Book created')

def remove_book(isbn):
    cn = connection()
    cur = cn.cursor()
    cur.execute("DELETE FROM book WHERE isbn = %s", (isbn,))
    cn.commit()
    print('Book removed')

def get_books_of_basket(basket_id):
    cn = connection()
    cur = cn.cursor()
    cur.execute("select * from basket_book where basket_id = %s", (basket_id,))
    return (cur.fetchall())


def place_order(basket_id):
    cn = connection()
    cur = cn.cursor()
    shipping_address = get_basket(basket_id)[4]
    books = get_books_of_basket(basket_id)

    total_payment = 0
    for b in books:
        price = get_book(b[1])[6] * b[2]
        total_payment += price
    
    val = (datetime.now(), shipping_address, total_payment, int(basket_id),)
    cur.execute("UPDATE basket SET place_date = %s, shipping_address = %s, total_payment = %s Where id = %s", val)
    cn.commit()
    print('Order placed')
    return get_basket(basket_id)

def get_total_sales():
    cn = connection()
    cur = cn.cursor()
    cur.execute("select SUM(total_payment) from basket where place_date IS NOT NULL")
    output = []
    for row in cur:
        output.append(str(row[0]))
    return (output[0])

def get_total_expenditures():
    cn = connection()
    cur = cn.cursor()
    cur.execute("select SUM(cost * count + cost * count * percentage) from book ")
    output = []
    for row in cur:
        output.append(str(row[0]))
    return (output[0])

def get_sales_per_genre():
    cn = connection()
    cur = cn.cursor()
    cur.execute("select sum(distinct b.total_payment), bo.genre from basket as b inner join basket_book as bb on b.id = bb.basket_id \
        inner join book as bo on bb.isbn = bo.isbn group by bo.genre ")
    return (cur.fetchall())

def get_sales_per_author():
    cn = connection()
    cur = cn.cursor()
    cur.execute("select sum(distinct b.total_payment), a.name from basket as b inner join basket_book as bb on b.id = bb.basket_id \
        inner join book as bo on bb.isbn = bo.isbn inner join author as a on bo.author_id = a.id group by bo.author_id")
    return (cur.fetchall())

def get_sales_per_publisher():
    cn = connection()
    cur = cn.cursor()
    cur.execute("select sum(distinct b.total_payment), p.name from basket as b inner join basket_book as bb on b.id = bb.basket_id \
        inner join book as bo on bb.isbn = bo.isbn inner join publisher as p on bo.publisher_id = p.id group by p.id")
    return (cur.fetchall())