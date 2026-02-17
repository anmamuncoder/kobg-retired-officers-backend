# KOBG Retired Officers Backend

Backend REST API for **KOBG (King of the Battle Group) – Retired Armoured Officers** membership and information management system.

This project is built with **Django** and **Django REST Framework** and is designed to handle officer registration, gallery, notices, and user management.

---

## Tech Stack

- Python 3.x
- Django
- Django REST Framework (DRF)
- MySQL / PostgreSQL (configurable)
- JWT Authentication
- Git
- Docker 

---

## 📁 Project Structure

```text 
kobg-retired-officers-backend/
├── apps/
│   ├── base/        # Common utilities and shared logic
│   ├── gallery/     # Gallery management
│   ├── notice/      # Notices and announcements
│   ├── officer/     # Retired officer information
│   └── user/        # User and authentication logic
│
├── core/            # Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```



> [kobg-retired-officers-backend](https://github.com/anmamuncoder/kobg-retired-officers-backend)
