# 🛍️ PyShop – Django E-commerce Website

PyShop is a modern, responsive e-commerce website built with Python and Django. It features a clean UI, user authentication, product listings by category, Paystack payment integration, order management, and a beautiful Jazzmin admin interface.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/Django-4.x-green" alt="Django">
  <img src="https://img.shields.io/badge/Paystack-Integrated-orange" alt="Paystack">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

---

## 📚 Table of Contents

* [🚀 Features](#-features)
* [🛠️ Tech Stack](#️-tech-stack)
* [⚡ Getting Started](#-getting-started)
* [💳 Payment Setup](#-payment-setup)
* [🛒 Admin Panel](#-admin-panel)
* [📁 Project Structure](#-project-structure)
* [🌐 Deployment](#-deployment)
* [📄 License](#-license)

---

## 🚀 Features

* 🛒 Browse products by **category and subcategory**
* 🔍 Smart **search** and **filtering** with pagination
* 👤 User **registration**, **login**, and **profile management**
* 💳 **Paystack payment integration** for secure checkout
* 📦 **Order management** with order history and tracking
* 🧾 **Invoice generation** and order details
* 🛠️ **Jazzmin admin** for managing products, orders, and users
* 📱 **Responsive design** with mobile-friendly UI
* 🚀 Production-ready with **PostgreSQL** support

---

## 🛠️ Tech Stack

| Technology           | Purpose                        |
| -------------------- | ------------------------------ |
| Python 3.9+ & Django 4.x | Core backend framework     |
| Bootstrap 5 (CDN)    | UI and responsive design       |
| SQLite (dev)         | Lightweight dev database       |
| PostgreSQL (prod)    | Production database            |
| Paystack             | Payment processing             |
| django-jazzmin       | Modern admin interface         |
| django-widget-tweaks | Form rendering customization   |
| uv                   | Fast Python package manager    |

---

## ⚡ Getting Started

Follow these steps to run PyShop on your local machine:

```bash
# 1. Clone the repository
git clone https://github.com/Adelodunpeter25/pyshop.git
cd pyshop

# 2. Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Create virtual environment and install dependencies
uv sync

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your Paystack keys

# 5. Run database migrations
uv run python manage.py migrate

# 6. Create a superuser
uv run python manage.py createsuperuser

# 7. Start the development server
uv run python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

### Using Makefile (Optional)

```bash
make install      # Install dependencies
make migrate      # Run migrations
make superuser    # Create superuser
make run          # Start server
make clean        # Clean cache files
```

---

## 💳 Payment Setup

1. Sign up at [Paystack](https://paystack.com)
2. Get your API keys from the dashboard
3. Add to `.env` file:
   ```
   PAYSTACK_SECRET_KEY=sk_test_xxxxx
   PAYSTACK_PUBLIC_KEY=pk_test_xxxxx
   ```

---

## 🛒 Admin Panel

* Access the Jazzmin admin at `/admin` with your superuser account
* Manage products, orders, users, and offers
* View order details and update order status
* Track inventory and low stock alerts
* Beautiful dark-themed interface

---

## 📁 Project Structure

```
products/
├── views/
│   ├── product_views.py    # Product listings & details
│   ├── auth_views.py       # Authentication
│   ├── cart_views.py       # Shopping cart
│   ├── order_views.py      # Orders & payment
│   └── profile_views.py    # User profiles
├── models.py               # Database models
├── admin.py                # Admin configuration
└── templates/              # HTML templates
```

---

## 🌐 Deployment

* Deploy on Render (recommended), Heroku, or any cloud platform
* For production, use PostgreSQL and set up environment variables
* Collect static files with:

```bash
uv run python manage.py collectstatic
```

### 🔗 Live Demo

You can check out a live version of PyShop here:
[https://pyshop1.onrender.com](https://pyshop1.onrender.com)

---

## 📄 License

MIT License

---

## 👨‍💻 Author

**Adelodun Peter**

© 2025 PyShop. All rights reserved.
