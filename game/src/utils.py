import pygame
import json
from enum import Enum

WHITE = (255, 255, 255)


class DataPath(Enum):
    PLAYER = "../data/player.json"
    ASSETS = "../data/assets.json"
    LIABILITIES = "../data/liabilities.json"
    EDUCATION = "../data/education.json"
    OCCUPATIONS = "../data/occupations.json"
    EVENTS = "../data/events.json"
    INVESTMENTS = "../data/investments.json"
    FONT_VIRGIL = "../assets/fonts/Virgil-GS-Regular.ttf"


def load_json(path: DataPath):
    p = path.value
    try:
        with open(p, "r") as file:
            content = json.load(file)
        return content
    except:
        print(f"Error loading {p}")
        return None


# TODO - set output to UI instead of console
def prompt_user(prompt: str, options: list, input_message: str = "Enter the number of your choice: "):
    """Given a prompt and available options, returns user's decision."""
    print(prompt)  # outputs to a popup menu
    print('\n')

    valid_inputs = set()
    i = 1

    for d in options:
        # outputs decision name to a popup menu
        print(f'{i}. {d["id"]}')  

        # outputs decision attributes to the overview panel
        for k, v in d.items():
            if k == 'id':
                continue
            print(f'{k}: {v}')  
            
        valid_inputs.add(str(i))
        i += 1

    choice = input(input_message)
    while choice not in valid_inputs:
        print(f"Invalid input: {choice}; Please enter a valid number.")
        choice = input(input_message)
    
    choice = int(choice) - 1
    return options[choice]


def draw_status_bar(surface, x, y, value, max_value, color):
    """Draws a status bar representing a value out of a maximum."""
    pygame.draw.rect(surface, color, (x, y, 200, 20))
    pygame.draw.rect(surface, WHITE, (x, y, 200 * (1 - value / max_value), 20))


def draw_button(button_font_size: int, win: pygame.surface.Surface, width: int, height: int, button_color, left: int, top: int):
    button_font = pygame.font.Font(None, button_font_size)
    button_text = button_font.render("Play Now", True, (255, 255, 255))  
    
  
    button_rect = pygame.Rect(width // 2 - 100, height // 2 + 90, 200, 60)
    
   
    pygame.draw.rect(win, button_color, button_rect)  
    
    
    win.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2, 
                           button_rect.y + (button_rect.height - button_text.get_height()) // 2))
    