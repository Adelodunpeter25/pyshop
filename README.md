# 🛍️ PyShop – Django E-commerce App

PyShop is a modern, responsive e-commerce web application built with Django. It features a clean UI (with dark mode!), user authentication, product listings by category, admin tools, and more.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/Django-4.x-green" alt="Django">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

---

## 🚀 Features

- 🛒 Browse products by **category and subcategory**
- 🔍 Smart **search** and **filtering**
- 👤 User **registration**, **login**, and **profile management**
- 🖼️ Profile editing with **avatar upload**
- 🛠️ Django admin for managing **products and offers**
- 📦 **Import/export** products in admin panel
- 🌗 Toggle between **light and dark mode**
- 📝 Viewable **order history** (extendable for carts/checkout)

---

## 🛠️ Tech Stack

| Technology             | Purpose                         |
|------------------------|----------------------------------|
| Python 3 & Django 4    | Core backend framework          |
| Bootstrap 5 (CDN)      | UI and responsive design        |
| SQLite (default)       | Lightweight dev database        |
| PostgreSQL (prod)      | Production database             |
| Pillow                 | Image handling (avatars, etc.)  |
| django-widget-tweaks   | Form rendering customization    |
| django-import-export   | Admin CSV/XLS import-export     |

---

## ⚡ Getting Started

Follow these steps to run PyShop on your local machine:

```bash
# 1. Clone the repository
git clone https://github.com/Adelodunpeter25/pyshop.git
cd pyshop

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
python manage.py migrate

# 5. Create a superuser
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 🌐 Deployment

- Ready for deployment on Render, Heroku, or any cloud platform.
- For production, use PostgreSQL and set up environment variables for security.
- Collect static files with:

```bash
python manage.py collectstatic
```

---

## ⚠️ Database Migration Note

If you switch from SQLite to PostgreSQL, migrate your data using Django’s `dumpdata` and `loaddata` commands:

```bash
python manage.py dumpdata > data.json
# Switch to PostgreSQL and run migrations
python manage.py migrate
python manage.py loaddata data.json
```

## 📄 License

MIT License
