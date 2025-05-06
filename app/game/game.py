import pygame
import sys
import sqlite3
import os
import random
import time
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
    def __init__(self, screen):
        self.screen = screen
        self.cards = []
        self.selected_cards = []
        self.matched_pairs = 0
        self.game_over = False
        self.snake_img = self.load_snake_image()
        self.showing_feedback = False
        self.feedback_start_time = 0
        self.feedback_text = ""
        self.feedback_color = BLACK
        self.wrong_match_time = 0  # Track when wrong match animation started
        self.is_animating = False  # Track if we're in animation
        self.setup_cards()
        
    def load_snake_image(self):
        # Load and scale the snake image
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            image_path = os.path.join(project_root, "app", "assets", "snake.png")
            print(f"Attempting to load image from: {image_path}")
            
            if not os.path.exists(image_path):
                print(f"Image file not found at: {image_path}")
                return None
                
            img = pygame.image.load(image_path)
            return pygame.transform.scale(img, (80, 80))
        except Exception as e:
            print(f"Error loading snake image: {e}")
            return None
        
    def setup_cards(self):
        # Create pairs of cards
        pairs = []
        for type_name, value in DATA_TYPES:
            pairs.append({'type': type_name, 'is_type': True})
            pairs.append({'type': type_name, 'is_type': False, 'value': value})
        random.shuffle(pairs)
        
        # Calculate card dimensions and layout
        card_width = 90
        card_height = 130
        spacing = 30
        grid_width = 4 * card_width + 3 * spacing
        grid_height = 3 * card_height + 2 * spacing  # Changed to 3 rows
        
        # Adjust vertical positioning to prevent overlap
        header_height = 150  # Space reserved for title and instructions
        start_x = (WIDTH - grid_width) // 2
        start_y = header_height + 20  # Start grid after header space
        
        for i, pair in enumerate(pairs):
            row = i // 4  # 4 cards per row
            col = i % 4
            x = start_x + col * (card_width + spacing)
            y = start_y + row * (card_height + spacing)
            
            card = {
                'rect': pygame.Rect(x, y, card_width, card_height),
                'type': pair['type'],
                'is_type': pair.get('is_type', True),
                'value': pair.get('value', ''),
                'flipped': False,
                'matched': False,
                'wrong_match': False
            }
            self.cards.append(card)
    
    def draw_card(self, card, x, y, width, height):
        # Draw card background with more visible colors
        if card['matched']:
            pygame.draw.rect(self.screen, GREEN, (x, y, width, height))
        elif card['wrong_match']:
            # Make wrong matches bright red
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, width, height))
            # Add a visual effect (like a border)
            pygame.draw.rect(self.screen, (200, 0, 0), (x, y, width, height), 4)
        elif card['flipped']:
            pygame.draw.rect(self.screen, BLUE, (x, y, width, height))
        else:
            pygame.draw.rect(self.screen, YELLOW, (x, y, width, height))
            if self.snake_img:
                scaled_size = 60
                snake_x = x + (width - scaled_size) // 2
                snake_y = y + (height - scaled_size) // 2
                scaled_img = pygame.transform.scale(self.snake_img, (scaled_size, scaled_size))
                self.screen.blit(scaled_img, (snake_x, snake_y))
        
        # Draw card border
        pygame.draw.rect(self.screen, BLACK, (x, y, width, height), 2)
        
        # Draw card content with improved visibility
        if card['flipped'] or card['matched'] or card['wrong_match']:
            if card['is_type']:
                text_content = card['type']
            else:
                text_content = card['value']
            small_card_font = pygame.font.SysFont("Arial", 16)
            text = small_card_font.render(text_content, True, WHITE)
            text_rect = text.get_rect(center=(x + width//2, y + height//2))
            self.screen.blit(text, text_rect)
    
    def draw_feedback(self):
        if self.showing_feedback and time.time() - self.feedback_start_time < 1.5:  # Increased duration to 1.5 seconds
            text = feedback_font.render(self.feedback_text, True, self.feedback_color)
            # Make the text larger and more visible
            feedback_bg = pygame.Surface((text.get_width() + 40, text.get_height() + 20))
            feedback_bg.fill(WHITE)
            feedback_bg.set_alpha(200)
            
            # Center the feedback
            bg_rect = feedback_bg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            
            # Draw background and text
            self.screen.blit(feedback_bg, bg_rect)
            self.screen.blit(text, text_rect)
        else:
            self.showing_feedback = False
    
    def show_feedback(self, text, color):
        self.feedback_text = text
        self.feedback_color = color
        self.showing_feedback = True
        self.feedback_start_time = time.time()
    
    def draw(self):
        self.screen.fill(WHITE)
        
        # Adjust text positioning
        title_y = 40
        instructions_y = 90
        
        # Draw title with background highlight
        title_text = title_font.render("Match Data Types", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH // 2, title_y))
        self.screen.blit(title_text, title_rect)
        
        # Draw instructions with background highlight
        inst_text = button_font.render("Match the data type with its example", True, BLACK)
        inst_rect = inst_text.get_rect(center=(WIDTH // 2, instructions_y))
        self.screen.blit(inst_text, inst_rect)
        
        # Draw cards
        for card in self.cards:
            self.draw_card(card, card['rect'].x, card['rect'].y, 
                         card['rect'].width, card['rect'].height)
        
        # Draw feedback if active
        self.draw_feedback()
        
        # Check if we need to reset wrong matched cards
        current_time = time.time()
        if self.is_animating and current_time - self.wrong_match_time >= 1:
            for card in self.selected_cards:
                if card['wrong_match']:
                    card['wrong_match'] = False
                    card['flipped'] = False
            self.is_animating = False
            self.selected_cards = []
        
        # Move buttons up slightly to ensure they don't overlap with cards
        button_y = HEIGHT - 100
        exit_button = pygame.draw.rect(self.screen, RED, (50, button_y, 200, 50))
        next_button = pygame.draw.rect(self.screen, GREEN, (WIDTH - 250, button_y, 200, 50))
        
        exit_text = button_font.render("Exit Game", True, WHITE)
        next_text = button_font.render("Next Level", True, WHITE)
        
        exit_text_rect = exit_text.get_rect(center=(150, button_y + 25))
        next_text_rect = next_text.get_rect(center=(WIDTH - 150, button_y + 25))
        
        self.screen.blit(exit_text, exit_text_rect)
        self.screen.blit(next_text, next_text_rect)
        
        # Draw game over message if applicable
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            complete_text = title_font.render("Level Complete!", True, WHITE)
            complete_rect = complete_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(complete_text, complete_rect)
        
        return exit_button, next_button
    
    async def process_match(self, card1, card2):
        # Check if one card is a type and the other is a matching value
        is_match = False
        for type_name, value in DATA_TYPES:
            if ((card1['type'] == type_name and card2['value'] == value) or
                (card2['type'] == type_name and card1['value'] == value)):
                is_match = True
                break
        
        if is_match:
            self.show_feedback("Correct!", GREEN)
            card1['matched'] = True
            card2['matched'] = True
            self.matched_pairs += 1
            if self.matched_pairs == len(DATA_TYPES):
                self.game_over = True
        else:
            self.show_feedback("Wrong!", (255, 0, 0))  # Bright red color
            card1['wrong_match'] = True
            card2['wrong_match'] = True
            self.wrong_match_time = time.time()
            self.is_animating = True
            await asyncio.sleep(1)  # Show red cards for 1 second
            
            # Only reset if these are still the wrong-matched cards
            if card1['wrong_match'] and card2['wrong_match']:
                card1['wrong_match'] = False
                card2['wrong_match'] = False
                card1['flipped'] = False
                card2['flipped'] = False
                self.is_animating = False
        
        self.selected_cards = []
    
    def handle_click(self, pos):
        # Don't allow clicks during animation
        if self.is_animating:
            return False
            
        for card in self.cards:
            if card['rect'].collidepoint(pos) and not card['flipped'] and not card['matched']:
                card['flipped'] = True
                self.selected_cards.append(card)
                
                if len(self.selected_cards) == 2:
                    asyncio.run(self.process_match(self.selected_cards[0], self.selected_cards[1]))
                return True
        return False

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Striking Vipers")
        self.current_screen = "login"
        self.email = ""
        self.username = ""
        self.password = ""
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

        # Draw test account info
        info_text = button_font.render("Test Account - Email: test@example.com, Username: testuser, Password: password123, Class: CS101", True, BLACK)
        self.screen.blit(info_text, (10, HEIGHT - 30))

        return login_button

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
        try:
            conn = sqlite3.connect("game.db")
            c = conn.cursor()
            c.execute("""
                SELECT * FROM students 
                WHERE StudentEmail = ? 
                AND StudentUserName = ? 
                AND StudentPassWord = ?
                AND ClassCode = ?
            """, (self.email, self.username, self.password, self.classcode))
            result = c.fetchone()
            conn.close()
            
            if result:
                print("Login successful!")
                self.current_screen = "level"
                return True
            print(f"Login failed. Please check your credentials.")
            return False
        except Exception as e:
            print(f"Login error: {e}")
            return False

    def run(self):
        while True:
            if self.current_screen == "login":
                login_button = self.draw_login_screen()
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

if __name__ == "__main__":
    init_game()
