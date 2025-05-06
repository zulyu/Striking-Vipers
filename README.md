# Striking Vipers

An educational game platform with teacher and student management.

## Features

- PyGame-based educational game
- REST API with Swagger documentation
- MySQL database integration
- User authentication
- Teacher and student management
- Class management

## Prerequisites

- Python 3.7+
- MySQL
- SDL2 libraries (for PyGame)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd striking-vipers
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

4. Set up the database:
```sql
CREATE DATABASE StrikingVipers;
```

5. Create a .env file with your configuration:
```
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://root:your-password@localhost/StrikingVipers
FLASK_ENV=development
FLASK_APP=run.py
```

## Running the Application

1. Start the Flask application:
```bash
python run.py
```

2. Access the Swagger documentation at:
```
http://localhost:5000/api/
```

## Running Tests

```bash
pytest app/tests/
```

## Deployment

The application can be deployed to AWS Elastic Beanstalk:

1. Install AWS CLI
2. Configure AWS credentials
3. Deploy using:
```bash
eb init -p python-3.7 striking-vipers
eb create striking-vipers-env
eb deploy
```

## License

This project is licensed under the MIT License.
