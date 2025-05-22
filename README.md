# Striking Vipers

An educational game platform to teach students the fundamentals of programmking in Python.

## Features

- PyGame-based educational game
- Browser-compatible HTML/JavaScript version
- REST API with Swagger documentation
- SQLite database integration
- User authentication

## Installation and Setup

1. Unzip the files to a directory
2. Change into the root directory

3. Create a Python virtual environment:
```bash
python3.10 -m venv venv_py310
```

4. Activate the virtual environment:
```bash
source venv_py310/bin/activate
```

5. Install dependencies:
```bash
pip install -r requirements.txt
```

6. Initialize the database with sample data:
```bash
python init_db.py
```

## Running the Application

1. Start the Flask application:
```bash
python3.10 run.py
```

2. Access the Swagger API documentation at:
```
http://localhost:5002/api/
```


## Accessing the Log In Screen
'''
http://localhost:5002/login.html
'''

## Accessing the Game
'''
http://localhost:5002/game.html
'''

### Online AWS Web Version
The game is deployed at:
```
http://striking-vipers-game-2024.s3-website-us-east-1.amazonaws.com/login.html
```

### Test Account Credentials
Use these credentials to log in:
- Email: test@example.com
- Username: testuser
- Password: password123
- Class Code: CS101

## Running Tests

To successfully run the tests, follow these steps:

1. Make sure you're in your Python 3.10 environment:
```bash
source venv_py310/bin/activate
```

2. Add the current directory to your Python path:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

3. Run the tests:
```bash
pytest tests/unit/ tests/integration/
```

OR 

```bash
pytest
```


## Troubleshooting

### MacOS Security Warning
If you get an error about "library load disallowed by system policy" related to rpds or any other library:

```bash
# Run this command to remove the quarantine attribute
xattr -d com.apple.quarantine venv_py310/lib/python3.10/site-packages/rpds/rpds.cpython-310-darwin.so
```

### Missing JWT Module
If you get an error "No module named 'jwt'", install PyJWT:

```bash
pip install PyJWT
```

### Missing Flask-Cors Module
If you get an error "No module named 'flask_cors'", install Flask-Cors:

```bash
pip install Flask-Cors
```