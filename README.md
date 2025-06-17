# E-Commerce-using-FastApi

This is a backend system for an e-commerce platform built using FastAPI, SQLAlchemy, and PostgreSQL. It includes user authentication, product management, cart functionality, orders, and checkout.

## Features

- User Authentication (Signup, Login, JWT Tokens)
- Role-based access (Admin & User)
- Product Management (Add/Edit/Delete/View products)
- Cart Management (Add/Update/Remove/View items)
- Order Management (View history, Order details)
- Checkout with stock validation and order creation
- Logging and input validation

## Project Structure
```bash
ECOM_FASTAPI/
│
├── alembic/                          # Alembic migrations folder
│
├── app/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   ├── services.py
│   │   └── utils.py
│   │
│   ├── cart/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── services.py
│   │
│   ├── checkout/
│   │   ├── __init__.py
│   │   └── routes.py          
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py              # DB engine/session setup
│   │   ├── exception_handler.py     # Custom exception handling
│   │   └── logger.py                # Logging config
│   │
│   ├── middlewares/
│   │   ├── __init__.py
│   │   └── dependencies.py                
│   │
│   ├── orders/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── services.py
│   │
│   ├── products/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── admin_routes.py
│   │   ├── public_routes.py
│   │   ├── schemas.py
│   │   └── services.py
│   │
│   └── main.py                      # FastAPI app entry point
│
├── env/                             # Environment config folder
│
├── logs/                            # Folder to store log files
│
├── .env                             # Environment variables 
├── .gitignore
├── alembic.ini                      # Alembic config file
├── LICENSE
├── README.md
└── requirements.txt                 # Python dependencies

```

## Installation

1. **Clone the repository**
   ```bash
    git clone https://github.com/mistborns/e-commerce-FastApi.git
    cd e-commerce-FastApi


2. **Create and activate virtual environment**
    ```bash
    python -m virtualenv env
    source env/bin/activate  # on Windows: .\env\Scripts\activate

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt

4. **Set up environment variables**

    create a .env file or configure app/core/config.py

5. **Run the app**
    ```bash
    uvicorn app.main:app --reload



## API Endpoints
Explore API using the built-in Swagger docs:
    http://localhost:8000/docs

Some example endpoints:

- POST /auth/signup — Register new user
- POST /auth/signin — Login user
- GET /products/ — List public products
- POST /cart/ — Add product to cart
- GET /orders/ — Get order history
- POST /checkout/ — Place an order