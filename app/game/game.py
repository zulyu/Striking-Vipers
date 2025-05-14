import pygame
import sys
import sqlite3
import os
import random
import time
import requests
import asyncio

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
RED = (255, 50, 50)
YELLOW = (255, 223, 0)

# Fonts
font = pygame.font.SysFont("Arial", 30)
button_font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 40)
card_font = pygame.font.SysFont("Arial", 20)
feedback_font = pygame.font.SysFont("Arial", 36)

# Data type pairs for matching
DATA_TYPES = [
    ("Float", "6.2"),
    ("Int", "42"),
    ("String", "Python"),
    ("Boolean", "True"),
    ("List", "[1,2,3]"),
    ("Dict", "{key:val}")
]

# API Configuration
API_URL = "https://your-backend-api-url.com/api"  # Replace with your actual API URL

# Initialize SQLite database
def init_db():
    # Remove existing database if it exists
    if os.path.exists("game.db"):
        os.remove("game.db")
        
    db_path = "game.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create tables if they don't exist with email field
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY, 
                  StudentFirstName TEXT,
                  StudentLastName TEXT,
                  StudentEmail TEXT UNIQUE,
                  StudentUserName TEXT UNIQUE,
                  StudentPassWord TEXT,
                  ClassCode TEXT)''')
    
    # Add test account with email
    c.execute("""
        INSERT INTO students 
        (StudentFirstName, StudentLastName, StudentEmail, StudentUserName, StudentPassWord, ClassCode) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("Test", "User", "test@example.com", "testuser", "password123", "CS101"))
    
    conn.commit()
    conn.close()
    print("Database initialized with test account:")
    print("Email: test@example.com")
    print("Username: testuser")
    print("Password: password123")
    print("Class Code: CS101")

class MatchingGame:
    """Matching game implementation."""

    def __init__(self, screen):
        """Initialize the matching game."""
        self.screen = screen
        self.cards = []
        self.selected_cards = []
        self.matched_pairs = 0
        self.game_over = False
        self.showing_feedback = False
        self.feedback_text = ""
        self.feedback_timer = 0
        self.feedback_duration = 2000  # 2 seconds
        self.initialize_cards()

    def initialize_cards(self):
        """Initialize the card deck."""
        # Define the pairs (type and value)
        pairs = [
            ("int", "1"),
            ("float", "1.0"),
            ("str", '"hello"'),
            ("list", "[1,2,3]"),
            ("dict", '{"key":"value"}'),
            ("bool", "True")
        ]

        # Create cards for each pair
        for pair in pairs:
            # Add type card
            self.cards.append({
                'type': pair[0],
                'value': pair[0],
                'flipped': False,
                'matched': False,
                'is_type': True,
                'rect': pygame.Rect(0, 0, 100, 150)  # Will be positioned later
            })
            # Add value card
            self.cards.append({
                'type': pair[0],
                'value': pair[1],
                'flipped': False,
                'matched': False,
                'is_type': False,
                'rect': pygame.Rect(0, 0, 100, 150)  # Will be positioned later
            })

        # Shuffle the cards
        random.shuffle(self.cards)

        # Position the cards in a grid
        margin = 20
        card_width = 100
        card_height = 150
        grid_width = 4
        grid_height = 3
        start_x = (1280 - (grid_width * card_width + (grid_width - 1) * margin)) // 2
        start_y = (800 - (grid_height * card_height + (grid_height - 1) * margin)) // 2

        for i, card in enumerate(self.cards):
            row = i // grid_width
            col = i % grid_width
            x = start_x + col * (card_width + margin)
            y = start_y + row * (card_height + margin)
            card['rect'].x = x
            card['rect'].y = y

    def handle_click(self, pos):
        """Handle mouse click event."""
        if self.showing_feedback:
            return False

        # Check if a card was clicked
        for card in self.cards:
            if card['rect'].collidepoint(pos):
                if not card['flipped'] and not card['matched'] and len(self.selected_cards) < 2:
                    card['flipped'] = True
                    self.selected_cards.append(card)
                    if len(self.selected_cards) == 2:
                        self.process_match(self.selected_cards[0], self.selected_cards[1])
                    return True
        return False

    def process_match(self, card1, card2):
        """Process a potential match between two cards."""
        # Check if the cards match
        if card1['type'] == card2['type'] and card1['is_type'] != card2['is_type']:
            card1['matched'] = True
            card2['matched'] = True
            self.matched_pairs += 1
            self.showing_feedback = True
            self.feedback_text = "Match!"
            self.feedback_timer = pygame.time.get_ticks()

            # Check if game is over
            if self.matched_pairs == len(self.cards) // 2:
                self.game_over = True
                self.feedback_text = "Game Over!"
        else:
            # Cards don't match, flip them back after a delay
            self.showing_feedback = True
            self.feedback_text = "Try again!"
            self.feedback_timer = pygame.time.get_ticks()
            pygame.time.wait(1000)  # Show cards for 1 second
            card1['flipped'] = False
            card2['flipped'] = False

        self.selected_cards = []

    def check_game_over(self):
        """Check if the game is over."""
        if self.matched_pairs == len(self.cards) // 2:
            self.game_over = True
            self.feedback_text = "Game Over!"
            self.showing_feedback = True
            self.feedback_timer = pygame.time.get_ticks()
        return self.game_over

    def draw(self):
        """Draw the game state."""
        self.screen.fill((255, 255, 255))  # White background

        # Draw cards
        for card in self.cards:
            if card['flipped'] or card['matched']:
                # Draw card face
                pygame.draw.rect(self.screen, (200, 200, 200), card['rect'])
                # Draw text
                font = pygame.font.Font(None, 24)
                text = font.render(card['value'], True, (0, 0, 0))
                text_rect = text.get_rect(center=card['rect'].center)
                self.screen.blit(text, text_rect)
            else:
                # Draw card back
                pygame.draw.rect(self.screen, (100, 100, 200), card['rect'])

        # Draw feedback if showing
        if self.showing_feedback:
            current_time = pygame.time.get_ticks()
            if current_time - self.feedback_timer >= self.feedback_duration:
                self.showing_feedback = False
            else:
                font = pygame.font.Font(None, 48)
                text = font.render(self.feedback_text, True, (0, 0, 0))
                text_rect = text.get_rect(center=(640, 50))
                self.screen.blit(text, text_rect)

        # Draw exit and next buttons
        exit_button = pygame.draw.rect(self.screen, RED, (20, 20, 100, 40))
        exit_text = button_font.render("Exit", True, WHITE)
        self.screen.blit(exit_text, (30, 25))

        next_button = pygame.draw.rect(self.screen, GREEN, (WIDTH - 120, 20, 100, 40))
        next_text = button_font.render("Next", True, WHITE)
        self.screen.blit(next_text, (WIDTH - 110, 25))

        pygame.display.flip()
        return exit_button, next_button

class Game:
    """Main game class."""

    def __init__(self):
        """Initialize the game."""
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Striking Vipers")
        self.current_screen = "login"
        self.username = ""
        self.password = ""
        self.email = ""
        self.classcode = ""
        self.selected_box = None
        self.matching_game = None
        self.setup_input_boxes()
        init_db()  # Initialize database with test account

    def setup_input_boxes(self):
        box_width = 300
        box_height = 40
        box_x = WIDTH // 2 - box_width // 2
        spacing = 20

        # Add email box and adjust other boxes' positions
        self.email_box = pygame.Rect(
            box_x, HEIGHT // 2 - box_height * 2 - spacing * 3, box_width, box_height
        )
        self.classcode_box = pygame.Rect(
            box_x, HEIGHT // 2 - box_height - spacing * 2, box_width, box_height
        )
        self.username_box = pygame.Rect(
            box_x, HEIGHT // 2 - spacing, box_width, box_height
        )
        self.password_box = pygame.Rect(
            box_x, HEIGHT // 2 + box_height + spacing, box_width, box_height
        )

    def draw_login_screen(self):
        self.screen.fill(WHITE)

        # Title
        title_text = title_font.render("Striking Vipers", True, BLACK)
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 6))

        # Draw input boxes
        pygame.draw.rect(self.screen, BLUE, self.email_box, 2)
        pygame.draw.rect(self.screen, BLUE, self.classcode_box, 2)
        pygame.draw.rect(self.screen, BLUE, self.username_box, 2)
        pygame.draw.rect(self.screen, BLUE, self.password_box, 2)

        # Render and draw text inside input boxes
        email_text = font.render(
            self.email if self.email else "Email", True, BLACK
        )
        classcode_text = font.render(
            self.classcode if self.classcode else "Class Code", True, BLACK
        )
        username_text = font.render(
            self.username if self.username else "Username", True, BLACK
        )
        hidden_pw = "*" * len(self.password)
        password_text = font.render(
            hidden_pw if self.password else "Password", True, BLACK
        )

        self.screen.blit(email_text, (self.email_box.x + 10, self.email_box.y + 5))
        self.screen.blit(classcode_text, (self.classcode_box.x + 10, self.classcode_box.y + 5))
        self.screen.blit(username_text, (self.username_box.x + 10, self.username_box.y + 5))
        self.screen.blit(password_text, (self.password_box.x + 10, self.password_box.y + 5))

        # Draw login button
        login_button = pygame.draw.rect(
            self.screen, GREEN, (WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)
        )
        button_text = button_font.render("Login", True, WHITE)
        self.screen.blit(
            button_text, (WIDTH // 2 - button_text.get_width() // 2, HEIGHT // 2 + 160)
        )

        # Draw signup button
        signup_button = pygame.draw.rect(
            self.screen, BLUE, (WIDTH // 2 - 100, HEIGHT // 2 + 220, 200, 50)
        )
        signup_text = button_font.render("Sign Up", True, WHITE)
        self.screen.blit(
            signup_text, (WIDTH // 2 - signup_text.get_width() // 2, HEIGHT // 2 + 230)
        )

        # Draw test account info
        info_text = button_font.render("Test Account - Email: test@example.com, Username: testuser, Password: password123, Class: CS101", True, BLACK)
        self.screen.blit(info_text, (10, HEIGHT - 30))

        return login_button, signup_button

    def draw_level_screen(self):
        self.screen.fill(WHITE)
        
        # Title
        title_text = title_font.render("Select Level", True, BLACK)
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 6))

        # Level buttons
        level1_button = pygame.draw.rect(self.screen, BLUE, (WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50))
        level2_button = pygame.draw.rect(self.screen, BLUE, (WIDTH // 2 - 100, HEIGHT // 2, 200, 50))
        level3_button = pygame.draw.rect(self.screen, BLUE, (WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50))

        # Level button text
        level1_text = button_font.render("Typing Game", True, WHITE)
        level2_text = button_font.render("Dragging Game", True, WHITE)
        level3_text = button_font.render("Matching Game", True, WHITE)

        self.screen.blit(level1_text, (WIDTH // 2 - level1_text.get_width() // 2, HEIGHT // 2 - 90))
        self.screen.blit(level2_text, (WIDTH // 2 - level2_text.get_width() // 2, HEIGHT // 2 + 10))
        self.screen.blit(level3_text, (WIDTH // 2 - level3_text.get_width() // 2, HEIGHT // 2 + 110))

        return level1_button, level2_button, level3_button

    def handle_login(self):
        """Handle login attempt using API."""
        try:
            if requests:  # Check if requests is available (not in browser)
                response = requests.post(f"{API_URL}/auth/login", json={
                    "email": self.email,
                    "username": self.username,
                    "password": self.password,
                    "classcode": self.classcode
                })
                if response.status_code == 200:
                    self.current_screen = "level"
                    return True
            else:
                # For browser: use test account (temporary solution)
                if (self.email == "test@example.com" and 
                    self.username == "testuser" and 
                    self.password == "password123" and
                    self.classcode == "CS101"):
                    self.current_screen = "level"
                    return True
        except Exception as e:
            print(f"Login error: {e}")
        return False

    def handle_signup(self):
        """Handle signup attempt using API."""
        try:
            if requests:  # Check if requests is available (not in browser)
                response = requests.post(f"{API_URL}/auth/signup", json={
                    "name": self.username,
                    "email": self.email,
                    "password": self.password,
                    "role": "student",
                    "class_code": self.classcode
                })
                if response.status_code == 201:
                    self.current_screen = "level"
                    return True, "Signup successful"
                else:
                    error_msg = "Email already exists or invalid data"
                    if response.json() and "message" in response.json():
                        error_msg = response.json()["message"]
                    return False, error_msg
            else:
                # For browser: only allow test account (temporary)
                if self.email == "test@example.com":
                    return False, "Email already registered"
                else:
                    # Simulate successful signup in browser
                    self.current_screen = "level"
                    return True, "Signup successful (TEST MODE)"
        except Exception as e:
            print(f"Signup error: {e}")
            return False, str(e)

    def run(self):
        while True:
            if self.current_screen == "login":
                login_button, signup_button = self.draw_login_screen()
            elif self.current_screen == "level":
                level1_button, level2_button, level3_button = self.draw_level_screen()
            elif self.current_screen == "matching":
                exit_button, next_button = self.matching_game.draw()
                if self.matching_game.game_over:
                    # Show game over message
                    game_over_text = title_font.render("Game Over!", True, BLACK)
                    self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.current_screen == "login":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.email_box.collidepoint(event.pos):
                            self.selected_box = "email"
                        elif self.classcode_box.collidepoint(event.pos):
                            self.selected_box = "classcode"
                        elif self.username_box.collidepoint(event.pos):
                            self.selected_box = "username"
                        elif self.password_box.collidepoint(event.pos):
                            self.selected_box = "password"
                        elif login_button.collidepoint(event.pos):
                            if self.handle_login():
                                print("Login successful!")
                            else:
                                print("Login failed.")
                        elif signup_button.collidepoint(event.pos):
                            success, message = self.handle_signup()
                            if success:
                                print("Signup successful!")
                                self.current_screen = "level"
                            else:
                                print(f"Signup failed: {message}")

                    elif event.type == pygame.KEYDOWN:
                        if self.selected_box == "email":
                            if event.key == pygame.K_BACKSPACE:
                                self.email = self.email[:-1]
                            else:
                                self.email += event.unicode
                        elif self.selected_box == "classcode":
                            if event.key == pygame.K_BACKSPACE:
                                self.classcode = self.classcode[:-1]
                            else:
                                self.classcode += event.unicode
                        elif self.selected_box == "username":
                            if event.key == pygame.K_BACKSPACE:
                                self.username = self.username[:-1]
                            else:
                                self.username += event.unicode
                        elif self.selected_box == "password":
                            if event.key == pygame.K_BACKSPACE:
                                self.password = self.password[:-1]
                            else:
                                self.password += event.unicode

                elif self.current_screen == "level":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if level1_button.collidepoint(event.pos):
                            print("Starting Typing Game")
                            # TODO: Implement typing game
                        elif level2_button.collidepoint(event.pos):
                            print("Starting Dragging Game")
                            # TODO: Implement dragging game
                        elif level3_button.collidepoint(event.pos):
                            print("Starting Matching Game")
                            self.matching_game = MatchingGame(self.screen)
                            self.current_screen = "matching"

                elif self.current_screen == "matching":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if exit_button.collidepoint(event.pos):
                            self.current_screen = "level"
                        elif next_button.collidepoint(event.pos):
                            # TODO: Implement next level
                            pass
                        else:
                            self.matching_game.handle_click(event.pos)

            pygame.display.update()

def init_game():
    game = Game()
    game.run()

# Main function for pygbag compatibility
async def main():
    game = Game()
    
    running = True
    while running:
        # Handle game state
        if game.current_screen == "login":
            login_button, signup_button = game.draw_login_screen()
        elif game.current_screen == "level":
            level1_button, level2_button, level3_button = game.draw_level_screen()
        elif game.current_screen == "matching":
            exit_button, next_button = game.matching_game.draw()
            if game.matching_game.game_over:
                game_over_text = title_font.render("Game Over!", True, BLACK)
                game.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Handle events based on current screen
            if game.current_screen == "login":
                # Placeholder for login event handling
                pass
                
            elif game.current_screen == "level":
                # Placeholder for level event handling
                pass
                
            elif game.current_screen == "matching":
                # Placeholder for matching game event handling
                pass
                
        # This is critical for web deployment
        pygame.display.flip()
        await asyncio.sleep(0)  # Required for web version
    
    pygame.quit()

# Entry point
if __name__ == "__main__":
    if 'asyncio' in sys.modules:
        # Web (pygbag) mode
        asyncio.run(main())
    else:
        # Desktop mode - fall back to your original code
        init_game()
