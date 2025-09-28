import pygame
from .IPosition import IPosition

#TODO make ABS, also make more shapes if needed
class Collider:
    def __init__(self,
                 parent: IPosition,
                 radius: float,
                 offset: pygame.Vector2 = pygame.Vector2()):
        self.parent = parent
        self.radius = radius
        self.offset = offset

    @property
    def center(self) -> pygame.Vector2:
        return self.parent.pos + self.offset

    def intersects(self, other: "Collider") -> bool:
        dist_sq = (self.center - other.center).length_squared()
        r_sum = self.radius + other.radius
        return dist_sq <= r_sum * r_sum