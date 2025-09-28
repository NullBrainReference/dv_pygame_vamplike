import pygame

class FPSCounter:
    def __init__(self, font: pygame.font.Font, pos: tuple[int,int] = (10, 10), color=(255,255,255)):
        self.font  = font
        self.pos   = pos
        self.color = color

    def draw(self, surface: pygame.Surface, clock: pygame.time.Clock):
        fps = clock.get_fps()
        text = f"FPS: {fps:5.1f}"
        img  = self.font.render(text, True, self.color)
        surface.blit(img, self.pos)
