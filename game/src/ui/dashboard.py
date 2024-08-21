import pygame
import pygame.gfxdraw
import sys
from pygame.locals import QUIT, KEYDOWN, K_s, MOUSEBUTTONDOWN
from player import save_player
from utils import draw_status_bar, load_json, DataPath
from phases import early_life_phase, young_adult_phase, mid_life_phase
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

    # Set up font for occupation label
    occupation_label = font.render("Occupation", True, label_color)
    padding = 10  # General padding for the contents
    top_left_margin = 20  # Additional margin for top and left

    bank_label_rect = pygame.Rect(0, 0, 0, 0)  # Dummy rect for position

    # Position the occupation label below the age label
    occupation_label_rect = occupation_label.get_rect(topleft=(padding + top_left_margin, age_label_rect.bottom + padding))
    left_box.blit(occupation_label, occupation_label_rect)

    # Render the player's occupation from JSON
    occupation = font.render(str(player["occupation"]), True, label_color)
    occupation_rect = occupation.get_rect(topleft=(occupation_label_rect.right + padding, occupation_label_rect.top))
    left_box.blit(occupation, occupation_rect)

    # Draw "Continue" button with rounded corners
    button_font = pygame.font.Font(FONT_VIRGIL, 24)
    button_text = button_font.render("Continue", True, label_color)
    
    # Position the button right next to the age number
    button_rect = pygame.Rect(age_number_rect.right + padding + 40, age_number_rect.top - 10, 185, 60)

    # Draw the rounded rectangle button
    draw_rounded_rect(left_box, BLUE, button_rect, corner_radius=20)
    
    # Center the button text inside the rounded rectangle
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

def draw_prompt_menu(win, width, height, margin, prompt, options, player):
    """Displays a decision prompt with clickable options centered on the screen."""
    font = pygame.font.Font(FONT_VIRGIL, 24)
    label_color = (255, 255, 255)
    BLUE = (0, 0, 255)

    # Calculate the dimensions of the prompt box
    prompt_box_width = width - 2 * margin
    option_height = 50  # Height for each option button
    prompt_box_height = option_height * len(options) + 3 * margin  # Adjust height based on the number of options
    prompt_box_x = (width - prompt_box_width) // 2
    prompt_box_y = (height - prompt_box_height) // 2

    # Create the prompt box surface
    prompt_box = pygame.Surface((prompt_box_width, prompt_box_height), pygame.SRCALPHA)

    # Draw the prompt box
    border_rect = pygame.Rect(0, 0, prompt_box_width, prompt_box_height)
    draw_rounded_rect(prompt_box, (0, 0, 0), border_rect, corner_radius=20)
    inner_rect = border_rect.inflate(-4, -4)
    draw_rounded_rect(prompt_box, (111, 128, 145), inner_rect, corner_radius=20)

    # Render the prompt text and center it horizontally
    prompt_text = font.render(prompt, True, label_color)
    prompt_text_rect = prompt_text.get_rect(center=(prompt_box_width // 2, margin))
    prompt_box.blit(prompt_text, prompt_text_rect)

    # Render options as buttons and center them horizontally
    option_rects = []
    for i, option in enumerate(options):
        option_id = option.get("id", "Unnamed Option")  # Safely get the id or provide a default
        option_text = font.render(option_id, True, label_color)
        option_rect = pygame.Rect((prompt_box_width - 300) // 2, prompt_text_rect.bottom + margin + i * option_height, 300, 40)
        pygame.draw.rect(prompt_box, BLUE, option_rect)
        option_text_rect = option_text.get_rect(center=option_rect.center)
        prompt_box.blit(option_text, option_text_rect)
        option_rects.append((option_rect, option))

    # Blit the prompt box to the window
    win.blit(prompt_box, (prompt_box_x, prompt_box_y))
    pygame.display.update()

    return option_rects

def display_message(win, message, font, position, color=(255, 255, 255)):
    """Displays a message on the screen at the specified position."""
    text_surface = font.render(message, True, color)
    win.blit(text_surface, position)
    pygame.display.update()



def dashboard_screen(win, width, height, bg_color, player):
    """Handles the dashboard screen logic."""
    button_rect = draw_dashboard_screen(win, width, height, bg_color, player)
    
    events = load_json(DataPath.EVENTS)
    occupations = load_json(DataPath.OCCUPATIONS)

    font = pygame.font.Font(FONT_VIRGIL, 24)  
    
    clock = pygame.time.Clock()

    decision_made = False
    options_rects = []
    decision_data = None

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_s:
                    save_player(player)
                    display_message(win, "Game saved!", font, (50, 50))  
            if event.type == MOUSEBUTTONDOWN:
                if len(options_rects) > 0:
                    for option_rect, option in options_rects:
                        if option_rect.collidepoint(event.pos):
                            decision_data = option
                            decision_made = True
                            options_rects = []
                            break
                elif button_rect and button_rect.collidepoint(event.pos):
                    player = handle_turn(player, events, occupations)
                    button_rect = draw_dashboard_screen(win, width, height, bg_color, player)

        if decision_made:
            if player["age"] < 23:
                player = early_life_phase(player)
            elif player["age"] < 31:
                player = young_adult_phase(player)
            else:
                player = mid_life_phase(player)
            
            if decision_data["id"] == "High School":
                occupations = load_json(DataPath.OCCUPATIONS)
                occupation_options = occupations[0]["occupations"]
                options_rects = draw_prompt_menu(win, width, height, 20, "Choose your career path:", occupation_options)
                player['occupation'] = decision_data
                income_key = "Starting Income" if "Starting Income" in decision_data else "Est. Start Income"
                player['income'] = decision_data[income_key]
            else:
                player['skills']['education'] = decision_data["id"]
                player['bank'] -= decision_data["Cost"]
                income_key = "Starting Income" if "Starting Income" in decision_data else "Est. Start Income"
                player['income'] = decision_data[income_key]
            
            decision_made = False
            options_rects = []
            
            button_rect = draw_dashboard_screen(win, width, height, bg_color, player)

        pygame.display.update()
        clock.tick(1)
