import pygame
import sys

# === Colors from menu.py ===
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
ORANGE = (249, 181, 15)
BUTTON_FORE = (0, 36, 66)
BUTTON_BACK = (26, 183, 156)
BUTTON_HOVER = (34, 255, 217)

# Fonts from menu.py
pygame.init()
FONT = pygame.font.SysFont('Segoe UI', 40, bold=True)
SMALL_FONT = pygame.font.SysFont('Segoe UI', 24, bold=True)

def draw_exit_button(screen, y_offset, hover=False):
    button_width = 160
    button_height = 50
    screen_width = screen.get_width()

    x = (screen_width - button_width) // 2
    y = y_offset

    button_rect = pygame.Rect(x, y, button_width, button_height)

    # Shadow
    shadow_rect = button_rect.copy()
    shadow_rect.move_ip(4, 4)
    pygame.draw.rect(screen, (180, 180, 180), shadow_rect, border_radius=12)

    # Button
    color = BUTTON_HOVER if hover else BUTTON_BACK
    pygame.draw.rect(screen, color, button_rect, border_radius=12)

    label = SMALL_FONT.render("Thoát", True, BUTTON_FORE)
    label_rect = label.get_rect(center=button_rect.center)
    screen.blit(label, label_rect)

    return button_rect

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + ' '
    if current_line:
        lines.append(current_line.strip())
    return lines

def show_help_screen(screen):
    help_running = True
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))  # translucent overlay

    box_width = min(720, screen_width - 40)
    box_height = 420
    box_x = (screen_width - box_width) // 2
    box_y = 80
    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

    while help_running:
        screen.blit(overlay, (0, 0))

        shadow_rect = box_rect.copy()
        shadow_rect.move_ip(6, 6)
        pygame.draw.rect(screen, (180, 180, 180), shadow_rect, border_radius=25)
        pygame.draw.rect(screen, WHITE, box_rect, border_radius=25)

        title = FONT.render("Hướng Dẫn Chơi", True, BUTTON_FORE)
        title_rect = title.get_rect(center=(screen_width // 2, box_y + 50))
        screen.blit(title, title_rect)

        content_lines = [
            "1. Click chuột vào một cột để thả quân cờ.",
            "2. Trò chơi luân phiên giữa 2 người chơi.",
            "3. Người thắng là người có 4 quân liền nhau theo hàng ngang, dọc hoặc chéo."
        ]

        max_line_width = box_width - 60
        y_offset = box_y + 120
        for line in content_lines:
            wrapped = wrap_text(line, SMALL_FONT, max_line_width)
            for sub_line in wrapped:
                rendered = SMALL_FONT.render(sub_line, True, BUTTON_FORE)
                screen.blit(rendered, (box_x + 30, y_offset))
                y_offset += 30

        mouse_pos = pygame.mouse.get_pos()
        hover = False
        button_y = box_y + box_height + 20
        exit_button_rect = draw_exit_button(screen, y_offset=button_y, hover=False)

        if exit_button_rect.collidepoint(mouse_pos):
            exit_button_rect = draw_exit_button(screen, y_offset=button_y, hover=True)
            hover = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and hover:
                help_running = False

        pygame.display.update()
