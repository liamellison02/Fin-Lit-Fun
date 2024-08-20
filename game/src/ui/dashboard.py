import pygame
import pygame.gfxdraw
import sys
from pygame.locals import QUIT

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

def draw_game_menu(win, width, height, margin):
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
    
    win.blit(left_box, (left_box_x, left_box_y))

def draw_status_menu(win, width, height, margin):
    """Draws the status menu box (top right corner with rounded corners)."""
    top_right_box_width = width // 2 - 2 * margin # Increased width
    top_right_box_height = 180
    top_right_box_x = width - top_right_box_width - margin
    top_right_box_y = margin

    top_right_box = pygame.Surface((top_right_box_width, top_right_box_height), pygame.SRCALPHA)
    
    # Draw a black border around the box
    border_rect = pygame.Rect(0, 0, top_right_box_width, top_right_box_height)
    draw_rounded_rect(top_right_box, (0, 0, 0), border_rect, corner_radius=20)
    
    # Draw the rounded box inside the border
    inner_rect = border_rect.inflate(-4, -4)  # Reduce size for the inner box
    draw_rounded_rect(top_right_box, (111, 128, 145), inner_rect, corner_radius=20)
    
    win.blit(top_right_box, (top_right_box_x, top_right_box_y))

def draw_detail_menu(win, width, height, margin):
    """Draws the detail menu box (bottom right corner)."""
    bottom_right_box_width = width // 2 - 2 * margin # Increased width
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

def draw_dashboard_screen(win, width, height, bg_color):
    """Draws the dashboard screen with three sections."""
    win.fill(bg_color)  # Set background color
    
    margin = 10
    
    # Draw the game menu, status menu, and detail menu
    draw_game_menu(win, width, height, margin)
    draw_status_menu(win, width, height, margin)
    draw_detail_menu(win, width, height, margin)
    
    pygame.display.update()

def dashboard_screen(win, width, height, bg_color):
    """Handles the dashboard screen logic."""
    draw_dashboard_screen(win, width, height, bg_color)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Add logic for handling interactions here (e.g., button clicks)
        
        pygame.display.update()

# Initialize Pygame and create a window to test
pygame.init()
width, height = 800, 600
window = pygame.display.set_mode((width, height))
dashboard_screen(window, width, height, (111, 128, 145))  # Example background color
