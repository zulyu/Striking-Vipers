import pytest
from app import create_app, db
from app.models import Teacher, Class as ClassModel, Student

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_teacher(client):
    response = client.post('/api/teachers', json={
        'name': 'John Doe',
        'email': 'jdoe@example.com',
        'subject': 'Computer Science'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'John Doe'
    assert data['email'] == 'jdoe@example.com'
    assert data['subject'] == 'Computer Science'

def test_create_class(client):
    # First create a teacher
    teacher = Teacher(
        name='John Doe',
        email='jdoe@example.com',
        subject='Computer Science'
    )
    db.session.add(teacher)
    db.session.commit()

    response = client.post('/api/classes', json={
        'id': 'CS101',
        'capacity': 30,
        'teacher_id': teacher.id
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] == 'CS101'
    assert data['capacity'] == 30

def test_create_student(client):
    # First create a teacher and class
    teacher = Teacher(
        name='John Doe',
        email='jdoe@example.com',
        subject='Computer Science'
    )
    db.session.add(teacher)
    db.session.commit()

    classroom = ClassModel(
        id='CS101',
        capacity=30,
        teacher_id=teacher.id
    )
    db.session.add(classroom)
    db.session.commit()

    response = client.post('/api/students', json={
        'name': 'Jane Smith',
        'email': 'jsmith@example.com',
        'grade': '10',
        'class_id': classroom.id
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Jane Smith'
    assert data['email'] == 'jsmith@example.com'
    assert data['grade'] == '10'

# Teacher Tests
def test_create_teacher_invalid_data(client):
    """Test creating a teacher with invalid data."""
    response = client.post("/api/teachers", json={
        "name": "",  # Invalid empty name
        "email": "invalid-email",  # Invalid email format
        "subject": ""  # Invalid empty subject
    })
    assert response.status_code == 400

def test_create_teacher_duplicate_email(client):
    """Test creating a teacher with duplicate email."""
    # Create first teacher
    client.post("/api/teachers", json={
        "name": "John Doe",
        "email": "jdoe@example.com",
        "subject": "Math"
    })
    
    # Try to create second teacher with same email
    response = client.post("/api/teachers", json={
        "name": "Jane Doe",
        "email": "jdoe@example.com",  # Same email
        "subject": "Science"
    })
    assert response.status_code == 400

def test_update_teacher_not_found(client):
    """Test updating a non-existent teacher."""
    response = client.put("/api/teachers/999", json={
        "name": "John Doe",
        "email": "jdoe@example.com",
        "subject": "Math"
    })
    assert response.status_code == 404

# Class Tests
def test_create_class_invalid_teacher(client):
    """Test creating a class with non-existent teacher."""
    response = client.post("/api/classes", json={
        "id": "CS101",
        "capacity": 30,
        "teacher_id": 999  # Non-existent teacher
    })
    assert response.status_code == 400

def test_create_class_invalid_capacity(client):
    """Test creating a class with invalid capacity."""
    # First create a teacher
    teacher_response = client.post("/api/teachers", json={
        "name": "John Doe",
        "email": "jdoe@example.com",
        "subject": "Math"
    })
    teacher_id = teacher_response.get_json()["id"]

    response = client.post("/api/classes", json={
        "id": "CS101",
        "capacity": -1,  # Invalid negative capacity
        "teacher_id": teacher_id
    })
    assert response.status_code == 400

def test_create_class_duplicate_id(client):
    """Test creating a class with duplicate ID."""
    # First create a teacher
    teacher_response = client.post("/api/teachers", json={
        "name": "John Doe",
        "email": "jdoe@example.com",
        "subject": "Math"
    })
    teacher_id = teacher_response.get_json()["id"]

    # Create first class
    client.post("/api/classes", json={
        "id": "CS101",
        "capacity": 30,
        "teacher_id": teacher_id
    })

    # Try to create second class with same ID
    response = client.post("/api/classes", json={
        "id": "CS101",  # Same ID
        "capacity": 25,
        "teacher_id": teacher_id
    })
    assert response.status_code == 400

# Student Tests
def test_create_student_invalid_class(client):
    """Test creating a student with non-existent class."""
    response = client.post("/api/students", json={
        "name": "Jane Smith",
        "email": "jsmith@example.com",
        "grade": "10",
        "class_id": "NONEXISTENT"  # Non-existent class
    })
    assert response.status_code == 400

def test_create_student_duplicate_email(client):
    """Test creating a student with duplicate email."""
    # First create required teacher and class
    teacher_response = client.post("/api/teachers", json={
        "name": "John Doe",
        "email": "jdoe@example.com",
        "subject": "Math"
    })
    teacher_id = teacher_response.get_json()["id"]

    class_response = client.post("/api/classes", json={
        "id": "CS101",
        "capacity": 30,
        "teacher_id": teacher_id
    })
    class_id = class_response.get_json()["id"]

    # Create first student
    client.post("/api/students", json={
        "name": "Jane Smith",
        "email": "jsmith@example.com",
        "grade": "10",
        "class_id": class_id
    })

    # Try to create second student with same email
    response = client.post("/api/students", json={
        "name": "John Smith",
        "email": "jsmith@example.com",  # Same email
        "grade": "11",
        "class_id": class_id
    })
    assert response.status_code == 400

def test_class_at_capacity(client):
    """Test adding a student to a full class."""
    # First create required teacher and class
    teacher_response = client.post("/api/teachers", json={
        "name": "John Doe",
        "email": "jdoe@example.com",
        "subject": "Math"
    })
    teacher_id = teacher_response.get_json()["id"]

    # Create class with capacity 1
    class_response = client.post("/api/classes", json={
        "id": "CS101",
        "capacity": 1,  # Only one student allowed
        "teacher_id": teacher_id
    })
    class_id = class_response.get_json()["id"]

    # Add first student (should succeed)
    client.post("/api/students", json={
        "name": "Jane Smith",
        "email": "jsmith@example.com",
        "grade": "10",
        "class_id": class_id
    })

    # Try to add second student (should fail)
    response = client.post("/api/students", json={
        "name": "John Smith",
        "email": "john@example.com",
        "grade": "10",
        "class_id": class_id
    })
    assert response.status_code == 400

def test_invalid_grade(client):
    """Test creating a student with invalid grade."""
    # First create required teacher and class
    teacher_response = client.post("/api/teachers", json={
        "name": "John Doe",
        "email": "jdoe@example.com",
        "subject": "Math"
    })
    teacher_id = teacher_response.get_json()["id"]

    class_response = client.post("/api/classes", json={
        "id": "CS101",
        "capacity": 30,
        "teacher_id": teacher_id
    })
    class_id = class_response.get_json()["id"]

    response = client.post("/api/students", json={
        "name": "Jane Smith",
        "email": "jsmith@example.com",
        "grade": "13",  # Invalid grade (assuming grades are 1-12)
        "class_id": class_id
    })
    assert response.status_code == 400 