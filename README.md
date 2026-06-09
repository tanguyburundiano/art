<<<<<<< HEAD
# Legal Texts Platform

Django site for internal lawyers to search, filter, copy and consult useful legal texts. Staff users can add, edit and delete parts, sections and articles.

## Features

- Login required for all users
- Staff dashboard
- Search by title, keyword, content, law number, part or section
- Filter by domain/part and section
- Copy button for every article
- Add/edit/delete only for staff users
- Django admin available at `/admin/`

## Installation

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_legaltexts
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## Staff access

To use the staff dashboard, the user must have `is_staff=True`. A superuser created with `createsuperuser` already has staff access.
=======
# art
>>>>>>> 8fb9b8beaaef9edd37a9563cb6c57c84c92cb7d6
# art
