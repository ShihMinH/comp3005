from flask import Flask, jsonify, request, render_template
from database.db_conn import *
import json
import datetime
app = Flask(__name__)

from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)

class DatetimeEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime):
      return str(obj)
    return json.JSONEncoder.default(self, obj)


@app.route('/')
def test_page():
    return render_template('index.html')


@app.route('/books', methods=['GET', 'POST', 'DELETE'])
def books():
    if request.method == 'POST':
        isbn = request.form.get('isbn')
        name = request.form.get('name')
        author = request.form.get('author')
        author_address = request.form.get('author_address')
        publisher = request.form.get('publisher')
        publisher_email = request.form.get('publisher_email')
        genre = request.form.get('genre')
        pages = request.form.get('pages')
        price = request.form.get('price')
        cost = request.form.get('cost')
        percentage = request.form.get('percentage')
        count = request.form.get('count')

        add_book(isbn, name, author, author_address, publisher, publisher_email, 
        genre, pages, price, cost, percentage, count)

        book = get_book(isbn=isbn)
        book = json.dumps(book, cls=DecimalEncoder)
        return jsonify(book) 
    elif request.method == 'GET':
        books = get_books_by_owner()
        books = json.dumps(books, cls=DecimalEncoder)
        return books
    elif request.method == 'DELETE':
        remove_book(request.args.get('isbn'))
        return 'OK and return to main page'

@app.route('/search_books', methods=['GET'])
def search_books():
    search_by = request.args.get('category')
    value = request.args.get('value')
    books = ()
    if search_by == 'All':
        books = get_books()
    elif search_by == 'ISBN':
        books = [get_book(value)]
    elif search_by == 'Name':
        books = get_books_by(name=value)
    elif search_by == 'Genre':
        books = get_books_by(genre=value)
    elif search_by == 'Author':
        books = get_books_by(author=value)
    elif search_by == 'Publisher':
        books = get_books_by(publisher=value)

    books = json.dumps(books, cls=DecimalEncoder)
    print(books)
    return books

@app.route('/track_order', methods=['GET'])
def track_order():
    basket_id = request.args.get('basket_id')

    basket = get_basket(basket_id)
    status = ''
    if basket:
        if basket[2] and basket[5]:
            status =  'Delivery Status is ' + basket[5]
        elif not basket[5]:
            status = 'Delivey Status has not been updated yet'
        else:
            status = 'Order not placed yet'
    else: 
        status = 'Order not found'
    return jsonify(status)

@app.route('/myaccount', methods=['GET', 'POST'])
def myaccount():
    return render_template('myaccount.html')
    # if request.method == 'POST':
    #     name = request.form.get('name')
    #     phone = request.form.get('phone')
    #     email = request.form.get('email')
    #     billing_address = request.form.get('billing_address')
    #     shipping_address = request.form.get('shipping_address')
    #     banking_account = request.form.get('banking_account')
    #     add_customer(name, phone, email, billing_address, shipping_address, banking_account)
    #     return 'OK', 200
    # elif request.method == 'GET':
    #     print(request.form.get('email'))
    #     account = get_customer_by_email(request.form.get('email'))
    #     return jsonify(account) 

@app.route('/accountinfo', methods=['GET', 'POST'])
def accountinfo():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        billing_address = request.form.get('billing_address')
        shipping_address = request.form.get('shipping_address')
        banking_account = request.form.get('banking_account')
        add_customer(name, phone, email, billing_address, shipping_address, banking_account)
        return 'OK', 200
    elif request.method == 'GET':
        account = get_customer_by_email(request.args.get('email'))
        return render_template('accountinfo.html', account=account)

@app.route('/owner', methods=['GET', 'POST'])
def owner():
    return render_template('owner.html')

@app.route('/basket', methods=['GET', 'POST'])
def basket():
    if request.method == 'POST':
        shipping_address = request.form.get('shipping_address')
        account_id = request.form.get('account_id')
        add_basket(account_id, shipping_address)
        
        baskets = get_baskets_by_customer_id(account_id)
        baskets = json.dumps(baskets, cls=DecimalEncoder,  default=str)
        return baskets

    elif request.method == 'GET':
        baskets = get_baskets_by_customer_id(request.args.get('account_id'))
        baskets = json.dumps(baskets, cls=DecimalEncoder, default=str)
        return baskets

@app.route('/author', methods=['GET', 'POST'])
def author():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')

        add_author(name, address)
        author = get_author_by_name_address(name, address)
        return jsonify(author) 
    elif request.method == 'GET':
        authors = get_authors()
        return jsonify(authors) 

@app.route('/publisher', methods=['GET', 'POST'])
def publisher():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        email = request.form.get('email')
        phone = request.form.get('phone')
        banking_account = request.form.get('banking_account')

        add_publisher(name, email, phone, address, banking_account)
        publisher = get_publisher_by_name_email(name, email)
        return jsonify(publisher) 
    elif request.method == 'GET':
        publishers = get_publishers()
        return jsonify(publishers) 

@app.route('/basket_book', methods=['GET', 'POST'])
def basket_book():
    if request.method == 'POST':
        basket_id = request.form.get('basket_id')
        isbn = request.form.get('isbn')
        count = request.form.get('count')
        add_to_basket(basket_id, isbn, count)
        books = get_books_of_basket(basket_id)
        return jsonify(books)
    elif request.method == 'GET':
        books = get_books_of_basket(request.args.get('basket_id'))
        return jsonify(books)
        # account = get_customer_by_email(request.args.get('email'))
        # return render_template('accountinfo.html', account=account)

@app.route('/place_order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        basket_id = request.form.get('basket_id')
        place_order(basket_id)
        return 'Success Return to main page to see status'
    elif request.method == 'GET':
        return 'OK'
        # baskets = get_baskets_by_customer_id(request.args.get('account_id'))
        # print(baskets)
        # return jsonify(baskets) 

@app.route('/report', methods=['GET', 'POST'])
def report():
    return render_template('report.html')

@app.route('/total_sales', methods=['GET'])
def total_sales():
    return get_total_sales()

@app.route('/total_expenditures', methods=['GET'])
def total_expenditures():
    return get_total_expenditures()

@app.route('/sales_per_genre', methods=['GET'])
def sales_per_genre():
    sales = json.dumps(get_sales_per_genre(), cls=DecimalEncoder)
    return sales

@app.route('/sales_per_author', methods=['GET'])
def sales_per_author():
    sales = json.dumps(get_sales_per_author(), cls=DecimalEncoder)
    return sales

@app.route('/sales_per_publisher', methods=['GET'])
def sales_per_publisher():
    sales = json.dumps(get_sales_per_publisher(), cls=DecimalEncoder)
    return sales


app.run(debug=True)