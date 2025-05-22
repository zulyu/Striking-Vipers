import pytest
from app import create_app, db
from app.models import Teacher, Class as ClassModel, Student
from app.game.game import Game, MatchingGame, init_db
import pygame
import os
import time
from app.config import config

@pytest.fixture(scope='function')
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

@pytest.fixture
def game():
    pygame.init()

    return Game()

@pytest.fixture
def matching_game():
    pygame.init()
    screen = pygame.display.set_mode((1280, 800))
    return MatchingGame(screen)

@pytest.fixture
def test_data(app):
    """Create test data for login."""
    with app.app_context():
        # Create a test teacher
        teacher = Teacher(name="Test Teacher", email="teacher@test.com", subject="Test")
        db.session.add(teacher)
        
        # Create a test class
        class_obj = ClassModel(id="CS101", capacity=30, teacher_id=1)
        db.session.add(class_obj)
        
        # Create a test student
        student = Student(name="testuser", email="test@example.com", grade="10", class_id="CS101")
        db.session.add(student)
        
        db.session.commit()
        
        return {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'password123',
            'classcode': 'CS101'
        }

def test_game_initialization(game):
    assert game.current_screen == "login"
    assert game.username == ""
    assert game.password == ""
    assert game.email == ""
    assert game.classcode == ""
    assert game.selected_box is None

def test_matching_game_initialization(matching_game):
    assert matching_game.cards != []
    assert len(matching_game.cards) == 12  # 6 pairs
    assert matching_game.selected_cards == []
    assert matching_game.matched_pairs == 0
    assert matching_game.game_over is False
    assert matching_game.showing_feedback is False
    assert matching_game.feedback_text == ""
    assert matching_game.feedback_timer == 0
    assert matching_game.feedback_duration == 2000

def test_card_flipping(matching_game):
    # Get first card position
    first_card = matching_game.cards[0]
    card_center = (
        first_card['rect'].x + first_card['rect'].width // 2,
        first_card['rect'].y + first_card['rect'].height // 2
    )
    
    # Simulate clicking the card
    assert matching_game.handle_click(card_center) is True
    assert first_card['flipped'] is True
    assert len(matching_game.selected_cards) == 1

def test_matching_pairs(matching_game):
    # Find a matching pair
    type_card = None
    value_card = None
    
    for i, card in enumerate(matching_game.cards):
        if card['is_type']:
            type_card = card
            # Find its matching value
            type_name = card['type']
            for other_card in matching_game.cards[i+1:]:
                if not other_card['is_type'] and other_card['type'] == type_name:
                    value_card = other_card
                    break
            if value_card:
                break
    
    assert type_card is not None
    assert value_card is not None
    
    # Simulate matching the pair
    type_card['flipped'] = True
    matching_game.selected_cards.append(type_card)
    value_card['flipped'] = True
    matching_game.selected_cards.append(value_card)
    
    # Process the match
    matching_game.process_match(type_card, value_card)
    
    assert type_card['matched'] is True
    assert value_card['matched'] is True
    assert matching_game.matched_pairs == 1
    assert matching_game.showing_feedback is True
    assert matching_game.feedback_text == "Match!"

def test_wrong_match(matching_game):
    # Find two non-matching cards
    first_card = None
    second_card = None
    
    for i, card in enumerate(matching_game.cards):
        if card['is_type']:
            first_card = card
            # Find a non-matching value card
            for other_card in matching_game.cards[i+1:]:
                if not other_card['is_type'] and other_card['type'] != first_card['type']:
                    second_card = other_card
                    break
            if second_card:
                break
    
    assert first_card is not None
    assert second_card is not None
    
    # Simulate matching non-matching cards
    first_card['flipped'] = True
    matching_game.selected_cards.append(first_card)
    second_card['flipped'] = True
    matching_game.selected_cards.append(second_card)
    
    # Process the match
    matching_game.process_match(first_card, second_card)
    
    assert first_card['matched'] is False
    assert second_card['matched'] is False
    assert matching_game.matched_pairs == 0
    assert matching_game.showing_feedback is True
    assert matching_game.feedback_text == "Try again!"

def test_game_completion(matching_game):
    # Simulate matching all pairs
    for i in range(0, len(matching_game.cards), 2):
        card1 = matching_game.cards[i]
        card2 = matching_game.cards[i+1]
        card1['matched'] = True
        card2['matched'] = True
        matching_game.matched_pairs += 1
    
    assert matching_game.matched_pairs == len(matching_game.cards) // 2
    matching_game.check_game_over()  # Call check_game_over to update game state
    assert matching_game.game_over is True
    assert matching_game.showing_feedback is True
    assert matching_game.feedback_text == "Game Over!"

def test_invalid_login(game):
    game.email = "invalid@example.com"
    game.username = "invalid"
    game.password = "invalid"
    game.classcode = "invalid"
    
    assert game.handle_login() is False
    assert game.current_screen == "login"

# def test_successful_login(game):
#     game.email = "test@example.com"
#     game.username = "testuser"
#     game.password = "password123"
#     game.classcode = "CS101"
    
#     assert game.handle_login() is True
#     assert game.current_screen == "level" 

def test_successful_login(game, sample_data):
    """Test successful login with valid credentials"""
    # Use the sample data from the fixture
    game.email = sample_data['student_email']
    game.username = sample_data['student_username']
    game.password = sample_data['student_password']
    game.classcode = sample_data['class_id']
    
    # Add a small delay to ensure database is ready
    time.sleep(0.5)
    
    assert game.handle_login() is True
    assert game.current_screen == "level" 
