import pygame

def draw_hp_bar(screen, unit, offset_y=10, width=40, height=6):
    x = unit.pos.x + 10 - width // 2  # центр над юнитом
    y = unit.pos.y - offset_y

    hp_ratio = unit.hp / unit.max_hp
    hp_color = (0, 255, 0) if hp_ratio > 0.5 else (255, 255, 0) if hp_ratio > 0.2 else (255, 0, 0)

    pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))  # фон
    pygame.draw.rect(screen, hp_color, (x, y, int(width * hp_ratio), height))  # HP
    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 1)  # рамка

