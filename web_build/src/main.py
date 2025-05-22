import pygame
import asyncio
import sys
import random
import json
from pathlib import Path

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

class MatchingGame:
    """Matching game implementation."""
    def __init__(self, screen):
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
        pairs = [
            ("int", "1"),
            ("float", "1.0"),
            ("str", '"hello"'),
            ("list", "[1,2,3]"),
            ("dict", '{"key":"value"}'),
            ("bool", "True")
        ]

        for pair in pairs:
            self.cards.append({
                'type': pair[0],
                'value': pair[0],
                'flipped': False,
                'matched': False,
                'is_type': True,
                'rect': pygame.Rect(0, 0, 100, 150)
            })
            self.cards.append({
                'type': pair[0],
                'value': pair[1],
                'flipped': False,
                'matched': False,
                'is_type': False,
                'rect': pygame.Rect(0, 0, 100, 150)
            })

        random.shuffle(self.cards)

        margin = 20
        card_width = 100
        card_height = 150
        grid_width = 4
        grid_height = 3
        start_x = (WIDTH - (grid_width * card_width + (grid_width - 1) * margin)) // 2
        start_y = (HEIGHT - (grid_height * card_height + (grid_height - 1) * margin)) // 2

        for i, card in enumerate(self.cards):
            row = i // grid_width
            col = i % grid_width
            x = start_x + col * (card_width + margin)
            y = start_y + row * (card_height + margin)
            card['rect'].x = x
            card['rect'].y = y

    def handle_click(self, pos):
        if self.showing_feedback:
            return False

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
        if card1['type'] == card2['type'] and card1['is_type'] != card2['is_type']:
            card1['matched'] = True
            card2['matched'] = True
            self.matched_pairs += 1
            self.showing_feedback = True
            self.feedback_text = "Match!"
            self.feedback_timer = pygame.time.get_ticks()

            if self.matched_pairs == len(self.cards) // 2:
                self.game_over = True
                self.feedback_text = "Game Over!"
        else:
            self.showing_feedback = True
            self.feedback_text = "Try again!"
            self.feedback_timer = pygame.time.get_ticks()
            pygame.time.wait(1000)
            card1['flipped'] = False
            card2['flipped'] = False

        self.selected_cards = []

    def draw(self):
        self.screen.fill(WHITE)

        for card in self.cards:
            if card['flipped'] or card['matched']:
                pygame.draw.rect(self.screen, (200, 200, 200), card['rect'])
                text = font.render(card['value'], True, BLACK)
                text_rect = text.get_rect(center=card['rect'].center)
                self.screen.blit(text, text_rect)
            else:
                pygame.draw.rect(self.screen, (100, 100, 200), card['rect'])

        if self.showing_feedback:
            current_time = pygame.time.get_ticks()
            if current_time - self.feedback_timer >= self.feedback_duration:
                self.showing_feedback = False
            else:
                text = feedback_font.render(self.feedback_text, True, BLACK)
                text_rect = text.get_rect(center=(WIDTH // 2, 50))
                self.screen.blit(text, text_rect)

        exit_button = pygame.draw.rect(self.screen, RED, (20, 20, 100, 40))
        exit_text = button_font.render("Exit", True, WHITE)
        self.screen.blit(exit_text, (30, 25))

        next_button = pygame.draw.rect(self.screen, GREEN, (WIDTH - 120, 20, 100, 40))
        next_text = button_font.render("Next", True, WHITE)
        self.screen.blit(next_text, (WIDTH - 110, 25))

        return exit_button, next_button

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Striking Vipers")
        self.current_screen = "matching"  # Start directly with matching game for web version
        self.matching_game = MatchingGame(self.screen)

    def draw(self):
        if self.current_screen == "matching":
            exit_button, next_button = self.matching_game.draw()
            if self.matching_game.game_over:
                game_over_text = title_font.render("Game Over!", True, BLACK)
                self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
            return exit_button, next_button

async def main():
    game = Game()
    
    while True:
        if game.current_screen == "matching":
            exit_button, next_button = game.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game.current_screen == "matching":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    elif next_button.collidepoint(event.pos):
                        # Reset game
                        game.matching_game = MatchingGame(game.screen)
                    else:
                        game.matching_game.handle_click(event.pos)

        pygame.display.update()
        await asyncio.sleep(0)  # Required for web deployment

# This is the entry point for Pygbag
async def start():
    await main()

# This is required for Pygbag
if __name__ == "__main__":
    asyncio.run(main()) 