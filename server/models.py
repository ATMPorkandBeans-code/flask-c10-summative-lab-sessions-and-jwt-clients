from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields
from decimal import Decimal
from config import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = (
        db.CheckConstraint('length(username) >= 6'),
    )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)

    expenses = db.relationship('Expense', back_populates='user')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
    
    def __repr__(self):
        return f'<user {self.username}>'
    
class Expense(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates="expenses")

    # @validates('amount')
    # def validate_price(self, key, value):
    #     # 1. Convert to float for validation if needed, or check decimal places
    #     try:
    #         amount = Decimal(str(value))
    #     except:
    #         raise ValueError("Amount must be a valid number")

    #     # 2. Check for negative values
    #     if amount < 0:
    #         raise ValueError("Amount cannot be negative")

    #     # 3. Check for more than 2 decimal places (dollars and cents)
    #     if abs(amount.as_tuple().exponent) > 2:
    #         raise ValueError("Amount can only have up to two decimal places")

    #     return amount

    def __repr__(self):
        return f'<Expense: {self.id}: {self.title}>'
    
class UserSchema(Schema):
    id = fields.Int()
    username = fields.String()

    expenses = fields.List(fields.Nested(lambda: ExpenseSchema(exclude=("user",))))

class ExpenseSchema(Schema):
    id = fields.Int()
    title = fields.String()
    amount = fields.Float()

    user = fields.Nested(UserSchema(exclude=("expenses",)))
    
    

