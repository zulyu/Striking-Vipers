import pytest
from app import create_app, db
from app.models import Teacher, Class, Student

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app('testing')
    
    # Create the database and load test data
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

class TestTeacherModel:
    def test_create_teacher(self, app):
        """Test creating a teacher."""
        with app.app_context():
            teacher = Teacher(
                name="Test Teacher",
                email="teacher@test.com",
                subject="Math",
                password_hash="hashed_password"
            )
            db.session.add(teacher)
            db.session.commit()
            
            assert teacher.id is not None
            assert teacher.name == "Test Teacher"
            assert teacher.email == "teacher@test.com"
            assert teacher.subject == "Math"

    def test_teacher_relationships(self, app):
        """Test teacher relationships with classes."""
        with app.app_context():
            teacher = Teacher(
                name="Test Teacher",
                email="teacher@test.com",
                subject="Math",
                password_hash="hashed_password"
            )
            db.session.add(teacher)
            db.session.commit()
            
            class_ = Class(
                id="CS101",
                capacity=30,
                teacher_id=teacher.id
            )
            db.session.add(class_)
            db.session.commit()
            
            assert len(teacher.classes) == 1
            assert teacher.classes[0].id == "CS101"

class TestClassModel:
    def test_create_class(self, app):
        """Test creating a class."""
        with app.app_context():
            teacher = Teacher(
                name="Test Teacher",
                email="teacher@test.com",
                subject="Math",
                password_hash="hashed_password"
            )
            db.session.add(teacher)
            db.session.commit()
            
            class_ = Class(
                id="CS101",
                capacity=30,
                teacher_id=teacher.id
            )
            db.session.add(class_)
            db.session.commit()
            
            assert class_.id == "CS101"
            assert class_.capacity == 30
            assert class_.teacher_id == teacher.id

    def test_class_relationships(self, app):
        """Test class relationships with teacher and students."""
        with app.app_context():
            teacher = Teacher(
                name="Test Teacher",
                email="teacher@test.com",
                subject="Math",
                password_hash="hashed_password"
            )
            db.session.add(teacher)
            db.session.commit()
            
            class_ = Class(
                id="CS101",
                capacity=30,
                teacher_id=teacher.id
            )
            db.session.add(class_)
            db.session.commit()
            
            student = Student(
                name="Test Student",
                email="student@test.com",
                grade="10",
                class_id=class_.id
            )
            db.session.add(student)
            db.session.commit()
            
            assert class_.teacher == teacher
            assert len(class_.students) == 1
            assert class_.students[0].email == "student@test.com"

class TestStudentModel:
    def test_create_student(self, app):
        """Test creating a student."""
        with app.app_context():
            teacher = Teacher(
                name="Test Teacher",
                email="teacher@test.com",
                subject="Math",
                password_hash="hashed_password"
            )
            db.session.add(teacher)
            db.session.commit()
            
            class_ = Class(
                id="CS101",
                capacity=30,
                teacher_id=teacher.id
            )
            db.session.add(class_)
            db.session.commit()
            
            student = Student(
                name="Test Student",
                email="student@test.com",
                grade="10",
                class_id=class_.id
            )
            db.session.add(student)
            db.session.commit()

            assert student.id is not None
            assert student.name == "Test Student"
            assert student.email == "student@test.com"
            assert student.grade == "10"
            assert student.class_id == class_.id

    def test_student_relationships(self, app):
        """Test student relationships with class."""
        with app.app_context():
            teacher = Teacher(
                name="Test Teacher",
                email="teacher@test.com",
                subject="Math",
                password_hash="hashed_password"
            )
            db.session.add(teacher)
            db.session.commit()

            class_ = Class(
                id="CS101",
                capacity=30,
                teacher_id=teacher.id
            )
            db.session.add(class_)
            db.session.commit()
            
            student = Student(
                name="Test Student",
                email="student@test.com",
                grade="10",
                class_id=class_.id
            )
            db.session.add(student)
            db.session.commit() 
            
            assert student.class_id == class_.id
            assert student.class_ref.teacher == teacher 