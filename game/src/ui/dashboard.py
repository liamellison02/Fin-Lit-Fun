import pygame
import pygame.gfxdraw
import sys
from pygame.locals import QUIT
from utils import draw_status_bar 

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

    font = pygame.font.Font(None, 32)

    label_color = (255, 255, 255)  # White color for labels

    # Set up font for age label
    age_label = font.render("Age", True, label_color)
    padding = 10  # General padding for the contents
    top_left_margin = 20  # Additional margin for top and left

    financial_status_label_rect = pygame.Rect(0, 0, 0, 0)  # Dummy rect for position

    # Position the age label with extra margin from the top and left
    age_label_rect = age_label.get_rect(topleft=(padding + top_left_margin, financial_status_label_rect.bottom + padding + top_left_margin))
    left_box.blit(age_label, age_label_rect)

    # Render the player's age from JSON
    age_number = font.render(str(player['age']), True, label_color)
    age_number_rect = age_number.get_rect(topleft=(age_label_rect.right + padding, age_label_rect.top))
    left_box.blit(age_number, age_number_rect)

    win.blit(left_box, (left_box_x, left_box_y))


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
    font = pygame.font.Font(None, 24)
    label_color = (255, 255, 255)  # White color for labels
    
    # Render Health label with padding
    health_label = font.render("Health:", True, label_color)
    health_label_rect = health_label.get_rect(topleft=(padding, padding))
    top_right_box.blit(health_label, health_label_rect)
    
    # Render Happiness label with padding
    happiness_label = font.render("Happiness:", True, label_color)
    happiness_label_rect = happiness_label.get_rect(topleft=(padding, health_label_rect.bottom + padding))
    top_right_box.blit(happiness_label, happiness_label_rect)

    # Render Financial Status label with padding
    financial_status_label = font.render("Bank Account:", True, label_color)
    financial_status_number = font.render(str(player['financial_status']), True, label_color)
    financial_status_label_rect = financial_status_label.get_rect(topleft=(padding, happiness_label_rect.bottom + padding))
    top_right_box.blit(financial_status_label, financial_status_label_rect)
    
    # Render the financial status number from JSON
    financial_status_number_rect = financial_status_number.get_rect(topleft=(financial_status_label_rect.right + padding, happiness_label_rect.bottom + padding))
    top_right_box.blit(financial_status_number, financial_status_number_rect)
    
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
    
    # Draw the game menu, status menu, and detail menu
    draw_game_menu(win, width, height, margin, player)
    draw_status_menu(win, width, height, margin, player)  # Pass player object here
    draw_detail_menu(win, width, height, margin)
    
    pygame.display.update()

def dashboard_screen(win, width, height, bg_color, player):
    """Handles the dashboard screen logic."""
    draw_dashboard_screen(win, width, height, bg_color, player)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Add logic for handling interactions here (e.g., button clicks)
        
        pygame.display.update()
