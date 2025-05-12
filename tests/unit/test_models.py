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

def test_student_creation(app):
    with app.app_context():
        student = Student(
            name='Jane Smith',
            email='jsmith@example.com',
            grade='10',
            class_id='CS101'
        )
        db.session.add(student)
        db.session.commit()

        assert student.id is not None
        assert student.name == 'Jane Smith'
        assert student.email == 'jsmith@example.com'
        assert student.grade == '10'
        assert student.class_id == 'CS101'

def test_student_validation(app):
    with app.app_context():
        # Test that email must be unique
        student1 = Student(
            name='Jane Smith',
            email='jsmith@example.com',
            grade='10',
            class_id='CS101'
        )
        db.session.add(student1)
        db.session.commit()

        # Try to create another student with the same email
        student2 = Student(
            name='John Doe',
            email='jsmith@example.com',  # Same email as student1
            grade='11',
            class_id='CS102'
        )
        db.session.add(student2)
        
        with pytest.raises(Exception):  # Should raise an integrity error
            db.session.commit() 