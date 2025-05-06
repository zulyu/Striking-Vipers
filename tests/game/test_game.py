import pytest
from app import create_app, db
from app.models import Teacher, Class as ClassModel, Student
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
        # Create a test account with the same credentials as in game.py
        student = Student(
            name='Test User',
            email='test@example.com',
            grade='10',
            class_id='CS101'
        )
        db.session.add(student)
        db.session.commit()

        return {
            'student_email': 'test@example.com',
            'student_username': 'testuser',
            'student_password': 'password123',
            'class_id': 'CS101'
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
        game.email = sample_data['student_email']
        game.username = sample_data['student_username']
        game.password = sample_data['student_password']
        game.classcode = sample_data['class_id']
        
        assert game.handle_login() is True
        assert game.current_screen == "level"

def test_login_failure(app):
    with app.app_context():
        game = Game()
        game.email = "nonexistent@example.com"
        game.username = "nonexistent"
        game.password = "wrongpass"
        game.classcode = "INVALID"
        
        assert game.handle_login() is False
        assert game.current_screen == "login" 