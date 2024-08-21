import pygame
import sys
from pygame.locals import QUIT, KEYDOWN, K_RETURN

def draw_guide_screen(WIN, WIDTH, HEIGHT, BG_COLOR):
    """Displays the guide screen with instructions."""
    WIN.fill(BG_COLOR)  # Set background color

    # Instructions text
    font = pygame.font.Font(None, 30)  # Reduced font size to 30
    instructions = [
        "Welcome to FinLitFun!",
        "Objective:",
        "The goal of FinLitFun is to retire as early as possible while maximizing",
        "your health, happiness, and Bank. Make wise decisions",
        "throughout your life to secure your future!",
        "Your player will start at age 16 with a randomly generated profile.",
        "Click next to view the game phases and make decisions that will",
        "impact your player's life.",
    ]

    # Display instructions
    y_offset = 80  # Increased top offset
    line_spacing = 35  # Reduced spacing between lines
    for line in instructions:
        text = font.render(line, True, (255, 255, 255))  # White text
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += line_spacing

    # Display "Press Enter to continue" message
    continue_text = font.render("Press Enter to continue...", True, (255, 255, 255))
    WIN.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT - 60))  # Adjusted position

    pygame.display.update()

def guide_screen(WIN, WIDTH, HEIGHT, BG_COLOR):
    """Handles the guide screen logic."""
    draw_guide_screen(WIN, WIDTH, HEIGHT, BG_COLOR)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:  # Continue when Enter is pressed
                    return  # Exit the guide screen and proceed to the game

        pygame.display.update()

def draw_phases_screen(WIN, WIDTH, HEIGHT, BG_COLOR):
    """Displays the game phases screen with instructions."""
    WIN.fill(BG_COLOR)  # Set background color

    # Instructions text for game phases
    font = pygame.font.Font(None, 30)  # Reduced font size to 30
    phase_instructions = [
        "Game Phases:",
        "1. Early Life (Ages 16-22):",
        "   - Start with part-time jobs and build credit.",
        "   - Open a checking account and save money.",
        "   - Optionally, become an authorized user on parents' credit card.",
        "",
        "2. Young Adult (Ages 23-30):",
        "   - Advance education or skills for better job opportunities.",
        "   - Invest in real estate or retirement accounts.",
        "   - Make career decisions that impact your future.",
        "",
        "3. Mid-Life (Ages 31 and beyond):",
        "   - Focus on career growth and sound investments.",
        "   - Plan for retirement and maintain health and happiness.",
        "   - Manage major life events like starting a family.",
    ]

    # Display phase instructions
    y_offset = 50  # Increased top offset
    line_spacing = 30  # Reduced spacing between lines
    for line in phase_instructions:
        text = font.render(line, True, (255, 255, 255))  # White text
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += line_spacing

    # Display "Press Enter to continue" message
    continue_text = font.render("Press Enter to continue...", True, (255, 255, 255))
    WIN.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT - 60))  # Adjusted position

    pygame.display.update()

def phases_screen(WIN, WIDTH, HEIGHT, BG_COLOR):
    """Handles the game phases screen logic."""
    draw_phases_screen(WIN, WIDTH, HEIGHT, BG_COLOR)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:  # Continue when Enter is pressed
                    return  # Exit the phases screen and proceed to the game

        pygame.display.update()

def draw_status_screen(WIN, WIDTH, HEIGHT, BG_COLOR):
    """Displays the managing status, decision making, and random events screen."""
    WIN.fill(BG_COLOR)  # Set background color

    # Instructions text for managing status, decision making, and random events
    font = pygame.font.Font(None, 30)  # Reduced font size to 30
    status_instructions = [
        "Managing Status:",
        "   - Health: Stay healthy by balancing work and personal time.",
        "   - Happiness: Enjoy life by taking vacations and engaging in hobbies.",
        "   - Bank: Build wealth by managing assets and debts.",
        "",
        "Decision Making:",
        "   - Make career, education, and investment choices wisely.",
        "   - Each decision affects your health, happiness, and finances.",
        "",
        "Random Events:",
        "   - Be prepared for emergencies, promotions, and opportunities.",
        "   - Handle unexpected events that can change your life.",
        "",
        "Winning the Game:",
        "Aim to retire as early as possible with the highest health, happiness, and Bank.",
        "Decisions throughout the game will shape your player's life and determine success.",
        "Good luck! When you are ready, hit Enter to start the game.",
        "Press Enter to start the game..."
    ]

    # Display status instructions
    y_offset = 50  # Increased top offset
    line_spacing = 30  # Reduced spacing between lines
    for line in status_instructions:
        text = font.render(line, True, (255, 255, 255))  # White text
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += line_spacing

    pygame.display.update()

def status_screen(WIN, WIDTH, HEIGHT, BG_COLOR):
    """Handles the guide for status, decision making, and random events logic."""
    draw_status_screen(WIN, WIDTH, HEIGHT, BG_COLOR)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:  # Continue when Enter is pressed
                    return  # Exit the status screen and proceed to the game

        pygame.display.update()

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("FinLitFun Guide")
    BG_COLOR = (0, 0, 0)  # Black background

    # Display guide screen
    guide_screen(WIN, WIDTH, HEIGHT, BG_COLOR)

    # Display game phases screen
    phases_screen(WIN, WIDTH, HEIGHT, BG_COLOR)

    # Display managing status, decision making, and random events screen
    status_screen(WIN, WIDTH, HEIGHT, BG_COLOR)

    # Proceed to the game (main game loop would go here)
    print("Game starts now...")

if __name__ == "__main__":
    main()


