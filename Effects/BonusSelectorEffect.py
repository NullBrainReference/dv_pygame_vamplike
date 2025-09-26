
import pygame
from Events.EventBus import bus
from Events.Events    import BonusSelected

class BonusSelectorEffect:
    """
    Shows a list of buttons with fixed width; height adapts to line count.
    options: list of (label: str, effect_instance)
    """
    BUTTON_W      = 320
    PADDING       = 12
    SPACING       = 10
    LINE_SPACING  = 4
    BG_COLOR      = (200, 200, 200)
    BORDER_COLOR  = (50, 50, 50)
    BORDER_WIDTH  = 2

    def __init__(self, options):
        pygame.font.init()
        self.font    = pygame.font.SysFont(None, 24)
        self.alive   = True
        self.buttons = []

        # Precompute each button's height based on its lines
        for label, effect in options:
            lines = label.split('\n')
            # measure each line's height
            line_heights = [self.font.size(line)[1] for line in lines]
            text_block_h = sum(line_heights) + (len(lines) - 1) * self.LINE_SPACING
            btn_h = text_block_h + self.PADDING * 2

            self.buttons.append({
                'lines':  lines,
                'effect': effect,
                'w':      self.BUTTON_W,
                'h':      btn_h,
                'rect':   None
            })

    def update(self, dt: float):
        mx, my = pygame.mouse.get_pos()
        if not pygame.mouse.get_pressed()[0]:
            return

        # check click against stored rects
        for btn in self.buttons:
            rect = btn['rect']
            if rect and rect.collidepoint(mx, my):
                bus.emit(BonusSelected(effect=btn['effect']))
                self.alive = False
                return

    def draw(self, screen: pygame.Surface, camera=None):
        sx, sy = screen.get_size()

        # semi-transparent background
        overlay = pygame.Surface((sx, sy), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # vertical centering
        total_h = sum(btn['h'] for btn in self.buttons) \
                  + (len(self.buttons) - 1) * self.SPACING
        start_y = (sy - total_h) // 2

        y = start_y
        for btn in self.buttons:
            w, h = btn['w'], btn['h']
            x = (sx - w) // 2
            rect = pygame.Rect(x, y, w, h)
            btn['rect'] = rect

            # draw the button
            pygame.draw.rect(screen, self.BG_COLOR, rect)
            pygame.draw.rect(screen, self.BORDER_COLOR, rect, self.BORDER_WIDTH)

            # draw each line centered horizontally
            text_y = y + self.PADDING
            for line in btn['lines']:
                txt = self.font.render(line, True, (0, 0, 0))
                tx, ty = txt.get_size()
                text_x = x + (w - tx) // 2
                screen.blit(txt, (text_x, text_y))
                text_y += ty + self.LINE_SPACING

            y += h + self.SPACING
