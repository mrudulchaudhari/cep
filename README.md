# cep

Anandwan Visitor Room Booking System
A web-based room booking system for Anandwan, a community rehabilitation center founded by social activist Baba Amte near Warora in Maharashtra, India.
Project Overview
This system aims to streamline the process of room booking for visitors at Anandwan. The current manual process creates inefficiencies that this project aims to solve, including:

Difficulty checking room availability in advance
Challenges in managing deposits and refunds
Inefficient allocation of rooms
Limited ability to forecast visitor numbers
Communication gaps between visitors and management

Features

User registration and profile management
Room availability search and calendar view
Online booking with instant confirmation
Secure payment processing for deposits
Automated receipt generation
Booking management and cancellation
Admin dashboard for inventory management
Accessibility features

Technology Stack

Backend: Django 4.2.7
Frontend: Bootstrap 5
Database: SQLite (development) / PostgreSQL (production)
Additional Libraries:

Pillow for image processing
django-crispy-forms for enhanced form handling
crispy-bootstrap5 for Bootstrap 5 compatibility



Project Structure
anandwan_booking/
├── anandwan_booking/      # Main project folder
│   ├── __init__.py
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── booking/               # Booking app
│   ├── __init__.py
│   ├── admin.py           # Admin configuration
│   ├── apps.py            # App configuration
│   ├── models.py          # Database models
│   ├── migrations/        # Database migrations
│   ├── tests.py           # Testing
│   └── views.py           # View functions
├── manage.py              # Django management script
├── env/                   # Virtual environment
├── .gitignore             # Git ignore file
├── README.md              # Project documentation
└── requirements.txt       # Project dependencies
Installation

Clone the repository
Create a virtual environment: python -m venv env
Activate the virtual environment:

Windows: env\Scripts\activate
Linux/Mac: source env/bin/activate


Install dependencies: pip install -r requirements.txt
Run migrations: python manage.py migrate
Create a superuser: python manage.py createsuperuser
Start the development server: python manage.py runserver

Models

RoomType: Defines different types of rooms with prices and capacities
Room: Represents individual rooms with room numbers
Visitor: Extends the User model with visitor information (Aadhar number, etc.)
Booking: Contains booking details including dates and status
Payment: Tracks payment information related to bookings

Contributors

Prem Baba (Group Leader) – B53
Mrudul Chaudhari – B29
Om Patni – B38
Pihu Patne – B42
Homeshwari Baitalwar – B7