import pygame
from abc import ABC, abstractmethod
from .IPosition import IPosition

#TODO make ABC, also make more shapes if needed
class Collider(ABC):
    def __init__(self,
                 parent: IPosition,
                 offset: pygame.Vector2 = pygame.Vector2()):
        self.parent = parent
        # self.radius = radius
        self.offset = offset

    @property
    def center(self) -> pygame.Vector2:
        return self.parent.pos + self.offset

    @abstractmethod
    def intersects(self, other: "Collider") -> bool:
        pass

    @abstractmethod
    def intersects_circle(self, circle: "CircleCollider") -> bool:
        pass

    @abstractmethod
    def intersects_box(self, box: "BoxCollider") -> bool:
        pass
    
class CircleCollider(Collider):
    def __init__(self,
                parent: IPosition,
                radius: float,
                offset: pygame.Vector2 = pygame.Vector2()):
        super().__init__(parent, offset)
        self.radius = radius

    def intersects(self, other: "Collider") -> bool:
        return other.intersects_circle(self)

    def intersects_circle(self, circle: "CircleCollider") -> bool:
        dist_sq = (self.center - circle.center).length_squared()
        r_sum = self.radius + circle.radius
        return dist_sq <= r_sum * r_sum

    def intersects_box(self, box: "BoxCollider") -> bool:
        circle_center = self.center
        box_rect = box.rect
        closest_x = max(box_rect.left, min(circle_center.x, box_rect.right))
        closest_y = max(box_rect.top, min(circle_center.y, box_rect.bottom))
        distance = pygame.Vector2(closest_x, closest_y) - circle_center
        return distance.length_squared() <= self.radius ** 2
    

class BoxCollider(Collider):
    def __init__(self,
                 parent: IPosition,
                 width: float,
                 height: float,
                 offset: pygame.Vector2 = pygame.Vector2()):
        super().__init__(parent, offset)
        self.width = width
        self.height = height

    @property
    def rect(self) -> pygame.Rect:
        top_left = self.center - pygame.Vector2(self.width / 2, self.height / 2)
        return pygame.Rect(top_left.x, top_left.y, self.width, self.height)

    def intersects(self, other: "Collider") -> bool:
        return other.intersects_box(self)

    def intersects_circle(self, circle: "CircleCollider") -> bool:
        circle_center = circle.center
        box_rect = self.rect
        closest_x = max(box_rect.left, min(circle_center.x, box_rect.right))
        closest_y = max(box_rect.top, min(circle_center.y, box_rect.bottom))
        distance = pygame.Vector2(closest_x, closest_y) - circle_center
        return distance.length_squared() <= circle.radius ** 2

    def intersects_box(self, box: "BoxCollider") -> bool:
        return self.rect.colliderect(box.rect)
