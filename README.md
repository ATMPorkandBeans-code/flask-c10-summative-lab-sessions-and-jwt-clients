EXPENSE TRACKER:

Here is a Flask/React app that can track expenses for different users. The app is complete with a React frontend with signup, login and check session capabilities, as well as a backend that utilizes a Flask constructed API that uses SQLAlchemy and api as a database. The user will create an account with username and password and then have the oppurtunity to save the names and amounts of various expenses to their user accounts. All accounts are protected by user authentication and authorization only on that user's routes.

TECH STACK:

1. REACT (Front-end)
2. FLASK/FLASK-RESTFUL (RESTAPI)
3. SQLALCHEMY (Database)

PREREQUISITES:

1. Python(3.x)
2. Node.js(v20+ recommended)
3. pip or pipenv
4. npm or yarn

BACKEND SETUP(FLASK + SQLALCHEMY):

In the terminal run:

git clone https://github.com/ATMPorkandBeans-code/flask-c10-summative-lab-sessions-and-jwt-clients
cd flask-c10-summative-lab-sessions-and-jwt-clients
cd server

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

pip install -r requirements.txt

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

flask run
OR
python app.py

FRONTEND SETUP(REACT):

cd frontend # or client

npm install
npm start

RUNNING APP (SIMULTANEOUSLY):

flask run

npm start

SEEDING DATABASE:

In terminal run:

python seed.py

PROJECT STRUCTURE:

The backend consists of models.py that detail the User and Expense class tables in SQLALCHEMY. It uses Marshmallow to Schema the information in and out of the Flask app. The Flask app.py consists of a variety of different routes such as:

1. '/signup'
2. '/check_session'
3. '/login'
4. '/logout'
5. '/expenses'
6. '/expenses/<int:id>'

These routes allow the user to signup, log in, check session, logout, view their personal expense list, post a new expense, view a single expense by id, edit a single expense, and delete a single expense. The seed file uses Faker to create 20 unique users and 50 different sample expenses with amounts.
