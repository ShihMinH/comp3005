To Run the Application:

1. Install Python 3 and pip.
Python 3: check https://www.python.org/downloads/ .
pip install: go to terminal and run command: python get-pip.py.

2. Install dependencies
pip install flask. 
pip install mysql-connector. 

3. Run APP
Go to database/db_conn.py, change database name and password if needed.
Go to proj folder and run command: python run.py.
Open browser and access http://127.0.0.1:5000/.



4. APP structure
run.py: contains all API endpoints .
database/db_conn.py: database connection and all the SQL query functions.
templates: contains all html pages with javascript functions.
SQL: sql related files.