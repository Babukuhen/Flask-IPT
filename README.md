---

# Employee Management API

This is a Flask-based RESTful API for managing employees and their departments.

## Features

- **Authentication**: Uses JWT (JSON Web Tokens) for user authentication.
- **CRUD Operations**: Supports basic CRUD operations for employees and departments.
- **Data Formats**: Provides support for both JSON and XML data formats.
- **Unit Testing**: Includes unit tests to ensure the functionality of the API endpoints.

## Prerequisites

- Python 3.x
- Flask
- Flask-MySQLDB
- PyJWT
- Dicttoxml

## Installation

1. Clone this repository:

    ```bash
    git clone <repository_url>
    ```

2. Install the required dependencies:

    ```bash
    pip install Flask Flask-MySQLDB PyJWT dicttoxml
    ```

3. Set up MySQL database:
   
    - Create a database named `emp_dep_db`.
    - Set your MySQL username and password in `api.py`:
    
        ```python
        app.config["MYSQL_USER"] = "root"
        app.config["MYSQL_PASSWORD"] = "your_password_here"
        ```

4. Optionally, adjust token lock settings:

    - To disable token requirement, set `token_lock` to `False` in `api.py`:
    
        ```python
        token_lock = False
        ```

5. Run the Flask application:

    ```bash
    python api.py
    ```

## API Endpoints

### Authentication

- `POST /login`: Authenticates users and generates JWT token.

### Employees

- `GET /employee`: Retrieves all employees.
- `GET /employee/<int:id>`: Retrieves an employee by ID.
- `GET /employee/<int:id>/department`: Retrieves department location by employee ID.
- `POST /employee`: Adds a new employee.
- `PUT /employee/<int:id>`: Updates an existing employee.
- `DELETE /employee/<int:id>`: Deletes an employee.

### Department

- No direct endpoints for department operations are provided in this implementation.

### Search

- `GET /search`: Renders a search form for employees.
- `GET /search/results`: Retrieves search results based on provided criteria.

### Example Route with Token Requirement

To access routes that require authentication, users must include the JWT token in the request headers. For example:

```http
GET /employee?token=<your_jwt_token_here>
```


## Testing

Before running the unit tests, make sure you are in an environment where you have installed the dependencies and that the API is running. You can activate the virtual environment by navigating to the project directory and running:

```bash
<venv_name>\Scripts\activate
```

Replace `<venv_name>` with the name of your virtual environment directory.

Once the virtual environment is activated and the API is running, you can run the unit tests:

```bash
python tests.py
```

**Note:** Testing currently does not take into account the token requirement. Make sure to disable token requirement to test properly. You can modify the `token_required` decorator or adjust the test cases accordingly.


## Additional Notes

- The `login.html`, `search.html`, and `search_results.html` files are provided for frontend views and form submissions.

---