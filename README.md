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

<br>

### Location of API Docs OpenAPI 3.0 specification
 
#### **How to View the API Documentation**

You can load the file directly in Swagger Online Editor: <br>
🔗 **Swagger Online Editor** [editor.swagger.io](https://editor.swagger.io/)

**Steps:**

1. Open the Swagger Editor link above.
2. On the top menu, click **File → Import File → Paste JSON/YAML**.
3. Open the `docs/*.yml` file from this repository on GitHub.
4. Copy the entire contents of the YAML file.
5. Paste it into the Swagger Editor.
6. The interactive API documentation will load automatically.

<br>

```shell
docs/
├── user-management.yml      # Authentication APIs 
│                             # Role Base Admin/Officer Login, Register, Admin create, Officer Register Data approve, Profile Update
│

```
<br>



> [kobg-retired-officers-backend](https://github.com/anmamuncoder/kobg-retired-officers-backend)
