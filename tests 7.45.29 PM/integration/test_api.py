import pytest
from app import create_app, db
from app.models import Teacher, Class as ClassModel, Student
import jwt
from datetime import datetime, timedelta

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def auth_headers():
    """Create authentication headers for testing."""
    def _create_headers(user_id, role):
        token = jwt.encode({
            'user_id': user_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, 'your-secret-key', algorithm='HS256')
        return {'Authorization': f'Bearer {token}'}
    return _create_headers

def test_create_teacher(client, auth_headers):
    """Test creating a new teacher."""
    # First create a teacher to get an ID for auth
    teacher = Teacher(
        name='Admin Teacher',
        email='admin@example.com',
        subject='Admin'
    )
    teacher.set_password('password123')
    db.session.add(teacher)
    db.session.commit()

    headers = auth_headers(teacher.id, 'teacher')
    response = client.post('/api/teachers', json={
        'name': 'John Doe',
        'email': 'jdoe@example.com',
        'subject': 'Computer Science'
    }, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['email'] == 'jdoe@example.com'

def test_create_class(client, auth_headers):
    """Test creating a new class."""
    # First create a teacher
    teacher = Teacher(
        name='John Doe',
        email='jdoe@example.com',
        subject='Computer Science'
    )
    teacher.set_password('password123')
    db.session.add(teacher)
    db.session.commit()

    headers = auth_headers(teacher.id, 'teacher')
    response = client.post('/api/classes', json={
        'id': 'CS101',
        'capacity': 30,
        'teacher_id': teacher.id
    }, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] == 'CS101'

def test_create_student(client, auth_headers):
    """Test creating a new student."""
    # First create a teacher and class
    teacher = Teacher(
        name='John Doe',
        email='jdoe@example.com',
        subject='Computer Science'
    )
    teacher.set_password('password123')
    db.session.add(teacher)
    db.session.commit()

    classroom = ClassModel(
        id='CS101',
        capacity=30,
        teacher_id=teacher.id
    )
    db.session.add(classroom)
    db.session.commit()

    headers = auth_headers(teacher.id, 'teacher')
    response = client.post('/api/students', json={
        'name': 'Jane Smith',
        'email': 'jsmith@example.com',
        'grade': '10',
        'class_id': classroom.id
    }, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['email'] == 'jsmith@example.com'

def test_create_teacher_invalid_data(client, auth_headers):
    """Test creating a teacher with invalid data."""
    # First create a teacher to get an ID for auth
    teacher = Teacher(
        name='Admin Teacher',
        email='admin@example.com',
        subject='Admin'
    )
    teacher.set_password('password123')
    db.session.add(teacher)
    db.session.commit()

    headers = auth_headers(teacher.id, 'teacher')
    response = client.post("/api/teachers", json={
        "name": "",  # Invalid empty name
        "email": "invalid-email",  # Invalid email format
        "subject": ""  # Invalid empty subject
    }, headers=headers)
    assert response.status_code == 400

def test_create_teacher_duplicate_email(client, auth_headers):
    """Test creating a teacher with duplicate email."""
    # First create a teacher to get an ID for auth
    teacher = Teacher(
        name='Admin Teacher',
        email='admin@example.com',
        subject='Admin'
    )
    teacher.set_password('password123')
    db.session.add(teacher)
    db.session.commit()

    headers = auth_headers(teacher.id, 'teacher')
    # Create first teacher
    client.post("/api/teachers", json={
        "name": "John Doe",
        "email": "jdoe@example.com",
        "subject": "Math"
    }, headers=headers)

    # Try to create second teacher with same email
    response = client.post("/api/teachers", json={
        "name": "Jane Doe",
        "email": "jdoe@example.com",  # Same email
        "subject": "Science"
    }, headers=headers)
    assert response.status_code == 400

def test_update_teacher_not_found(client, auth_headers):
    """Test updating a non-existent teacher."""
    # First create a teacher to get an ID for auth
    teacher = Teacher(
        name='Admin Teacher',
        email='admin@example.com',
        subject='Admin'
    )
    teacher.set_password('password123')
    db.session.add(teacher)
    db.session.commit()

    headers = auth_headers(teacher.id, 'teacher')
    response = client.put("/api/teachers/999", json={
        "name": "John Doe",
        "email": "jdoe@example.com",
        "subject": "Math"
    }, headers=headers)
    assert response.status_code == 404

def test_create_class_invalid_teacher(client, auth_headers):
    """Test creating a class with non-existent teacher."""
    # First create a teacher to get an ID for auth
    teacher = Teacher(
        name='Admin Teacher',
        email='admin@example.com',
        subject='Admin'
    )
    teacher.set_password('password123')
    db.session.add(teacher)
    db.session.commit()

    headers = auth_headers(teacher.id, 'teacher')
    response = client.post("/api/classes", json={
        "id": "CS101",
        "capacity": 30,
        "teacher_id": 999  # Non-existent teacher
    }, headers=headers)
    assert response.status_code == 400

def test_create_class_invalid_capacity(client, auth_headers):
    """Test creating a class with invalid capacity."""
    # First create a teacher to get an ID for auth
    teacher = Teacher(
        name='Admin Teacher',
        email='admin@example.com',
        subject='Admin'
    )
    teacher.set_password('password123')
    db.session.add(teacher)
    db.session.commit()

    headers = auth_headers(teacher.id, 'teacher')
    response = client.post("/api/classes", json={
        "id": "CS101",
        "capacity": -1,  # Invalid capacity
        "teacher_id": teacher.id
    }, headers=headers)
    assert response.status_code == 400

def test_create_class_duplicate_id(client, auth_headers):
    """Test creating a class with duplicate ID."""
    # First create a teacher to get an ID for auth
    teacher = Teacher(
        name='Admin Teacher',
        email='admin@example.com',
        subject='Admin'
    )
    teacher.set_password('password123')
    db.session.add(teacher)
    db.session.commit()

    headers = auth_headers(teacher.id, 'teacher')
    # Create first class
    client.post("/api/classes", json={
        "id": "CS101",
        "capacity": 30,
        "teacher_id": teacher.id
    }, headers=headers)

    # Try to create second class with same ID
    response = client.post("/api/classes", json={
        "id": "CS101",  # Same ID
        "capacity": 25,
        "teacher_id": teacher.id
    }, headers=headers)
    assert response.status_code == 400

def test_create_student_invalid_class(client, auth_headers):
    """Test creating a student with non-existent class."""
    # First create a teacher to get an ID for auth
    teacher = Teacher(
        name='Admin Teacher',
        email='admin@example.com',
        subject='Admin'
    )
    teacher.set_password('password123')
    db.session.add(teacher)
    db.session.commit()

    headers = auth_headers(teacher.id, 'teacher')
    response = client.post("/api/students", json={
        "name": "Jane Smith",
        "email": "jsmith@example.com",
        "grade": "10",
        "class_id": "NONEXISTENT"  # Non-existent class
    }, headers=headers)
    assert response.status_code == 400

def test_create_student_duplicate_email(client, auth_headers):
    """Test creating a student with duplicate email."""
    # First create a teacher and class
    teacher = Teacher(
        name='Admin Teacher',
        email='admin@example.com',
        subject='Admin'
    )
    teacher.set_password('password123')
    db.session.add(teacher)
    db.session.commit()

    classroom = ClassModel(
        id='CS101',
        capacity=30,
        teacher_id=teacher.id
    )
    db.session.add(classroom)
    db.session.commit()

    headers = auth_headers(teacher.id, 'teacher')
    # Create first student
    client.post("/api/students", json={
        "name": "John Smith",
        "email": "jsmith@example.com",
        "grade": "10",
        "class_id": classroom.id
    }, headers=headers)

    # Try to create second student with same email
    response = client.post("/api/students", json={
        "name": "Jane Smith",
        "email": "jsmith@example.com",  # Same email
        "grade": "11",
        "class_id": classroom.id
    }, headers=headers)
    assert response.status_code == 400

def test_class_at_capacity(client, auth_headers):
    """Test adding a student to a full class."""
    # First create a teacher and class
    teacher = Teacher(
        name='Admin Teacher',
        email='admin@example.com',
        subject='Admin'
    )
    teacher.set_password('password123')
    db.session.add(teacher)
    db.session.commit()

    classroom = ClassModel(
        id='CS101',
        capacity=2,  # Small capacity for testing
        teacher_id=teacher.id
    )
    db.session.add(classroom)
    db.session.commit()

    headers = auth_headers(teacher.id, 'teacher')
    # Fill the class
    for i in range(2):
        client.post("/api/students", json={
            "name": f"Student {i}",
            "email": f"student{i}@example.com",
            "grade": "10",
            "class_id": classroom.id
        }, headers=headers)

    # Try to add one more student
    response = client.post("/api/students", json={
        "name": "Extra Student",
        "email": "extra@example.com",
        "grade": "10",
        "class_id": classroom.id
    }, headers=headers)
    assert response.status_code == 400
    assert "Class is at capacity" in response.get_json()["message"]

def test_invalid_grade(client, auth_headers):
    """Test creating a student with invalid grade."""
    # First create a teacher and class
    teacher = Teacher(
        name='Admin Teacher',
        email='admin@example.com',
        subject='Admin'
    )
    teacher.set_password('password123')
    db.session.add(teacher)
    db.session.commit()

    classroom = ClassModel(
        id='CS101',
        capacity=30,
        teacher_id=teacher.id
    )
    db.session.add(classroom)
    db.session.commit()

    headers = auth_headers(teacher.id, 'teacher')
    response = client.post("/api/students", json={
        "name": "Jane Smith",
        "email": "jsmith@example.com",
        "grade": "13",  # Invalid grade
        "class_id": classroom.id
    }, headers=headers)
    assert response.status_code == 400
    assert "Grade must be between 1 and 12" in response.get_json()["message"] 