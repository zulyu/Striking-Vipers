import pytest
from app import create_app, db
from app.models import Student, Class
from app.game.game import Game

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def sample_data(app):
    with app.app_context():
        # Create a class
        classroom = Class(
            id='CS101',
            capacity=30,
            teacher_id=1
        )
        db.session.add(classroom)
        db.session.commit()

        # Create a student
        student = Student(
            name='Jane Smith',
            email='jsmith@example.com',
            grade='10',
            class_id=classroom.id
        )
        db.session.add(student)
        db.session.commit()

        return {
            'class_id': classroom.id,
            'student_email': student.email
        }

def test_game_initialization():
    game = Game()
    assert game.current_screen == "login"
    assert game.username == ""
    assert game.password == ""
    assert game.classcode == ""
    assert game.selected_box is None

def test_login_success(app, sample_data):
    with app.app_context():
        game = Game()
        game.username = sample_data['student_email']
        game.classcode = sample_data['class_id']
        
        assert game.handle_login() is True
        assert game.current_screen == "level"

def test_login_failure(app):
    with app.app_context():
        game = Game()
        game.username = "nonexistent@example.com"
        game.classcode = "INVALID"
        
        assert game.handle_login() is False
        assert game.current_screen == "login" 