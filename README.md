# 🧵 Clothing E-Commerce Backend

A Flask-based backend for a clothing e-commerce application with user authentication, product management, and cart functionality.

## Features

- User authentication (signup/login)
- Product management (CRUD operations)
- Shopping cart functionality
- Admin role for product management
- PostgreSQL database
- JWT-based authentication

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- PostgreSQL (via Docker)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the PostgreSQL database:
```bash
docker-compose up -d
```

5. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Run the application:
```bash
flask run
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register a new user
- `POST /api/auth/login` - Login and get JWT token

### Products
- `GET /api/products` - Get all products
- `GET /api/products/<id>` - Get a specific product
- `POST /api/products` - Create a new product (Admin only)
- `PUT /api/products/<id>` - Update a product (Admin only)
- `DELETE /api/products/<id>` - Delete a product (Admin only)

### Cart
- `GET /api/cart` - Get user's cart
- `POST /api/cart/add` - Add item to cart
- `POST /api/cart/remove` - Remove item from cart
- `PUT /api/cart/update` - Update cart item quantity
- `POST /api/cart/clear` - Clear the cart

## Environment Variables

Create a `.env` file in the root directory with the following variables:
```
DATABASE_URL=postgresql://zee:Zcanucks83@localhost:5432/ecommerce_db
JWT_SECRET_KEY=your-secret-key-here
```

## Testing

Run tests using pytest:
```bash
pytest
```

## TODO

- Implement Stripe payment integration
- Add more comprehensive error handling
- Add request rate limiting
- Add API documentation
- Add more test cases 