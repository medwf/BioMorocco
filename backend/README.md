# Portfolio Project - Backend Development

## Project Overview

This project is the backend for my portfolio website. It is built using Flask, a lightweight WSGI web application framework in Python, and MySQL, a popular relational database management system.

## API Endpoints Documentation

The API endpoint Swagger documentation is available at [http://localhost:5000/api/v1/docs](http://localhost:5000/api/v1/docs).

## API Endpoints

### Public Endpoints

- **Index:**
  - GET `/`: Welcome to the API.
  - GET `/status`: API status and information.
  - GET `/stats`: Count of all tables.

### Authentication

- **Public:**

  - GET `/api/v1/signUp`: Create a new user.
  - POST `/api/v1/login`: Log in a user based on email and password. Creates a session.
  - POST `/api/v1/forget_password`: Generate a code sent via email to recover password (2-minute expiration).
  - PUT `/api/v1/forget_password`: Set a new password based on the code sent via email.

- **Authenticated:**
  - DELETE `/api/v1/logout`: Log out a user based on session cookies.

### User Management

- **Authenticated:**
  - GET `/api/v1/profile`: Retrieve user data.
  - PUT `/api/v1/users`: Update user data (password not included).
  - POST `/api/v1/reset_password`: Change password based on the old one.
  - DELETE `/api/v1/users`: Delete user account.

### Store Management

- **Public:**

  - GET `/api/v1/store`: Retrieve store data.

- **Authenticated:**
  - PUT `/api/v1/store`: Update store data.
  - POST `/api/v1/store`: Create a new store.
  - DELETE `/api/v1/store`: Delete store.

### Categories

- **Public:**

  - GET `/api/v1/categories`: Retrieve categories data.
  - GET `/api/v1/categories/<id>`: Retrieve category data by ID.

- **Authenticated:**

  - PUT `/api/v1/categories/<id>`: Update category data.
  - POST `/api/v1/categories`: Create new categories.
  - DELETE `/api/v1/categories/<id>`: Delete categories.

### Products

- **Public:**

  - GET `/api/v1/products`: Retrieve products data.
  - GET `/api/v1/products/<id>`: Retrieve product data by ID.

- **Authenticated:**
  - PUT `/api/v1/products/<id>`: Update product data.
  - POST `/api/v1/categories/<category_id>/products`: Create new products.
  - DELETE `/api/v1/products/<id>`: Delete products.

### Cart Items

- **Authenticated:**
  - GET `/api/v1/cartItems`: Retrieve cart items data.
  - PUT `/api/v1/cartItems/<id>`: Update cart items data.
  - POST `/api/v1/products/<product_id>/cartItems`: Add new cart items.
  - DELETE `/api/v1/cartItems/<id>`: Delete cart items.

### Reviews

- **Public:**

  - GET `/products/<int:product_id>/reviews`: Retrieve reviews data.
  - GET `/products/<int:product_id>/reviews/<int:review_id>`: Retrieve review data by ID.

- **Authenticated:**
  - PUT `/api/v1/reviews/<id>`: Update reviews data.
  - POST `/products/<int:product_id>/reviews`: Add new reviews.
  - DELETE `/api/v1/reviews/<id>`: Delete reviews.

### Orders

- **Authenticated:**
  - GET `/product/<int:product_id>/orders`: Retrieve orders by product ID.
  - GET `/users/orders`: Retrieve orders by user ID.
  - POST `/product/<int:product_id>/orders`: Add a new order. add sending Email: (New Orders `all details need` and Low stock dedicated)
  - POST `/users/orders`: Add a new order. add sending Email: (New Orders `all details need` and Low stock dedicated)

## License

This project is licensed under the MIT License.
