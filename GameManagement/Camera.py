
import pygame

class Camera:
    def __init__(self, screen_size: tuple[int,int]):
        self.offset   = pygame.Vector2(0, 0)
        self.screen_w = screen_size[0]
        self.screen_h = screen_size[1]

    def update(self, target_pos: pygame.Vector2):
        """
        Вычисляем смещение так, чтобы target_pos (игрок) оказался
        в центре экрана: offset = center – world_pos.
        """
        self.offset.x = self.screen_w / 2 - target_pos.x
        self.offset.y = self.screen_h / 2 - target_pos.y

    def apply(self, world_pos: pygame.Vector2) -> pygame.Vector2:
        """Преобразует координаты из мировых в экранные."""
        return world_pos + self.offset

    def apply_rect(self, rect: pygame.Rect) -> pygame.Rect:
        """Сдвигает прямоугольник на offset."""
        return rect.move(self.offset.x, self.offset.y)
