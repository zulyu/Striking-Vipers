import pytest
from app import create_app, db
from app.database.models import Teacher, Class, Student


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_teacher():
    return {
        "name": "John Doe",
        "email": "jdoe@example.com",
        "subject": "Computer Science"
    }


@pytest.fixture
def sample_class():
    return {
        "id": "CS101",
        "capacity": 30,
        "teacher_id": 1
    }


@pytest.fixture
def sample_student():
    return {
        "name": "Jane Smith",
        "email": "jsmith@example.com",
        "grade": "10",
        "class_id": "CS101"
    }


# Teacher Tests
def test_create_teacher(client, sample_teacher):
    response = client.post("/api/teachers", json=sample_teacher)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == sample_teacher["name"]
    assert data["email"] == sample_teacher["email"]
    assert data["subject"] == sample_teacher["subject"]
    assert "links" in data


def test_get_teacher(client, sample_teacher):
    # First create a teacher
    response = client.post("/api/teachers", json=sample_teacher)
    teacher_id = response.get_json()["id"]

    # Then get the teacher
    response = client.get(f"/api/teachers/{teacher_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == sample_teacher["name"]
    assert "links" in data


def test_update_teacher(client, sample_teacher):
    # First create a teacher
    response = client.post("/api/teachers", json=sample_teacher)
    teacher_id = response.get_json()["id"]

    # Update the teacher
    updated_data = {
        "name": "John Updated",
        "email": "updated@example.com",
        "subject": "Updated Subject"
    }
    response = client.put(f"/api/teachers/{teacher_id}", json=updated_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == updated_data["name"]
    assert data["email"] == updated_data["email"]
    assert data["subject"] == updated_data["subject"]


def test_delete_teacher(client, sample_teacher):
    # First create a teacher
    response = client.post("/api/teachers", json=sample_teacher)
    teacher_id = response.get_json()["id"]

    # Delete the teacher
    response = client.delete(f"/api/teachers/{teacher_id}")
    assert response.status_code == 204

    # Verify teacher is deleted
    response = client.get(f"/api/teachers/{teacher_id}")
    assert response.status_code == 404


# Class Tests
def test_create_class(client, sample_teacher, sample_class):
    # First create a teacher
    teacher_response = client.post("/api/teachers", json=sample_teacher)
    sample_class["teacher_id"] = teacher_response.get_json()["id"]

    # Create a class
    response = client.post("/api/classes", json=sample_class)
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == sample_class["id"]
    assert data["capacity"] == sample_class["capacity"]
    assert "links" in data


def test_get_class(client, sample_teacher, sample_class):
    # First create a teacher and class
    teacher_response = client.post("/api/teachers", json=sample_teacher)
    sample_class["teacher_id"] = teacher_response.get_json()["id"]
    class_response = client.post("/api/classes", json=sample_class)
    class_id = class_response.get_json()["id"]

    # Get the class
    response = client.get(f"/api/classes/{class_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == sample_class["id"]
    assert "links" in data


def test_update_class(client, sample_teacher, sample_class):
    # First create a teacher and class
    teacher_response = client.post("/api/teachers", json=sample_teacher)
    sample_class["teacher_id"] = teacher_response.get_json()["id"]
    class_response = client.post("/api/classes", json=sample_class)
    class_id = class_response.get_json()["id"]

    # Update the class
    updated_data = {
        "id": "CS102",
        "capacity": 40,
        "teacher_id": sample_class["teacher_id"]
    }
    response = client.put(f"/api/classes/{class_id}", json=updated_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["capacity"] == updated_data["capacity"]


def test_delete_class(client, sample_teacher, sample_class):
    # First create a teacher and class
    teacher_response = client.post("/api/teachers", json=sample_teacher)
    sample_class["teacher_id"] = teacher_response.get_json()["id"]
    class_response = client.post("/api/classes", json=sample_class)
    class_id = class_response.get_json()["id"]

    # Delete the class
    response = client.delete(f"/api/classes/{class_id}")
    assert response.status_code == 204

    # Verify class is deleted
    response = client.get(f"/api/classes/{class_id}")
    assert response.status_code == 404


# Student Tests
def test_create_student(client, sample_teacher, sample_class, sample_student):
    # First create a teacher and class
    teacher_response = client.post("/api/teachers", json=sample_teacher)
    sample_class["teacher_id"] = teacher_response.get_json()["id"]
    class_response = client.post("/api/classes", json=sample_class)
    sample_student["class_id"] = class_response.get_json()["id"]

    # Create a student
    response = client.post("/api/students", json=sample_student)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == sample_student["name"]
    assert data["email"] == sample_student["email"]
    assert "links" in data


def test_get_student(client, sample_teacher, sample_class, sample_student):
    # First create a teacher, class, and student
    teacher_response = client.post("/api/teachers", json=sample_teacher)
    sample_class["teacher_id"] = teacher_response.get_json()["id"]
    class_response = client.post("/api/classes", json=sample_class)
    sample_student["class_id"] = class_response.get_json()["id"]
    student_response = client.post("/api/students", json=sample_student)
    student_id = student_response.get_json()["id"]

    # Get the student
    response = client.get(f"/api/students/{student_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == sample_student["name"]
    assert "links" in data


def test_update_student(client, sample_teacher, sample_class, sample_student):
    # First create a teacher, class, and student
    teacher_response = client.post("/api/teachers", json=sample_teacher)
    sample_class["teacher_id"] = teacher_response.get_json()["id"]
    class_response = client.post("/api/classes", json=sample_class)
    sample_student["class_id"] = class_response.get_json()["id"]
    student_response = client.post("/api/students", json=sample_student)
    student_id = student_response.get_json()["id"]

    # Update the student
    updated_data = {
        "name": "Jane Updated",
        "email": "updated@example.com",
        "grade": "11",
        "class_id": sample_student["class_id"]
    }
    response = client.put(f"/api/students/{student_id}", json=updated_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == updated_data["name"]
    assert data["email"] == updated_data["email"]


def test_delete_student(client, sample_teacher, sample_class, sample_student):
    # First create a teacher, class, and student
    teacher_response = client.post("/api/teachers", json=sample_teacher)
    sample_class["teacher_id"] = teacher_response.get_json()["id"]
    class_response = client.post("/api/classes", json=sample_class)
    sample_student["class_id"] = class_response.get_json()["id"]
    student_response = client.post("/api/students", json=sample_student)
    student_id = student_response.get_json()["id"]

    # Delete the student
    response = client.delete(f"/api/students/{student_id}")
    assert response.status_code == 204

    # Verify student is deleted
    response = client.get(f"/api/students/{student_id}")
    assert response.status_code == 404


# List Tests
def test_list_teachers(client, sample_teacher):
    # Create multiple teachers
    for i in range(3):
        teacher_data = sample_teacher.copy()
        teacher_data["email"] = f"teacher{i}@example.com"
        client.post("/api/teachers", json=teacher_data)

    # Get all teachers
    response = client.get("/api/teachers")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 3
    for teacher in data:
        assert "links" in teacher


def test_list_classes(client, sample_teacher, sample_class):
    # Create a teacher
    teacher_response = client.post("/api/teachers", json=sample_teacher)
    teacher_id = teacher_response.get_json()["id"]

    # Create multiple classes
    for i in range(3):
        class_data = sample_class.copy()
        class_data["id"] = f"CS10{i}"
        class_data["teacher_id"] = teacher_id
        client.post("/api/classes", json=class_data)

    # Get all classes
    response = client.get("/api/classes")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 3
    for class_obj in data:
        assert "links" in class_obj


def test_list_students(client, sample_teacher, sample_class, sample_student):
    # Create a teacher and class
    teacher_response = client.post("/api/teachers", json=sample_teacher)
    sample_class["teacher_id"] = teacher_response.get_json()["id"]
    class_response = client.post("/api/classes", json=sample_class)
    class_id = class_response.get_json()["id"]

    # Create multiple students
    for i in range(3):
        student_data = sample_student.copy()
        student_data["email"] = f"student{i}@example.com"
        student_data["class_id"] = class_id
        client.post("/api/students", json=student_data)

    # Get all students
    response = client.get("/api/students")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 3
    for student in data:
        assert "links" in student
