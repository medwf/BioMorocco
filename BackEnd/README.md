# Portfolio Project - Backend Development

This project is developed solely by [WAFI Mohamed](https://github.com/medwf).

## Project Overview

This project is the backend for my portfolio website. It is built using Flask, a lightweight WSGI web application framework in Python, and MySQL, a popular relational database management system.

## Features

- `RESTful API` endpoints for managing portfolio data
- User `authentication` and `authorization`
- `Sending emails` for user notifications (sign-up and password recovery, and new Orders and Low stock dedicated)
- `CRUD operations` for projects and other portfolio elements
- supports `images uploads` and organizes them efficiently.
- Integration with `MySQL` for persistent data storage
- `Redis` integration for storing session IDs and password recovery codes with Expiration.

## Technologies Used

- **Flask**: Python web framework
- **MySQL**: Relational database management system
- **SQLAlchemy**: ORM for database interactions
- **Flask-RESTful**: Extension for building REST APIs with Flask
- **Redis**: In-memory data structure store for session management
- **smtplib**: Python library for sending email.

## Setup and Installation

### Prerequisites

- Python 3.x
- MySQL
- Redis
- pip (Python package installer)

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/medwf/BioMorocco.git
   cd BioMorocco/BackEnd
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the MySQL database and Redis:**

   - Install Redis on your machine.
   - Install MySQL on your machine.
   - Refer to `BioMorocco/BackEnd/mysql/mysql-startup.sql` file.
   - To set up MySQL, run the following in the root directory of BackEnd:

   ```bash
   cat BackEnd/mysql/mysql-startup.sql | sudo mysql -u root
   ```

5. **Set up environment variables:**

   - Create a `.env` file in the root directory of your project:

     ```env
     API_HOST=localhost
     API_PORT=5000
     # add all other necessary environment variables
     ```

   - Load environment variables in your Python script:

     ```python
     from dotenv import load_dotenv
     import os

     load_dotenv()
     # Use os.getenv("name of env that you want")
     ```

6. **Run MySQL and Redis:**

   ```bash
   # Check status:
   sudo service mysql status # if not running
   sudo service redis status # if not running
   # Start or restart services:
   sudo service mysql start/restart
   sudo service redis start/restart
   ```

7. **Run the application:**

   ```bash
   ./run
   ```

   The application should now be running on `http://127.0.0.1:5000`.

## API Endpoints Documentation

The API endpoint Swagger documentation is available at [http://localhost:5000/api/docs](http://localhost:5000/api/docs).

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

## Contact

For any inquiries or issues, please contact [LinkedIn](https://www.linkedin.com/in/mohamed-wafi-a65277273/) or [Gmail](med.wf95@gmail.com).
