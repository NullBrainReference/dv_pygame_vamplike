import pygame

# UI/HPBar.py
def draw_hp_bar(screen, unit, pos: pygame.Vector2):

    bar_width  = 40
    bar_height = 6
    pct        = unit.hp / unit.max_hp
    health_rect = pygame.Rect(
        pos.x - bar_width // 2,
        pos.y,
        int(bar_width * pct),
        bar_height
    )
    bg_rect = pygame.Rect(
        pos.x - bar_width // 2,
        pos.y,
        bar_width,
        bar_height
    )
    pygame.draw.rect(screen, (60, 60, 60), bg_rect)
    pygame.draw.rect(screen, (0, 255, 0), health_rect)
