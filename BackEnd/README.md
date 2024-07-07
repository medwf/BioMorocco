# Portfolio Project - Backend Development

This project is developed solely by [WAFI Mohamed](https://github.com/medwf).

## Project Overview

This project is the backend for my portfolio website. It is built using Flask, a lightweight WSGI web application framework in Python, and MySQL, a popular relational database management system.

## Features

- RESTful API endpoints for managing portfolio data
- User authentication and authorization
- CRUD operations for projects and other portfolio elements
- Integration with MySQL for persistent data storage

## Technologies Used

- **Flask**: Python web framework
- **MySQL**: Relational database management system
- **SQLAlchemy**: ORM for database interactions
- **Flask-RESTful**: Extension for building REST APIs with Flask

## Setup and Installation

### Prerequisites

- Python 3.x
- MySQL
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

4. **Set up the MySQL database:**

   - Install MySQL on your machine.
   - look at `BioMorocco/BackEnd/mysql/mysql-startup.sql` file
   - to setup Mysql just run in root directory of BackEnd

   ```bash
   cat BackEnd/mysql/mysql-startup.sql | sudo mysql -u root
   ```

5. **environment variables:**

   store it in run file

   ```Bash
   # just run console to test models.
   ./run <api or console>
   ```

6. **Run Mysql database:**

   ```bash
   # check status by
   sudo service mysql status # if not running
   # do
   sudo service mysql start/restart
   ```

7. **Run the application:**

   ```bash
   ./run api
   ```

   The application should now be running on `http://127.0.0.1:5000`.

## API Endpoints

**index :**

`PATHs` that is accessible to anyone.

- GET `/`: Say welcome to api.
- GET `/status`: status of our api and some information.
- GET `/stats`: count all tables.
- GET `/categories`: get all categories
- GET `/products`: get all products

**User :**

`PATHs` that is accessible to anyone.

- GET `/signUp`: create new User.
- POST `/login`: log in user based on email and password. create session

To access to `PATHs`, authentication is required.

- GET `/profile`: get data user
- PUT `/users`: update user data. password not included
- DELETE `/logout`: log out user based on cookies session
- DELETE `/users`: delete all user account
- POST `/reset_password`: change password based on old one

## License

This project is licensed under the MIT License.

## Contact

For any inquiries or issues, please contact [linkedin](https://www.linkedin.com/in/mohamed-wafi-a65277273/) or [Gmail](med.wf95@gmail.com).
