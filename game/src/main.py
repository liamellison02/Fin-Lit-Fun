import pygame
import sys
from player import create_player, load_player, save_player
from phases import load_events, trigger_random_event, early_life_phase, young_adult_phase, mid_life_phase
from pygame.locals import QUIT, KEYDOWN, K_s, K_l, MOUSEBUTTONDOWN

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FinLitFun")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BG_BLUE = (111, 128, 145)


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


def draw_title_screen():
    """Displays the title screen with a 'Play Now' button."""
    WIN.fill(BG_BLUE)
    
    # Draw title text
    logo = pygame.image.load('../assets/logo.png')
    logo = pygame.transform.scale(logo, (400, 400))  # Resize the image as needed
    
    # Draw the image above the "Play Now" button
    WIN.blit(logo, (WIDTH // 2 - logo.get_width() // 2, HEIGHT // 1.4 - logo.get_height()))

    # Draw "Play Now" button
    button_font = pygame.font.Font(None, 50)
    button_text = button_font.render("Play Now", True, WHITE)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 60)
    pygame.draw.rect(WIN, BLUE, button_rect)
    WIN.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2, 
                           button_rect.y + (button_rect.height - button_text.get_height()) // 2))

    pygame.display.update()
    
    return button_rect


def title_screen():
    """Handles the title screen logic."""
    button_rect = draw_title_screen()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Exit the title screen and start the game

        pygame.display.update()


def main_game_loop(player):
    """Main game loop after the title screen."""
    clock = pygame.time.Clock()

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
        WIN.fill(BG_BLUE)
        
        # Draw status bars for Health, Happiness, and Financial Status
        draw_status_bar(50, 50, player['health'], 100, RED)
        draw_status_bar(50, 100, player['happiness'], 100, GREEN)
        draw_status_bar(50, 150, player['financial_status'], 1000000, BLUE)  # Assuming 1,000,000 is max financial status
        
        # Update the display
        pygame.display.update()
        
        clock.tick(1)  # Slow down the game loop to one tick per second


def main():
    # Display the title screen
    title_screen()

    # Load or create a player profile
    player = load_player()
    if player is None:
        player_name = input("Enter your player's name: ")
        player = create_player(player_name)

    # Start the main game loop
    main_game_loop(player)


if __name__ == "__main__":
    main()
