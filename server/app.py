from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from config import app, db, api
from models import User, UserSchema, Expense, ExpenseSchema

class Signup(Resource):
    def post(self):
        request_json = request.get_json()

        username = request_json.get('username')
        password = request_json.get('password')

        user = User(
            username=username
        )

        user.password_hash = password

        try:
            db.session.add(user)
            db.session.commit()
            # session['user_id'] = user.id
            return UserSchema().dump(user), 201
        except IntegrityError:
            return {'error': '422 Unprocessable Entity'}, 422
        
class CheckSession(Resource):
    def get(self):

        if session.get('user_id'):
            user = User.query.filter(User.id == session['session_id']).first()
            return UserSchema().dump(user), 200
        
        return {'error': '401 Unauthorized'}, 401
    
class Login(Resource):
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']

        user = User.query.filter(User.username == username).first()

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return UserSchema().dump(user), 200
        
        return {'error': '401 Unauthorized'}, 401
    
class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            return {}, 204
        return {'error': '401 Unauthorized'}, 401
    
class ExpenseIndex(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            expenses = [ExpenseSchema().dump(e)
                         for e in Expense.query.filter_by(user_id=user_id).all()]
            return expenses, 200
        return {'error': '401 Unauthorized'}, 401
    
    def post(self):
        user_id = session.get('user_id')
        if user_id:
            request_json = request.get_json()
            print(Expense)
            expense = Expense(
                # id = request_json.get('id'),
                title = request_json.get('title'),
                amount = request_json.get('amount'),
                user_id = user_id
            )
            try:
                db.session.add(expense)
                db.session.commit()
                return ExpenseSchema().dump(expense), 201
            except IntegrityError:
                return {'error': '422 Unprocessable Entity'}, 422
        else:
            return {'error': '401 Unauthorized'}, 401
        
class Expense_by_Index(Resource):
    def get(self, id):
        user_id = session.get('user_id')
        if user_id:
            expense = Expense.query.filter(Expense.id == id).first()
            if not expense:
                {'error': 'Expense not found'}, 404
            if expense.user_id != user_id:
                return {'error': '401 Unauthorized'}, 401
            return ExpenseSchema().dump(expense), 200
        else:
            return {'error': '401 Unauthorized'}, 401
        
    def patch(self, id):
        user_id = session.get('user_id')
        if user_id:
            request_json = request.get_json()
            expense = Expense.query.filter(Expense.id == id).first()
            if not expense:
                {'error': 'Expense not found'}, 404
            if expense.user_id != user_id:
                return {'error': '401 Unauthorized'}, 401
            if 'title' in request_json:
                expense.title = request_json['title']
            if 'amount' in request_json:
                expense.amount = request_json['amount']
            try:
                db.session.commit()
                return ExpenseSchema().dump(expense), 200
            except IntegrityError:
                return {'error': '422 Unprocessable Entity'}, 422

        else:
            return {'error': '401 Unauthorized'}, 401
        
    def delete(self, id):
        user_id = session.get('user_id')
        if user_id:
            expense = Expense.query.filter(Expense.id == id).first()
            if not expense:
                {'error': 'Expense not found'}, 404
            if expense.user_id != user_id:
                return {'error': '401 Unauthorized'}, 401
            try:
                db.session.delete(expense)
                db.session.commit()
            except IntegrityError:
                return {'error': '422 Unprocessable Entity'}, 422
            
            return {}, 204
        else:
            return {'error': '401 Unauthorized'}, 401
            
    

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(ExpenseIndex, '/expenses', endpoint='expenses')
api.add_resource(Expense_by_Index, '/expenses/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)