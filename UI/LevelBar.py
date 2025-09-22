
import pygame

_FONT = None

def draw_level_progress(player, screen: pygame.Surface):
    global _FONT
    """
    Рисует уровень и полоску опыта игрока внизу слева,
    чуть выше панели с иконками оружия.
    """
    screen_w, screen_h = screen.get_size()

    # Размер полоски и отступы
    bar_width  = 180
    bar_height = 8
    margin_x   = 10
    margin_y   = 10

    # Положение иконок оружия
    icon_size  = 0
    icons_bottom = screen_h - margin_y
    icons_top    = icons_bottom - icon_size

    # Полоска опыта чуть выше иконок
    bar_x = margin_x
    bar_y = icons_top - margin_y - bar_height

    # Фон полоски
    bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
    pygame.draw.rect(screen, (50, 50, 50), bg_rect)

    # Заполненная часть
    if player.max_exp > 0:
        ratio = player.exp / player.max_exp
    else:
        ratio = 0
    fill_w = int(bar_width * ratio)
    fill_rect = pygame.Rect(bar_x, bar_y, fill_w, bar_height)
    pygame.draw.rect(screen, (100, 200, 100), fill_rect)

    if _FONT is None:
        pygame.font.init()
        _FONT = pygame.font.Font("Assets/Font/Caudex-Regular.ttf", 20)

    # Текст "LV X"
    txt_surf = _FONT.render(f"LVL. {player.level}", True, (220, 220, 220))
    txt_pos  = (bar_x, bar_y - margin_y - txt_surf.get_height())
    screen.blit(txt_surf, txt_pos)
