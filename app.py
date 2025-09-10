from flask import Flask, render_template, request, redirect, url_for, flash ,session
import os 
import click
from models import db, dish,Contact,Event
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_mail import Message
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from datetime import datetime

# from flask_wtf import CSRFProtect

load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static')
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret")

# Database config
# Database config (Postgres)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    "DATABASE_URL",  # Read from environment
    "postgresql://postgres:postgres@localhost:5432/dcevent")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind SQLAlchemy to app
db.init_app(app)

# Flask-Migrate setup
migrate = Migrate(app, db)

# Flask-Mail config
# Flask Config from .env
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS") == "True"
app.config['MAIL_USE_SSL'] = os.getenv("MAIL_USE_SSL") == "True"
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)


# Configure upload folder
# Path relative to the app root
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads', 'videos')
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads', 'videos')

ALLOWED_EXTENSIONS =  {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'ogg'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/admin/dishes')
def dish_dashboard():
    dishes = dish.query.all()
    total_dishes=len(dishes)
    return render_template('dishe.html', dishes=dishes,total=total_dishes)

@app.route('/admin/dishes/add', methods=['POST'])
def add_dish():
    name = request.form['name']
    cuisine = request.form['cuisine']
    veg = request.form.get('veg') == 'on'
    price = request.form['price']
    description = request.form['description']
    category = request.form['category']

    image_file = request.files.get('image')
    image_path = None

    if image_file and image_file.filename != '':
        # Save to static/uploads/images/
        image_folder = os.path.join(app.root_path, 'static', 'uploads', 'images')
        os.makedirs(image_folder, exist_ok=True)
        filename = secure_filename(image_file.filename)
        save_path = os.path.join(image_folder, filename)
        image_file.save(save_path)
        # Store relative path for use in templates
        image_path =filename    

    d = dish(
        name=name,
        cuisine=cuisine,
        veg=veg,
        price=price,
        category=category,
        image=image_path,
        description=description
    )
    db.session.add(d)
    db.session.commit()
    return redirect(url_for('dish_dashboard'))



@app.route('/dishes')
def catering():
    
    DD = dish.query.all()
    return render_template('catering.html',dishes=DD)


# Delete Dish
@app.route('/admin/dishes/delete/<int:dish_id>', methods=['POST'])
def delete_dish(dish_id):   # ✅ fixed param name
    d = dish.query.get_or_404(dish_id)

    # also remove image if exists
    if d.image:
        file_path = os.path.join(app.root_path, 'static', 'uploads', 'images', d.image)
        if os.path.exists(file_path):
            os.remove(file_path)

    db.session.delete(d)
    db.session.commit()
    return redirect(url_for('dish_dashboard'))





@app.route('/admin/dishes/edit/<int:dish_id>', methods=['GET', 'POST'])
def edit_dish(dish_id):
    d = dish.query.get_or_404(dish_id)

    if request.method == 'POST':
        d.name = request.form['name']
        d.cuisine = request.form['cuisine']
        d.veg = request.form['veg'] == 'True'   # ✅ works with radio buttons
        d.price = request.form['price']
        d.category = request.form['category']
        d.description = request.form['description']

        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            image_folder = os.path.join(app.root_path, 'static', 'uploads', 'images')
            os.makedirs(image_folder, exist_ok=True)
            filename = secure_filename(image_file.filename)
            save_path = os.path.join(image_folder, filename)
            image_file.save(save_path)
            d.image = filename   # ✅ store filename only

        db.session.commit()
        return redirect(url_for('dish_dashboard'))

    return render_template('edit_dish.html', dish=d)



# Add Event Page
@app.route('/admin/events/add', methods=['GET', 'POST'])

# need to update the video path
def add_event():
    if request.method == 'POST':
        name = request.form['name']
        date_str = request.form['date']
        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        location = request.form['location']
        guests = request.form['guests']
        description = request.form.get('description')

        video_file = request.files.get('video')
        video_path = None

        if video_file and allowed_file(video_file.filename):
            filename = secure_filename(video_file.filename)

            # Make sure folder exists
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

            # Absolute path for saving
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            video_file.save(save_path)

            # Store only relative path without "static/"
            video_path = f"uploads/videos/{filename}"

        e = Event(
            name=name,
            date=date,
            location=location,
            guests=guests,
            image=video_path,  # store relative path only
            description=description
        )
        db.session.add(e)
        db.session.commit()
        return redirect(url_for('events_dashboard'))

    return render_template('add_event.html')

# Edit Event
@app.route('/admin/events/edit/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    e = Event.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form['name']
        date_str = request.form['date']
        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        location = request.form['location']
        guests = request.form['guests']
        description = request.form.get('description')

        # Handle file upload (video or image)
        uploaded_file = request.files.get('media')  # rename input field in form to "media"
        media_path = None

    if uploaded_file and allowed_file(uploaded_file.filename):
        filename = secure_filename(uploaded_file.filename)

        # Ensure upload folder exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Save file
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(save_path)

        # Store only relative path (without "static/")
        media_path = f"uploads/media/{filename}"

    # Save event
        e = Event(
            name=name,
            date=date,
            location=location,
            guests=guests,
            image=media_path,  # can be video or image
            description=description
        )
        db.session.add(e)
        db.session.commit()
        return redirect(url_for('events_dashboard'))

    return render_template('edit_event.html', event=e)

# Delete Event
@app.route('/admin/events/delete/<int:id>')
def delete_event(id):
    e = Event.query.get_or_404(id)
    if e.image and os.path.exists(e.image):
        os.remove(e.image)  # remove video from server
    db.session.delete(e)
    db.session.commit()
    return redirect(url_for('events_dashboard'))

# Show All Events
@app.route('/admin/events')
def events_dashboard():
    events = Event.query.all()
    return render_template('events_dashboard.html', events=events)




@app.route('/calculator')

def calculator():
    all_dishes=dish.query.all()
    categories = ['Appetizer', 'Main Course', 'Dessert']

    dishes_by_category = {cat: [] for cat in categories}

    for d in all_dishes:
        if d.category in categories:
            dishes_by_category[d.category].append({
                'id': d.id,
                'name': d.name,
                'description': d.description,
                'price': d.price
            })
    return render_template('calculator.html', dishes_by_category=dishes_by_category)


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
        'id': 4,
        'name': 'Entertainment',
        'icon': 'fas fa-music',
        'price': 'Starting from ₹20,000',
        'description': 'Keep your guests entertained with our music and entertainment services.',
        'features': ['Professional DJ', 'Live band options', 'Sound system', 'Dance floor setup']
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
        'name': 'Wedding Photography',
        'icon': 'fas fa-camera',
        'price': 'Starting from ₹25,000',
        'description': 'Capture your special moments with our professional photography services.',
        'features': ['Pre-wedding shoot', 'Wedding day coverage', 'Edited photos', 'Online gallery']
    }
]




# Define the filter
def imgsrc_filter(path):
    # You can modify this logic as needed
    return f"/static/images/{path}"

# Register it
app.jinja_env.filters['imgsrc'] = imgsrc_filter


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



# @app.get("/api/dishes")
# def api_dishes():
#     # Simple: return all dishes, no filters/CRUD
#     return jsonify(DISHES)

# @app.get("/catering")
# def catering_page():
#     # Render a page that shows all dishes using a simple attractive grid
#     return render_template("catering.html", dishes=DISHES)



@app.route('/')
def home():
    all_events = Event.query.all()
    dd = dish.query.all()
    return render_template('index.html',events=all_events,d=dd)
@app.route('/about')
def aboutus():
    return render_template('about.html')

@app.route('/packages')
def packages():
    return render_template('packages.html', packages=packages_data)

@app.route('/services')
def services():
    return render_template('services.html', services=services_data)

@app.route('/events')
def events():
    q=Event.query.all()
    return render_template('events.html', all_evnt=q)

@app.route('/dishes')
def dishes():
    return render_template('dishes.html', dishes=dishes_data)



@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            message_text = request.form.get('message')
            event_date_str = request.form.get('event_date')
            service = request.form.get('service')
            budget = request.form.get('budget')

            # Convert event date if provided
            event_date = None
            if event_date_str:
                event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()

            # Save to database
            contact_entry = Contact(
                name=name,
                email=email,
                phone=phone,
                message=message_text,
                event_date=event_date,
                service=service,
                budget=budget
            )
            db.session.add(contact_entry)
            db.session.commit()

            # Send Email
            msg = Message(
                subject="📩 New Contact Form Submission",
                sender=email,  # sender is the user's email
                recipients=["abbdulrazza@gmail.com"],  # receiver (you)
                body=f"""
You have received a new contact form submission:

Name: {name}
Email: {email}
Phone: {phone}
Message: {message_text}
Event Date: {event_date if event_date else 'N/A'}
Service: {service}
Budget: {budget}
"""
            )
            mail.send(msg)

            flash("✅ Your message has been sent successfully!", "success")
            return redirect(url_for('contact'))

        except Exception as e:
            print("Error:", e)
            flash("❌ Something went wrong. Please try again later.", "danger")
            return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True,port=5000)
