
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()




class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(500), nullable=True)  # this is for both image and vedio 
    description = db.Column(db.Text, nullable=True)

class dish(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     category = db.Column(db.String(50), nullable=False)     
#     price = db.Column(db.Integer, nullable=False)
#     description = db.Column(db.String(255), nullable=True)

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