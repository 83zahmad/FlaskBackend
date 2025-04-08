
# 🧵 Clothing E-Commerce App - Backend Software Design Document (SDD)

## 1. Overview

This backend is built with **Flask** and supports two roles (Users and Admins). It includes secure authentication, product management, cart operations, and Stripe payment integration. The system connects to a PostgreSQL database using SQLAlchemy ORM with migrations handled by Flask-Migrate.

---

## 2. Backend Architecture

- **Framework**: Flask
- **Database**: PostgreSQL (in Docker)
- **ORM**: SQLAlchemy
- **Authentication**: JWT (Flask-JWT-Extended)
- **Payment Gateway**: Stripe
- **Migrations**: Flask-Migrate
- **Deployment**: Docker (local), Render/Railway (optional)

---

## 3. Key App Structure

```
/app
├── models/               # SQLAlchemy models for database schema
│   ├── user_model.py
│   ├── product_model.py
│   └── cart_model.py
│
├── services/             # Business logic separate from routes
│   ├── auth_service.py
│   ├── product_service.py
│   └── cart_service.py
│
├── routes/               # Flask API endpoints
│   ├── auth_routes.py
│   ├── product_routes.py
│   └── cart_routes.py
│
├── config.py             # Environment config (DB URI, JWT settings)
├── __init__.py           # App factory function
└── extensions.py         # Initialize SQLAlchemy, Migrate, JWT
```

---

## 4. PostgreSQL Docker Setup

```yaml
services:
  db:
    image: postgres:15
    container_name: ecommerce_postgres
    environment:
      POSTGRES_USER: zee
      POSTGRES_PASSWORD: Zcanucks83
      POSTGRES_DB: ecommerce_db
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

---

## 5. Flask Configuration

### Database URI (example)

```python
SQLALCHEMY_DATABASE_URI = 'postgresql://zee:Zcanucks83@localhost:5432/ecommerce_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

Use `@db` as the host if Flask is running in Docker too.

---

## 6. Database Migrations

Install and initialize:

```bash
pip install Flask-Migrate
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## 7. Services and Routes Example

**services/product_service.py**
```python
def get_all_products():
    return Product.query.all()
```

**routes/product_routes.py**
```python
from services.product_service import get_all_products

@product_bp.route("/", methods=["GET"])
def get_products():
    products = get_all_products()
    return jsonify([p.to_dict() for p in products])
```

---

## 8. Testing

- Use **pytest** for unit and integration tests
- Structure:
```
/tests
  ├── test_auth.py
  ├── test_products.py
  └── test_cart.py
```

---

## 9. Final Backend Structure Summary

```
/app
├── models/
├── services/
├── routes/
├── config.py
├── extensions.py
└── __init__.py

/tests
├── test_auth.py
├── test_products.py
└── test_cart.py

Dockerfile
docker-compose.yml
requirements.txt
```


---

## 10. Route Protection Overview

Route protection is enforced using JWT-based authentication. Admin-only routes require a valid token and admin privileges. Some routes are intentionally left open to support public access.

### 🔓 Public Routes (No Authentication Required)

| Method | Endpoint              | Description                 |
|--------|-----------------------|-----------------------------|
| POST   | /api/auth/signup      | User registration           |
| POST   | /api/auth/login       | User login                  |
| GET    | /api/products         | Public product listing      |

### 🔐 Protected Routes (User Authentication Required)

| Method | Endpoint                  | Description               |
|--------|---------------------------|---------------------------|
| GET    | /api/cart                 | View user's cart          |
| POST   | /api/cart/add             | Add item to cart          |
| POST   | /api/cart/remove          | Remove item from cart     |
| POST   | /api/payment/checkout     | Checkout via Stripe       |

### 🔐 Admin-Only Routes (Admin Auth Required)

| Method | Endpoint              | Description                    |
|--------|-----------------------|--------------------------------|
| POST   | /api/products         | Add a product                  |
| PUT    | /api/products/<id>    | Edit a product                 |
| DELETE | /api/products/<id>    | Delete a product               |

> Note: Admins can access both protected and public routes. Admin routes check for an "is_admin" claim in the JWT.

