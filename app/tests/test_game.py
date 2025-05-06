import pytest
from app.game.game import Game


@pytest.fixture
def game():
    return Game()


def test_game_initialization(game):
    assert game.current_screen == "login"
    assert game.username == ""
    assert game.password == ""
    assert game.classcode == ""
    assert game.selected_box is None


def test_input_box_setup(game):
    assert game.classcode_box.width == 300
    assert game.classcode_box.height == 40
    assert game.username_box.width == 300
    assert game.username_box.height == 40
    assert game.password_box.width == 300
    assert game.password_box.height == 40


def test_handle_login(game, monkeypatch):
    # Mock the database query
    class MockStudent:
        def __init__(self):
            self.StudentUserName = "testuser"
            self.StudentPassWord = "testpass"
            self.ClassCode = "testcode"

    def mock_query(*args, **kwargs):
        return MockStudent()

    monkeypatch.setattr("app.game.game.Student.query.filter_by", mock_query)

    game.username = "testuser"
    game.password = "testpass"
    game.classcode = "testcode"

    result = game.handle_login()
    assert result is True
    assert game.current_screen == "level"
