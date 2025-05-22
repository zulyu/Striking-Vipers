import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import create_app
import threading
import time
import requests

@pytest.fixture(scope="session")
def app():
    """Create and configure a Flask app for testing."""
    app = create_app('testing')
    return app

@pytest.fixture(scope="session")
def server(app):
    """Start the Flask server in a separate thread."""
    def run_server():
        app.run(port=5002)
    
    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()
    
    # Wait for server to start
    for _ in range(30):  # Try for 30 seconds
        try:
            requests.get('http://localhost:5002/api/')
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    else:
        pytest.fail("Server failed to start")

@pytest.fixture
def selenium_driver():
    """Create a Selenium WebDriver instance."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

@pytest.fixture
def base_url():
    """Base URL for the web application."""
    return 'http://localhost:5002'

@pytest.fixture
def sample_data():
    """Sample data for testing."""
    return {
        'class_id': 'CS101',
        'student_email': 'test@example.com',
        'student_password': 'password123',
        'student_username': 'testuser'
    }

@pytest.fixture
def logged_in_driver(selenium_driver, base_url, sample_data, server):
    """Fixture to provide a logged-in driver"""
    # Navigate to login page
    selenium_driver.get(f"{base_url}/login.html")
    
    # Wait for page to load and elements to be present
    wait = WebDriverWait(selenium_driver, 10)
    email_input = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    username_input = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    password_input = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    classcode_input = wait.until(EC.presence_of_element_located((By.ID, 'classcode')))
    login_button = wait.until(EC.element_to_be_clickable((By.ID, 'login-btn')))
    
    # Fill in login form
    email_input.send_keys(sample_data['student_email'])
    username_input.send_keys(sample_data['student_username'])
    password_input.send_keys(sample_data['student_password'])
    classcode_input.send_keys(sample_data['class_id'])
    
    # Click login button
    login_button.click()
    
    # Wait for login to complete and redirect
    wait.until(EC.url_contains('game.html'))
    
    return selenium_driver

class TestWebGames:
    def test_typing_game(self, logged_in_driver, base_url):
        """Test the typing game."""
        logged_in_driver.get(f"{base_url}/typing_game.html")
        time.sleep(2)  # Wait for game to load
        
        # Add your typing game test logic here
        assert "Typing Game" in logged_in_driver.title

    def test_dragging_game(self, logged_in_driver, base_url):
        """Test the dragging game."""
        logged_in_driver.get(f"{base_url}/dragging_game.html")
        time.sleep(2)  # Wait for game to load
        
        # Add your dragging game test logic here
        assert "Dragging Game" in logged_in_driver.title

    def test_matching_game(self, logged_in_driver, base_url):
        """Test the matching game."""
        logged_in_driver.get(f"{base_url}/matching_game.html")
        time.sleep(2)  # Wait for game to load
        
        # Add your matching game test logic here
        assert "Matching Game" in logged_in_driver.title

    def test_game_navigation(self, logged_in_driver, base_url):
        """Test navigation between games."""
        # Test navigation to typing game
        logged_in_driver.get(f"{base_url}/typing_game.html")
        time.sleep(2)
        assert "Typing Game" in logged_in_driver.title
        
        # Test navigation to dragging game
        logged_in_driver.get(f"{base_url}/dragging_game.html")
        time.sleep(2)
        assert "Dragging Game" in logged_in_driver.title
        
        # Test navigation to matching game
        logged_in_driver.get(f"{base_url}/matching_game.html")
        time.sleep(2)
        assert "Matching Game" in logged_in_driver.title 