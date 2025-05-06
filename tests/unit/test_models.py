import pytest
from app import create_app, db
from app.models import Student

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

        # Test that the student was created correctly
        saved_student = Student.query.filter_by(email='jsmith@example.com').first()
        assert saved_student is not None
        assert saved_student.name == 'Jane Smith'
        assert saved_student.grade == '10'
        assert saved_student.class_id == 'CS101'

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

        student2 = Student(
            name='John Smith',
            email='jsmith@example.com',  # Same email
            grade='10',
            class_id='CS101'
        )
        db.session.add(student2)
        with pytest.raises(Exception):
            db.session.commit() 