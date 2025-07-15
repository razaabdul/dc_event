from flask import Flask, render_template, request, redirect, url_for, flash
import os 
from dotenv import load_dotenv
from flask_migrate import Migrate
import click
from models import db, dish,Contact
from flask_mail import Mail
from flask_mail import Message

# from flask_wtf import CSRFProtect

app = Flask(__name__, static_folder='static')
app.secret_key = 'your-secret-key-here'
# csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback-secret")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///dishes.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

def create_db():
    """Create the database."""
    db.create_all()
    click.echo("Database created!")


# Flask-Mail config
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)






@app.route('/admin/dishes')
def dish_dashboard():
    dishes = dish.query.all()
    return render_template('dishe.html', dishes=dishes)

@app.route('/admin/dishes/add', methods=['POST'])
def add_dish():
    name = request.form['name']
    category = request.form['category']
    price = request.form['price']
    description = request.form['description']

    d = dish(name=name, category=category, price=price, description=description)
    db.session.add(d)
    db.session.commit()
    return redirect(url_for('dish_dashboard'))

@app.route('/admin/dishes/delete/<int:id>')
def delete_dish(id):
    d = dish.query.get_or_404(id)
    d.session.delete(d)
    d.session.commit()
    return redirect(url_for('dish_dashboard'))

@app.route('/admin/dishes/edit/<int:id>', methods=['POST'])
def edit_dish(id):
    Dish = dish.query.get_or_404(id)
    Dish.name = request.form['name']
    Dish.category = request.form['category']
    Dish.price = request.form['price']
    Dish.description = request.form['description']
    db.session.commit()
    return redirect(url_for('dish_dashboard'))


@app.route('/calculator')
def calculator():
    dishes = dish.query.all()
    return render_template('calculator.html',dishes=dishes)


# Sample data (in a real app, this would come from a database)
packages_data = [
    {
        'id': 1,
        'name': 'Silver Package',
        'price': '₹50,000',
        'popular': False,
        'features': [
            'Basic Decoration',
            'Photography (4 hours)',
            'Basic Catering (50 guests)',
            'Sound System',
            'Basic Lighting'
        ]
    },
    {
        'id': 2,
        'name': 'Gold Package',
        'price': '₹1,00,000',
        'popular': True,
        'features': [
            'Premium Decoration',
            'Photography & Videography (8 hours)',
            'Premium Catering (100 guests)',
            'Professional Sound System',
            'LED Lighting',
            'Bridal Makeup',
            'Flower Arrangements'
        ]
    },
    {
        'id': 3,
        'name': 'Platinum Package',
        'price': '₹2,00,000',
        'popular': False,
        'features': [
            'Luxury Decoration',
            'Full Day Photography & Videography',
            'Premium Catering (200 guests)',
            'Professional DJ & Sound',
            'Designer Lighting',
            'Bridal & Groom Makeup',
            'Luxury Car Decoration',
            'Welcome Drinks'
        ]
    }
]

services_data = [
    {
        'id': 1,
        'name': 'Wedding Photography',
        'icon': 'fas fa-camera',
        'price': 'Starting from ₹25,000',
        'description': 'Capture your special moments with our professional photography services.',
        'features': ['Pre-wedding shoot', 'Wedding day coverage', 'Edited photos', 'Online gallery']
    },
    {
        'id': 2,
        'name': 'Decoration Services',
        'icon': 'fas fa-palette',
        'price': 'Starting from ₹15,000',
        'description': 'Transform your venue with our stunning decoration services.',
        'features': ['Floral arrangements', 'Stage decoration', 'Lighting setup', 'Theme-based decor']
    },
    {
        'id': 3,
        'name': 'Catering Services',
        'icon': 'fas fa-utensils',
        'price': 'Starting from ₹500/plate',
        'description': 'Delicious cuisine prepared by our expert chefs.',
        'features': ['Multi-cuisine options', 'Live counters', 'Professional service', 'Custom menus']
    },
    {
        'id': 4,
        'name': 'Entertainment',
        'icon': 'fas fa-music',
        'price': 'Starting from ₹20,000',
        'description': 'Keep your guests entertained with our music and entertainment services.',
        'features': ['Professional DJ', 'Live band options', 'Sound system', 'Dance floor setup']
    }
]

events_data = [
    {
        'id': 1,
        'name': 'Royal Palace Wedding',
        'date': '2024-02-15',
        'location': 'Mumbai',
        'guests': 300,
        # 'image': '/placeholder.svg?height=250&width=350',
        'image': 'static/WhatsApp Video 2025-07-13 at 4.34.09 PM.mp4',
        'description': 'A grand celebration at the Royal Palace with traditional decorations and premium catering.'
    },
    {
        'id': 2,
        'name': 'Beach Wedding Ceremony',
        'date': '2024-03-20',
        'location': 'Goa',
        'guests': 150,
        'image': '/placeholder.svg?height=250&width=350',
        'description': 'A beautiful beachside wedding with sunset views and coastal cuisine.'
    },
    {
        'id': 3,
        'name': 'Garden Wedding',
        'date': '2024-04-10',
        'location': 'Delhi',
        'guests': 200,
        'image': '/placeholder.svg?height=250&width=350',
        'description': 'An elegant garden wedding with floral themes and outdoor dining.'
    }
]

dishes_data = {
    'appetizers': [
        {'name': 'Paneer Tikka', 'price': '₹300', 'veg': True},
        {'name': 'Chicken Tikka', 'price': '₹400', 'veg': False},
        {'name': 'Aloo Tikki', 'price': '₹200', 'veg': True},
        {'name': 'Fish Amritsari', 'price': '₹450', 'veg': False}
    ],
    'main_course': [
        {'name': 'Dal Makhani', 'price': '₹350', 'veg': True},
        {'name': 'Butter Chicken', 'price': '₹500', 'veg': False},
        {'name': 'Palak Paneer', 'price': '₹400', 'veg': True},
        {'name': 'Mutton Curry', 'price': '₹600', 'veg': False},
        {'name': 'Biryani', 'price': '₹450', 'veg': False},
        {'name': 'Veg Biryani', 'price': '₹350', 'veg': True}
    ],
    'desserts': [
        {'name': 'Gulab Jamun', 'price': '₹150', 'veg': True},
        {'name': 'Ras Malai', 'price': '₹200', 'veg': True},
        {'name': 'Ice Cream', 'price': '₹100', 'veg': True},
        {'name': 'Kulfi', 'price': '₹120', 'veg': True}
    ]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/packages')
def packages():
    return render_template('packages.html', packages=packages_data)

@app.route('/services')
def services():
    return render_template('services.html', services=services_data)

@app.route('/events')
def events():
    return render_template('events.html', events=events_data)

@app.route('/dishes')
def dishes():
    return render_template('dishes.html', dishes=dishes_data)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message_text = request.form.get('message')
        event_date = request.form.get('event_date')
        service = request.form.get('service')
        budget = request.form.get('budget')

        # Save to database
        contact_entry = Contact(name=name, email=email, phone=phone, message=message_text,event_date=event_date
                                ,service=service,budget=budget)
        db.session.add(contact_entry)
        db.session.commit()

        # Send Email
        msg = Message(subject="New Contact Form Submission",
                    recipients=["razalatitude@gmail.com"],  # <-- Replace with your receiver
                    body=f"""
        New Contact Message:
        Name: {name}
        Email: {email}
        Phone: {phone}
        Message: {message_text}
        Event Date: {event_date}
        Service: {service}
        Budget: {budget}
        """)
        mail.send(msg)

        # flash('Thank you for contacting us! We will reach out soon.', 'success')

    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True,port=5002)
