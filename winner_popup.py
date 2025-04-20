import pygame
import sys
from typing import Callable, Optional

# Use the same color values as the menu
ORANGE = (249, 181, 15)
BUTTON_FORE = (0, 36, 66)
BUTTON_BACK = (26, 183, 156)
BUTTON_HOVER = (34, 255, 217)
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (20, 50, 110)

def show_winner_popup(screen, winner: Optional[int], on_home: Callable = None, on_restart: Callable = None):
    popup_width, popup_height = 400, 200
    screen_width, screen_height = screen.get_size()

    popup_x = (screen_width - popup_width) // 2
    popup_y = (screen_height - popup_height) // 2

    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

    font = pygame.font.SysFont("arial", 36, bold=True)
    button_font = pygame.font.SysFont("arial", 28)

    button_width, button_height = 120, 50

    # Buttons
    home_button = pygame.Rect(
        popup_x + 40, popup_y + popup_height - 70, button_width, button_height
    )
    restart_button = pygame.Rect(
        popup_x + popup_width - button_width - 40,
        popup_y + popup_height - 70,
        button_width,
        button_height,
    )

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.collidepoint(event.pos):
                    return "home"  # Go back to home
                elif restart_button.collidepoint(event.pos):
                    if on_restart:
                        on_restart()  # Call the on_restart callback to restart the game
                    return "restart"  # Return restart trigger

        # Draw popup background
        pygame.draw.rect(screen, BACKGROUND_COLOR, popup_rect)
        pygame.draw.rect(screen, BUTTON_BACK, home_button, border_radius=10)
        pygame.draw.rect(screen, BUTTON_BACK, restart_button, border_radius=10)

        # Title text
        if winner is None:
            title = "It's a Draw!"
        else:
            title = f"{winner}"

        text_surface = font.render(title, True, ORANGE)
        screen.blit(
            text_surface,
            (
                popup_x + (popup_width - text_surface.get_width()) // 2,
                popup_y + 30,
            ),
        )

        # Button labels
        home_label = button_font.render("Home", True, BUTTON_FORE)
        restart_label = button_font.render("Restart", True, BUTTON_FORE)

        screen.blit(
            home_label,
            (
                home_button.x + (button_width - home_label.get_width()) // 2,
                home_button.y + 10,
            ),
        )
        screen.blit(
            restart_label,
            (
                restart_button.x + (button_width - restart_label.get_width()) // 2,
                restart_button.y + 10,
            ),
        )

        pygame.display.update()
        clock.tick(60)
