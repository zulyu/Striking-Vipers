import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from app import create_app, db
from app.models import Teacher, Class as ClassModel, Student

@pytest.fixture(scope="session")
def app():
    """Create and configure a Flask app for testing."""
    app = create_app('testing')
    
    # Create the database and load test data
    with app.app_context():
        db.create_all()
        
        # Create test data
        teacher = Teacher(name="Test Teacher", email="teacher@test.com", subject="Test")
        db.session.add(teacher)
        
        class_obj = ClassModel(id="CS101", capacity=30, teacher_id=1)
        db.session.add(class_obj)
        
        student = Student(
            name="Test User",
            email="test@example.com",
            username="testuser",
            password="password123",
            class_id="CS101"
        )
        db.session.add(student)
        
        db.session.commit()
        
        yield app
        
        # Clean up
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="session")
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope="session")
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture
def selenium_driver():
    """Create a Selenium WebDriver instance."""
    # Setup Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Initialize the driver with webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    
    yield driver
    
    # Cleanup
    driver.quit()

@pytest.fixture
def base_url(app):
    """Return the base URL for the test server."""
    return "http://localhost:5000" 