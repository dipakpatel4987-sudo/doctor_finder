# Doctor Finder

Django web app: patients doctors dhundte hain, appointment book karte hain aur payment (test mode) karte hain. Doctors apni appointments confirm ya cancel karte hain.

## Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   (aur .env me SECRET_KEY bharo)
python manage.py migrate
python manage.py seed_doctors
python manage.py createsuperuser
python manage.py runserver