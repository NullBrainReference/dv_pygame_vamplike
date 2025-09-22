import pygame
from typing import Dict

_ICON_CACHE: Dict[str, pygame.Surface] = {}

def draw_weapon_icons(player, screen: pygame.Surface):
    screen_w, screen_h = screen.get_size()
    icon_size = 48
    spacing   = 10

    weapons = list(player.weapons.items())
    total_w = len(weapons) * (icon_size + spacing) - spacing
    start_x = (screen_w - total_w) // 2
    y       = screen_h - icon_size - 10

    for idx, (name, weapon) in enumerate(weapons):
        x    = start_x + idx * (icon_size + spacing)
        rect = pygame.Rect(x, y, icon_size, icon_size)

        icon_path = weapon.icon_path

        # загрузить или взять из кэша
        if icon_path not in _ICON_CACHE:
            surf = pygame.image.load(icon_path).convert_alpha()
            _ICON_CACHE[icon_path] = pygame.transform.scale(surf, (icon_size, icon_size))
        icon = _ICON_CACHE[icon_path]

        # рамка вокруг выбранного
        if name == player.selected_weapon:
            pygame.draw.rect(screen, (255, 215, 0), rect.inflate(4, 4), 2)

        # рисуем иконку
        screen.blit(icon, rect.topleft)