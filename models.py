
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from extensions import db  # ✅ Use the same db, do NOT re-create it


# db = SQLAlchemy()
bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)



class event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(500), nullable=True)  # this is for both image and vedio 
    description = db.Column(db.Text, nullable=True)

class dish(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cuisine = db.Column(db.String(50), nullable=False)       # Added
    veg = db.Column(db.Boolean, nullable=False, default=True) # Added
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=True)          # Added
    description = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(50), nullable=True)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime)
    
    # New fields
    event_date = db.Column(db.Date, nullable=True)
    service = db.Column(db.String(100), nullable=True)
    budget = db.Column(db.String(50), nullable=True)