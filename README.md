# Doctor Finder

Django web app jahan patients doctors dhundte hain, appointment book karte hain aur payment (test mode) karte hain. Doctors apni appointments aur weekly schedule manage karte hain.

Live: https://deepak1195.pythonanywhere.com

## Features
- Patient / Doctor / Admin ke alag panel (role based login)
- Doctor directory: search, specialty/city filter, pagination, detail page
- Map par doctors (OpenStreetMap + Leaflet)
- Appointment booking, reschedule, cancel, double-booking check
- Doctor ki weekly availability (galat din/time par booking nahi hoti)
- Booking Summary (18% GST), mock Paytm payment, receipt, payment history
- Reviews aur ratings (doctor ki rating average se banti hai)
- Email notifications (booking, confirm, cancel, reschedule)
- Admin dashboard (stats, doctor approval)
- Custom 404 aur 500 pages

## Tech
Python 3.13, Django 6.1, SQLite, HTML/CSS/JavaScript

## Local setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_doctors
python manage.py createsuperuser
python manage.py runserver

## Tests
python manage.py test

## Project structure
config/        settings, urls
apps/accounts  custom User (email login, role), signup, login, profile
apps/doctors   Doctor, Availability, list, detail, map, doctor profile edit
apps/appointments  booking, reschedule, cancel, review, email notifications
apps/payments  summary, mock gateway, receipt, history
apps/core      home, admin dashboard, decorators, layout context
templates/     layouts (public, patient, doctor) aur page templates
static/        css, js