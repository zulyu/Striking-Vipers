import pytest
from app import create_app, db
from app.models import Teacher, Class, Student

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
    response = client.post('/api/api/teachers', json={
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

    response = client.post('/api/api/classes', json={
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

    classroom = Class(
        id='CS101',
        capacity=30,
        teacher_id=teacher.id
    )
    db.session.add(classroom)
    db.session.commit()

    response = client.post('/api/api/students', json={
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