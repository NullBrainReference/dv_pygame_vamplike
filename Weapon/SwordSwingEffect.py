import pygame
from Pool.ObjectPool import IPoolable
from GameManagement.Camera import Camera


class SwordSwingEffect(IPoolable):
    def __init__(self, pos, radius, on_expired):
        self.pos = pos
        self.radius = radius
        self.timer = 0.3
        self.alive = True
        self.on_expired = on_expired

    def reset(self, pos, radius):
        self.pos = pos
        self.radius = radius
        self.timer = 0.3
        self.alive = True

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            if self.is_active:
                self.on_expired()
                self.alive = False
            



    def draw(self, screen: pygame.Surface, camera: Camera):
        if not self.alive:
            return
        screen_pos = camera.apply(self.pos)
        alpha = int(255 * (self.timer / 0.3))
        color = (255, 255, 255, alpha)
        pygame.draw.circle(screen, color, screen_pos, int(self.radius), 2)

    @property
    def is_active(self) -> bool:
        return self.alive

    def release(self):
        self.alive = False

    def occupy(self):
        self.alive = True
    
