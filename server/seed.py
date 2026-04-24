from random import randint, choice as rc
from faker import Faker
from app import app
from models import db, Expense, User

fake = Faker()

with app.app_context():
    print("Deleting all records...")
    Expense.query.delete()
    User.query.delete()
    # db.session.commit()

    fake = Faker()

    print("Creating users...")

    
    users = []
    usernames = []

    for i in range(20):
        #make sure users have unique usernames
        username = fake.unique.first_name()
        #make sure users unique usernames are at least 6 characters
        while len(username) < 7:
            username = fake.unique.first_name()
        usernames.append(username)

        user = User(
            username=username
        )
        #Password for Faker users is username + 'password' ie. Jacquelinepassword
        user.password_hash = user.username + 'password'

        users.append(user)

    db.session.add_all(users)

    print("Creating expenses...")
    expenses = []
    for i in range(50):
        # Fake dollar and cents amount for an expense
        amount = fake.pydecimal(            
            left_digits=3, 
            right_digits=2, 
            positive=True, 
            min_value=1.00, 
            max_value=500.00)
        
        expense = Expense(
            title=fake.sentence(nb_words=3),
            amount=amount)
        
        expense.user = rc(users)

        expenses.append(expense)
    
    db.session.add_all(expenses)
    db.session.commit()
    print("Complete.")


