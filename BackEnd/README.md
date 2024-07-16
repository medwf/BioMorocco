# Portfolio Project - Backend Development

This project is developed solely by [WAFI Mohamed](https://github.com/medwf).

## Project Overview

This project is the backend for my portfolio website. It is built using Flask, a lightweight WSGI web application framework in Python, and MySQL, a popular relational database management system.

## Features

- `RESTful API` endpoints for managing portfolio data
- User `authentication` and `authorization`
- `Sending emails` for user notifications (sign-up and password recovery, and new Orders and Low stock dedicated)
- `CRUD operations` for projects and other portfolio elements
- Use `JSON` to store a list of image paths as a string in the database. This allows for easy storage and retrieval of multiple image references associated with various objects.
- Integration with `MySQL` for persistent data storage
- `Redis` integration for storing session IDs and password recovery codes with Expiration.
- Containerization with `Docker` for easy deployment
- Multi-container management with `Docker-Compose` for development and testing

## Technologies Used

- **Flask**: Python web framework
- **MySQL**: Relational database management system
- **SQLAlchemy**: ORM for database interactions
- **Flask-RESTful**: Extension for building REST APIs with Flask
- **Redis**: In-memory data structure store for session management
- **smtplib**: Python library for sending email
- **Docker**: Containerization platform
- **Docker-Compose**: Tool for defining and running multi-container Docker applications

## Setup and Installation

### Prerequisites

- Python 3.x
- Docker and Docker-Compose

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/medwf/BioMorocco.git
   cd BioMorocco
   ```

2. **Set up environment variables:**

   - Create a `.env` file in the root directory with the following content:

     ```env
     # just a example.

     FLASK_ENV=development
     MYSQL_HOST=db
     MYSQL_USER=USER
     MYSQL_PASSWORD=USER2024
     MYSQL_DB=DB
     REDIS_HOST=redis
     REDIS_PORT=6379
     ```

3. **Build and Start the Containers:**

   - go back to the route repo.
   - Run the following command to build and start all services:

     ```bash
     docker-compose up --build
     ```

   - This command will:
     - Build the Flask backend application.
     - Start the MySQL database with the specified user and database.
     - Start the Redis server.

4. **Accessing the Application:**

   - Once all services are up and running, the Flask application will be accessible at `http://localhost:5000`.
   - MySQL will be running on port `3306` and Redis on port `6379`.

5. **Managing Containers:**

   - To stop the containers, run:

     ```bash
     # for stop container
     docker-compose stop

     # to delete all container
     docker-compose down
     ```

   - To rebuild and start the containers, run:

     ```bash
     # rebuild container.
     docker-compose up --build

     # for starting container after stop.
     docker-compose start
     ```

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

For any inquiries or issues, please contact [LinkedIn](https://www.linkedin.com/in/mohamed-wafi-a65277273/) or [Gmail](mailto:med.wf95@gmail.com).
