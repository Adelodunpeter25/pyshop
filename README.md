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
- 🛠️ Django admin for managing **products, offers, and profiles**
- 📦 **Import/export** products in admin panel
- 🎨 **Customizable admin interface** with themes (using `admin_interface`)
- 🌗 Toggle between **light and dark mode**
- 📝 Viewable **order history** (extendable for carts/checkout)
- 🚀 Production-ready with **PostgreSQL** on Render

---

## 🛠️ Tech Stack

| Technology             | Purpose                         |
|------------------------|----------------------------------|
| Python 3 & Django      | Core backend framework          |
| Bootstrap 5 (CDN)      | UI and responsive design        |
| SQLite (dev)           | Lightweight dev database        |
| PostgreSQL (Render)    | Production database             |
| Pillow                 | Image handling (avatars, etc.)  |
| django-widget-tweaks   | Form rendering customization    |
| django-import-export   | Admin CSV/XLS import-export     |
| admin-interface        | Modern Django admin theming     |

---

## ⚡ Getting Started

Follow these steps to run PyShop on your local machine:

```bash
# 1. Clone the repository
git clone <https://github.com/Adelodunpeter25/myfirstwebsite>
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

- Deploy on Render (recommended), Heroku, or any cloud platform.
- For production, use PostgreSQL and set up environment variables for security.
- Collect static files with:

```bash
python manage.py collectstatic
```

---

## 🔄 Migrating Data from SQLite to PostgreSQL

To move your products from SQLite to your Render PostgreSQL database:

```bash
# Export products from SQLite
python manage.py dumpdata products > products.json

# Switch DATABASES in settings.py to PostgreSQL and run migrations
python manage.py migrate

# Import products into PostgreSQL
python manage.py loaddata products.json
```

---

## 🎨 Admin Panel Customization

- The admin panel uses `admin_interface` for a modern look.
- Customize themes and colors in the Django admin under the “Themes” section or via the `ADMIN_INTERFACE_THEME` setting.

---

## 📄 License

MIT License
