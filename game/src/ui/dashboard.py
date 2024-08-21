import pygame
import pygame.gfxdraw
import sys

from pygame.locals import QUIT, KEYDOWN, K_s, K_l, MOUSEBUTTONDOWN, K_RETURN, K_BACKSPACE
from player import create_player, save_player
from utils import draw_status_bar, draw_button, load_json, DataPath

from handle import handle_turn

FONT_VIRGIL = str(DataPath.FONT_VIRGIL.value)


def draw_rounded_rect(surface, color, rect, corner_radius):
    """Draws a rectangle with rounded corners."""
    pygame.gfxdraw.aacircle(surface, rect.x + corner_radius, rect.y + corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right - corner_radius - 1, rect.y + corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.x + corner_radius, rect.bottom - corner_radius - 1, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right - corner_radius - 1, rect.bottom - corner_radius - 1, corner_radius, color)

    pygame.gfxdraw.filled_circle(surface, rect.x + corner_radius, rect.y + corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right - corner_radius - 1, rect.y + corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.x + corner_radius, rect.bottom - corner_radius - 1, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right - corner_radius - 1, rect.bottom - corner_radius - 1, corner_radius, color)

    pygame.draw.rect(surface, color, rect.inflate(-2*corner_radius, 0))
    pygame.draw.rect(surface, color, rect.inflate(0, -2*corner_radius))


def draw_game_menu(win, width, height, margin, player):
    """Draws the game menu box (left half of the screen)."""
    left_box_width = width // 2 - 2 * margin
    left_box_height = height - 2 * margin
    left_box_x = margin
    left_box_y = margin

    left_box = pygame.Surface((left_box_width, left_box_height), pygame.SRCALPHA)
    
    # Draw a black border around the box
    border_rect = pygame.Rect(0, 0, left_box_width, left_box_height)
    draw_rounded_rect(left_box, (0, 0, 0), border_rect, corner_radius=20)
    
    # Draw the rounded box inside the border
    inner_rect = border_rect.inflate(-4, -4)  # Reduce size for the inner box
    draw_rounded_rect(left_box, (111, 128, 145), inner_rect, corner_radius=20)

    font = pygame.font.Font(FONT_VIRGIL, 32)

    label_color = (255, 255, 255)  # White color for labels
    BLUE = (0, 0, 255)  # Blue color for buttons

    # Set up font for age label
    age_label = font.render("Age", True, label_color)
    padding = 10  # General padding for the contents
    top_left_margin = 20  # Additional margin for top and left

    bank_label_rect = pygame.Rect(0, 0, 0, 0)  # Dummy rect for position

    # Position the age label with extra margin from the top and left
    age_label_rect = age_label.get_rect(topleft=(padding + top_left_margin, bank_label_rect.bottom + padding + top_left_margin))
    left_box.blit(age_label, age_label_rect)

    # Render the player's age from JSON
    age_number = font.render(str(player["age"]), True, label_color)
    age_number_rect = age_number.get_rect(topleft=(age_label_rect.right + padding, age_label_rect.top))
    left_box.blit(age_number, age_number_rect)

    # Draw "Continue" button
    button_font = pygame.font.Font(FONT_VIRGIL, 24)
    button_text = button_font.render("Continue", True, label_color)
    
    # Position the button right next to the age number
    button_rect = pygame.Rect(age_number_rect.right + padding, age_number_rect.top, 200, 60)
    pygame.draw.rect(left_box, BLUE, button_rect)
    left_box.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2, 
                                button_rect.y + (button_rect.height - button_text.get_height()) // 2))

    win.blit(left_box, (left_box_x, left_box_y))

    return button_rect  # Return the button's rect for click detection


    
   
def draw_status_menu(win, width, height, margin, player):
    """Draws the status menu box (top right corner with rounded corners)."""
    top_right_box_width = width // 2 - 2 * margin  # Increased width
    top_right_box_height = 180
    top_right_box_x = width - top_right_box_width - margin
    top_right_box_y = margin
    
    padding = 25  # Define padding for the inner content

    top_right_box = pygame.Surface((top_right_box_width, top_right_box_height), pygame.SRCALPHA)
    
    # Draw a black border around the box
    border_rect = pygame.Rect(0, 0, top_right_box_width, top_right_box_height)
    draw_rounded_rect(top_right_box, (0, 0, 0), border_rect, corner_radius=20)
    
    # Draw the rounded box inside the border
    inner_rect = border_rect.inflate(-4, -4)  # Reduce size for the inner box
    draw_rounded_rect(top_right_box, (111, 128, 145), inner_rect, corner_radius=20)
    
    # Set up font
    font = pygame.font.Font(FONT_VIRGIL, 24)
    label_color = (255, 255, 255)  # White color for labels
    
    # Render Health label with padding
    health_label = font.render("Health:", True, label_color)
    health_label_rect = health_label.get_rect(topleft=(padding, padding))
    top_right_box.blit(health_label, health_label_rect)
    
    # Render Happiness label with padding
    happiness_label = font.render("Happiness:", True, label_color)
    happiness_label_rect = happiness_label.get_rect(topleft=(padding, health_label_rect.bottom + padding))
    top_right_box.blit(happiness_label, happiness_label_rect)

    # Render Bank label with padding
    bank_label = font.render("Bank Account:", True, label_color)
    bank_number = font.render(f'${player["bank"]:.2f}', True, label_color)
    bank_label_rect = bank_label.get_rect(topleft=(padding, happiness_label_rect.bottom + padding))
    top_right_box.blit(bank_label, bank_label_rect)
    
    # Render the Bank number from JSON
    bank_number_rect = bank_number.get_rect(topleft=(bank_label_rect.right + padding, happiness_label_rect.bottom + padding))
    top_right_box.blit(bank_number, bank_number_rect)
    
    # Align the status bars to the right of the box, considering padding
    bar_x = top_right_box_width - (220 + padding)  # Adjust this value to align the bars to the right
    
    # Draw the status bars with padding
    draw_status_bar(top_right_box, bar_x, padding, player['health'], 100, (255, 0, 0))  # Red for Health
    draw_status_bar(top_right_box, bar_x, happiness_label_rect.top, player['happiness'], 100, (0, 255, 0))  # Green for Happiness
    
    win.blit(top_right_box, (top_right_box_x, top_right_box_y))


def draw_detail_menu(win, width, height, margin):
    """Draws the detail menu box (bottom right corner)."""
    bottom_right_box_width = width // 2 - 2 * margin 
    bottom_right_box_height = height - 2 * margin - 200
    bottom_right_box_x = width - bottom_right_box_width - margin
    bottom_right_box_y = height - bottom_right_box_height - margin

    bottom_right_box = pygame.Surface((bottom_right_box_width, bottom_right_box_height), pygame.SRCALPHA)
    
    # Draw a black border around the box
    border_rect = pygame.Rect(0, 0, bottom_right_box_width, bottom_right_box_height)
    draw_rounded_rect(bottom_right_box, (0, 0, 0), border_rect, corner_radius=20)
    
    # Draw the rounded box inside the border
    inner_rect = border_rect.inflate(-4, -4)  # Reduce size for the inner box
    draw_rounded_rect(bottom_right_box, (111, 128, 145), inner_rect, corner_radius=20)
    
    win.blit(bottom_right_box, (bottom_right_box_x, bottom_right_box_y))


def draw_dashboard_screen(win, width, height, bg_color, player):
    """Draws the dashboard screen with three sections."""
    win.fill(bg_color)  # Set background color
    
    margin = 10
    
    # Draw the game menu and get the button rect
    button_rect = draw_game_menu(win, width, height, margin, player)
    
    # Draw the status menu and detail menu
    draw_status_menu(win, width, height, margin, player)
    draw_detail_menu(win, width, height, margin)
    
    pygame.display.update()

    return button_rect  # Return the button rect



def dashboard_screen(win, width, height, bg_color, player):
    """Handles the dashboard screen logic."""
    button_rect = draw_dashboard_screen(win, width, height, bg_color, player)
    
    events = load_json(DataPath.EVENTS)
    occupations = load_json(DataPath.OCCUPATIONS)

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
            if event.type == MOUSEBUTTONDOWN:
                if button_rect and button_rect.collidepoint(event.pos):  # Check if the click is within the button's rect
                    # Handle a turn in the game
                    player = handle_turn(player, events, occupations)
                    # Redraw the screen with the updated player data
                    button_rect = draw_dashboard_screen(win, width, height, bg_color, player)  # Update button_rect after redraw
        
        # Update the display
        pygame.display.update()
        
        clock.tick(1)  # Slow down the game loop to one tick per second

