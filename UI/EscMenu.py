import pygame
from Events.EventBus import bus
from Events.Events import HideEscMenu, QuitGame

class EscMenu:
    BUTTON_W = 320
    BUTTON_H = 40
    SPACING  = 10
    BG_COLOR = (200, 200, 200)
    BORDER_COLOR = (50, 50, 50)

    def __init__(self, font):
        self.font = font
        self.alive = True
        self.buttons = [
            self._make_button("Continue", lambda: bus.emit(HideEscMenu())),
            self._make_button("Quit",     lambda: bus.emit(QuitGame())),
        ]

    def _make_button(self, text, on_click):
        return {
            "text": text,
            "rect": None,
            "on_click": on_click,
            "w": self.BUTTON_W,
            "h": self.BUTTON_H,
        }

    def update(self, dt):
        mx, my = pygame.mouse.get_pos()
        if not pygame.mouse.get_pressed()[0]:
            return
        for btn in self.buttons:
            if btn["rect"] and btn["rect"].collidepoint(mx, my):
                btn["on_click"]()
                self.alive = False
                return

    def draw(self, screen, camera=None):
        sx, sy = screen.get_size()
        overlay = pygame.Surface((sx, sy), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        total_h = sum(b["h"] for b in self.buttons) + (len(self.buttons)-1)*self.SPACING
        y = (sy - total_h) // 2
        for btn in self.buttons:
            x = (sx - btn["w"]) // 2
            rect = pygame.Rect(x, y, btn["w"], btn["h"])
            btn["rect"] = rect
            pygame.draw.rect(screen, self.BG_COLOR, rect)
            pygame.draw.rect(screen, self.BORDER_COLOR, rect, 2)

            txt = self.font.render(btn["text"], True, (0,0,0))
            tx, ty = txt.get_size()
            screen.blit(txt, (x + (btn["w"]-tx)//2, y + (btn["h"]-ty)//2))
            y += btn["h"] + self.SPACING
