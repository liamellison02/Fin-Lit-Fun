import pygame
import sys
from player import create_player, load_player, save_player
from phases import load_events, trigger_random_event, early_life_phase, young_adult_phase, mid_life_phase
from pygame.locals import QUIT, KEYDOWN, K_s, K_l, MOUSEBUTTONDOWN, K_RETURN, K_BACKSPACE
from ui.guide import guide_screen, phases_screen, status_screen
from ui.dashboard import dashboard_screen

from utils import prompt_user

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
    WIN.fill(BG_BLUE)  # Set background color to BG_BLUE
    
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
        


def get_player_name():
    """Handles player name input after 'Play Now' is clicked."""
    font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    player_name = ''
    cursor_visible = True
    cursor_timer = pygame.time.get_ticks()

    # Calculate the centered positions
    input_box = pygame.Rect(0, 0, 175, 50)
    input_box.center = (WIDTH // 2, HEIGHT // 2)

    submit_button = pygame.Rect(0, 0, 150, 60)
    submit_button.center = (WIDTH // 2, HEIGHT // 2 + 90)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                # If the user clicks inside the input box
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

                # If the user clicks the submit button
                if submit_button.collidepoint(event.pos):
                    return player_name

            if event.type == KEYDOWN:
                if active:
                    if event.key == K_RETURN:
                        return player_name
                    elif event.key == K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

        WIN.fill(BG_BLUE)

        # Draw the input box with white background
        pygame.draw.rect(WIN, WHITE, input_box)
        txt_surface = font.render(player_name, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        input_box.centerx = WIDTH // 2  # Adjust the center based on the new width
        WIN.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(WIN, color, input_box, 2)

        # Draw the submit button
        pygame.draw.rect(WIN, color_inactive, submit_button)
        button_text = button_font.render("Submit", True, BLACK)
        WIN.blit(button_text, (submit_button.x + (submit_button.width - button_text.get_width()) // 2, 
                               submit_button.y + (submit_button.height - button_text.get_height()) // 2))

        # Blinking cursor logic
        if active:
            current_time = pygame.time.get_ticks()
            if current_time - cursor_timer > 500:
                cursor_visible = not cursor_visible
                cursor_timer = current_time

            if cursor_visible:
                cursor_surface = font.render('|', True, color)
                WIN.blit(cursor_surface, (input_box.x + 5 + txt_surface.get_width(), input_box.y + 5))

        # Display the instructions to the player
        instruction_text = font.render("Enter your name:", True, BLACK)
        WIN.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 - 120))

        pygame.display.flip()





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
        
        # Update the display
        pygame.display.update()
        
        clock.tick(1)  # Slow down the game loop to one tick per second


def main():
    # Display the title screen
    title_screen()

    # Get the player's name via an input box
    player_name = get_player_name()

    # Guide the player with instructions
    guide_screen(WIN, WIDTH, HEIGHT, BG_BLUE)

    phases_screen(WIN, WIDTH, HEIGHT, BG_BLUE)
    
    status_screen(WIN, WIDTH, HEIGHT, BG_BLUE)

    # Load or create a player profile
    player = load_player()
    if player is None:
        player = create_player(player_name)
    
    dashboard_screen(WIN, WIDTH, HEIGHT, BG_BLUE, player)

    # Start the main game loop
    main_game_loop(player)


if __name__ == "__main__":
    main()

