# Effects/BonusSelectorEffect.py

import pygame
from Events.EventBus import bus
from Events.Events import BonusSelected

class BonusSelectorEffect:
    """
    UI-эффект, который показывает список кнопок-бонусов на экране
    и ждёт клика для выбора.
    options: list of (label: str, effect_instance)
    """
    PADDING = 20
    BUTTON_H = 40
    BUTTON_W = 200
    SPACING  = 10

    def __init__(self, options):
        self.options = options
        self.alive   = True
        self.font    = pygame.font.SysFont(None, 24)

    def update(self, dt: float):
        # Проверяем клик
        mx, my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            sx, sy = pygame.display.get_surface().get_size()
            # рисуем кнопки виртуально, как в draw
            total_h = len(self.options)*self.BUTTON_H + (len(self.options)-1)*self.SPACING
            start_y = (sy - total_h)//2
            for idx, (label, effect) in enumerate(self.options):
                bx = (sx - self.BUTTON_W)//2
                by = start_y + idx*(self.BUTTON_H + self.SPACING)
                rect = pygame.Rect(bx, by, self.BUTTON_W, self.BUTTON_H)
                if rect.collidepoint(mx, my):
                    # Игрок выбрал бонус
                    bus.emit(BonusSelected(effect=effect))
                    self.alive = False
                    return

    def draw(self, screen: pygame.Surface, camera):
        sx, sy = screen.get_size()
        # затемняем фон
        overlay = pygame.Surface((sx, sy), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        screen.blit(overlay, (0,0))

        # рисуем кнопки по центру
        total_h = len(self.options)*self.BUTTON_H + (len(self.options)-1)*self.SPACING
        start_y = (sy - total_h)//2

        for idx, (label, _) in enumerate(self.options):
            bx = (sx - self.BUTTON_W)//2
            by = start_y + idx*(self.BUTTON_H + self.SPACING)
            rect = pygame.Rect(bx, by, self.BUTTON_W, self.BUTTON_H)
            pygame.draw.rect(screen, (200,200,200), rect)
            pygame.draw.rect(screen, (50,50,50), rect, 2)

            txt = self.font.render(label, True, (0,0,0))
            tx, ty = txt.get_size()
            screen.blit(txt, (bx + (self.BUTTON_W - tx)//2,
                              by + (self.BUTTON_H - ty)//2))
