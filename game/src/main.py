import pygame
import sys
from player import create_player, load_player, save_player
from phases import load_events, trigger_random_event, early_life_phase, young_adult_phase, mid_life_phase
from pygame.locals import QUIT, KEYDOWN, K_s, K_l

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FinLitFun")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Status bar
def draw_status_bar(x, y, value, max_value, color):
    """Draws a status bar representing a value out of a maximum."""
    pygame.draw.rect(WIN, color, (x, y, 200, 20))
    pygame.draw.rect(WIN, WHITE, (x, y, 200 * (1 - value / max_value), 20))


def handle_turn(player):
    """Handles the logic for each turn (year) in the game."""
    events = load_events()
    player = trigger_random_event(player, events)

    if player['age'] < 23:
        player = early_life_phase(player)
    elif player['age'] < 31:
        player = young_adult_phase(player)
    else:
        player = mid_life_phase(player)
    
    save_player(player)
    
    return player


def main():
    clock = pygame.time.Clock()

    # Load or create a player profile
    player = load_player()
    if player is None:
        player_name = input("Enter your player's name: ")
        player = create_player(player_name)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_s:
                    save_player(player)
                    print("Game saved!")
                if event.key == K_l:
                    player = load_player()
                    print("Game loaded!")

        # Handle a turn in the game
        player = handle_turn(player)

        # Draw the game background
        WIN.fill(WHITE)
        
        # Draw status bars for Health, Happiness, and Financial Status
        draw_status_bar(50, 50, player['health'], 100, RED)
        draw_status_bar(50, 100, player['happiness'], 100, GREEN)
        draw_status_bar(50, 150, player['financial_status'], 1000000, BLUE)  # Assuming 1,000,000 is max financial status
        
        # Update the display
        pygame.display.update()
        
        clock.tick(1)  # Slow down the game loop to one tick per second


if __name__ == "__main__":
    main()
