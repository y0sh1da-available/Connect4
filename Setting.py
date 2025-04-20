import sys
import os
import pygame

# Thêm thư mục hiện tại vào sys.path để import các module cùng cấp
HERE = os.path.dirname(__file__)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import config


def show_settings_screen(screen):
    # Late import để tránh circular import với menu.py
    from menu import Button, FONT, BUTTON_BACK, BUTTON_FORE, BUTTON_HOVER

    clock = pygame.time.Clock()
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

    # Nút Thoát
    exit_button = Button(
        "←",
        (20, SCREEN_HEIGHT - 60, 40, 40),
        FONT,
        color=BUTTON_BACK,
        bg_color=BUTTON_FORE
    )

    # Nút bật/tắt âm lượng, hiển thị theo trạng thái
    volume_button = Button(
        "Mute" if config.sound_on else "Unmute",
        (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 30, 160, 60),
        FONT,
        color=BUTTON_FORE if config.sound_on else BUTTON_BACK,
        bg_color=BUTTON_BACK if config.sound_on else BUTTON_HOVER
    )

    # Thiết lập âm lượng ban đầu
    pygame.mixer.music.set_volume(1.0 if config.sound_on else 0.0)

    running = True
    while running:
        screen.fill(BUTTON_FORE)

        exit_button.draw(screen)
        volume_button.draw(screen)

        status_text = f"Volume: {'On' if config.sound_on else 'Off'}"
        status_label = FONT.render(status_text, True, BUTTON_HOVER)
        status_rect = status_label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
        screen.blit(status_label, status_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if exit_button.is_clicked(event):
                running = False

            if volume_button.is_clicked(event):
                # Đổi trạng thái và volume
                config.sound_on = not config.sound_on
                pygame.mixer.music.set_volume(1.0 if config.sound_on else 0.0)

                # Cập nhật nút volume
                volume_button.text = "Mute" if config.sound_on else "Unmute"
                volume_button.bg_color = BUTTON_BACK if config.sound_on else BUTTON_HOVER
                volume_button.color = BUTTON_FORE

        pygame.display.update()
        clock.tick(60)
