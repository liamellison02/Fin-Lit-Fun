import pygame

# TODO - set output to UI instead of console
def prompt_user(prompt: str, decisions: dict, input_message: str = "Enter the number of your choice: "):
    """Given a prompt and available options (decisions), returns user's decision."""
    print(prompt)  # outputs to a popup menu
    print('\n')

    valid_inputs = set()
    i = 1

    for k1, v1 in decisions:
        # outputs decision name to a popup menu
        print(f'{i}. {k1}')  

        # outputs decision attributes to the overview panel
        for k2, v2 in v1:
            print(f'{k2}: {v2}')  
            
        valid_inputs.add(str(i))
        i += 1

    choice = input(input_message)
    while choice not in valid_inputs:
        print(f"Invalid input: {choice}; Please enter a valid number.")
        choice = input(input_message)
    
    choice = int(choice) - 1
    return decisions[choice]

WHITE = (255, 255, 255)

def draw_status_bar(surface, x, y, value, max_value, color):
    """Draws a status bar representing a value out of a maximum."""
    pygame.draw.rect(surface, color, (x, y, 200, 20))
    pygame.draw.rect(surface, WHITE, (x, y, 200 * (1 - value / max_value), 20))
