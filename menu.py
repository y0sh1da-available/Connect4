import os
import sys
import pygame
import HuongDan
import Setting
import game

# Setup paths
HERE = os.path.dirname(__file__)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import config

# Initialize Pygame
pygame.init()

# Colors
ORANGE = (249, 181, 15)
BUTTON_FORE = (0, 36, 66)
BUTTON_BACK = (26, 183, 156)
BUTTON_HOVER = (34, 255, 217)
WHITE = (255, 255, 255)

# Fonts
TITLE_FONT = pygame.font.SysFont('arial', 60, bold=True)
FONT = pygame.font.SysFont('arial', 40, bold=True)
SMALL_FONT = pygame.font.SysFont('arial', 24, bold=True)


class Button:
    def __init__(self, text, rect, font, color=BUTTON_FORE, bg_color=BUTTON_BACK, image=None):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.font = font
        self.color = color
        self.bg_color = bg_color
        self.hover_color = BUTTON_HOVER
        self.default_color = bg_color
        self.image = image

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        if self.image:
            if self.rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, self.hover_color, self.rect, border_radius=8)
            else:
                pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=8)
            img_rect = self.image.get_rect(center=self.rect.center)
            screen.blit(self.image, img_rect)
        else:
            color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.bg_color
            pygame.draw.rect(screen, color, self.rect, border_radius=12)
            text_surf = self.font.render(self.text, True, self.color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


def show_difficulty_menu(screen):
    clock = pygame.time.Clock()
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

    easy_button = Button("Easy", (200, 200, 200, 60), FONT)
    medium_button = Button("Medium", (200, 280, 200, 60), FONT)
    hard_button = Button("Hard", (200, 360, 200, 60), FONT)
    back_button = Button("Back", (200, 440, 200, 60), FONT)

    background_image = pygame.image.load("background.png").convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    selecting = True
    while selecting:
        screen.blit(background_image, (0, 0))
        label = FONT.render("Select Difficulty", True, ORANGE)
        screen.blit(label, label.get_rect(center=(SCREEN_WIDTH // 2, 120)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.is_clicked(event):
                    config.difficulty = "Easy"
                    selecting = False
                elif medium_button.is_clicked(event):
                    config.difficulty = "Medium"
                    selecting = False
                elif hard_button.is_clicked(event):
                    config.difficulty = "Hard"
                    selecting = False
                elif back_button.is_clicked(event):
                    return main_menu()

        easy_button.draw(screen)
        medium_button.draw(screen)
        hard_button.draw(screen)
        back_button.draw(screen)

        pygame.display.update()
        clock.tick(60)


def main_menu():
    SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Four in a row")

    background_image = pygame.image.load("background.png").convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    click_sound = pygame.mixer.Sound(os.path.join(HERE, "click.mp3"))

    settings_icon = pygame.image.load("Setting.png").convert_alpha()
    settings_icon = pygame.transform.scale(settings_icon, (24, 24))

    pvp_button = Button("Player vs Player", (150, 200, 300, 60), FONT)
    pvb_button = Button("Player vs Bot", (150, 280, 300, 60), FONT)
    help_button = Button("?", (SCREEN_WIDTH - 90, 20, 40, 40), SMALL_FONT, color=BUTTON_FORE, bg_color=BUTTON_BACK)
    settings_button = Button("", (SCREEN_WIDTH - 50, 20, 40, 40), SMALL_FONT, image=settings_icon)
    exit_button = Button("Exit", (150, 500, 300, 60), FONT)

    label = TITLE_FONT.render("Four in a row", True, ORANGE)
    label_rect = label.get_rect(center=(SCREEN_WIDTH // 2, 100))

    running = True
    while running:
        screen.blit(background_image, (0, 0))
        screen.blit(label, label_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if config.sound_on:
                    click_sound.play()

                if pvp_button.is_clicked(event):
                    game.run_game(pvp=True)
                    return

                if pvb_button.is_clicked(event):
                    show_difficulty_menu(screen)
                    if config.difficulty in ["Easy", "Medium", "Hard"]:
                        game.run_game(pvp=False)
                        return

                if help_button.is_clicked(event):
                    HuongDan.show_help_screen(screen)

                if settings_button.is_clicked(event):
                    Setting.show_settings_screen(screen)

                if exit_button.is_clicked(event):
                    running = False

        pvp_button.draw(screen)
        pvb_button.draw(screen)
        help_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_menu()
