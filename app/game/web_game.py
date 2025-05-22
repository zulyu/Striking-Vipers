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

# Initialize SQLite database in memory for web version
def init_db():
    conn = sqlite3.connect(':memory:')
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
        init_db()

    # ... [Rest of the Game class implementation remains the same] ...

async def main():
    game = Game()
    
    while True:
        if game.current_screen == "login":
            login_button, signup_button = game.draw_login_screen()
        elif game.current_screen == "level":
            level1_button, level2_button, level3_button = game.draw_level_screen()
        elif game.current_screen == "matching":
            exit_button, next_button = game.matching_game.draw()
            if game.matching_game.game_over:
                game_over_text = title_font.render("Game Over!", True, BLACK)
                game.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game.current_screen == "login":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game.email_box.collidepoint(event.pos):
                        game.selected_box = "email"
                    elif game.classcode_box.collidepoint(event.pos):
                        game.selected_box = "classcode"
                    elif game.username_box.collidepoint(event.pos):
                        game.selected_box = "username"
                    elif game.password_box.collidepoint(event.pos):
                        game.selected_box = "password"
                    elif login_button.collidepoint(event.pos):
                        if game.handle_login():
                            print("Login successful!")
                        else:
                            print("Login failed.")
                    elif signup_button.collidepoint(event.pos):
                        success, message = game.handle_signup()
                        if success:
                            print("Signup successful!")
                            game.current_screen = "level"
                        else:
                            print(f"Signup failed: {message}")

                elif event.type == pygame.KEYDOWN:
                    if game.selected_box == "email":
                        if event.key == pygame.K_BACKSPACE:
                            game.email = game.email[:-1]
                        else:
                            game.email += event.unicode
                    elif game.selected_box == "classcode":
                        if event.key == pygame.K_BACKSPACE:
                            game.classcode = game.classcode[:-1]
                        else:
                            game.classcode += event.unicode
                    elif game.selected_box == "username":
                        if event.key == pygame.K_BACKSPACE:
                            game.username = game.username[:-1]
                        else:
                            game.username += event.unicode
                    elif game.selected_box == "password":
                        if event.key == pygame.K_BACKSPACE:
                            game.password = game.password[:-1]
                        else:
                            game.password += event.unicode

            elif game.current_screen == "level":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if level1_button.collidepoint(event.pos):
                        print("Starting Typing Game")
                    elif level2_button.collidepoint(event.pos):
                        print("Starting Dragging Game")
                    elif level3_button.collidepoint(event.pos):
                        print("Starting Matching Game")
                        game.matching_game = MatchingGame(game.screen)
                        game.current_screen = "matching"

            elif game.current_screen == "matching":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button.collidepoint(event.pos):
                        game.current_screen = "level"
                    elif next_button.collidepoint(event.pos):
                        pass
                    else:
                        game.matching_game.handle_click(event.pos)

        pygame.display.update()
        await asyncio.sleep(0)  # Required for web deployment

asyncio.run(main()) 