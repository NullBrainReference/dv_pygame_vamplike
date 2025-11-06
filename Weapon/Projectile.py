import pygame
from GameManagement.Camera import Camera
from Collision.IPosition import IPosition
from Collision.Collider import CircleCollider, Collider
from Pool.ObjectPool import IPoolable
import math

class Projectile(IPosition, IPoolable):
    _base_image = None

    def __init__(self,
                 pos: pygame.Vector2,
                 direction: pygame.Vector2,
                 damage: float,
                 owner,
                 target=None):
        
        self._pos      = pos.copy()
        self.spawn_pos = pos.copy()
        self.direction = direction.normalize()
        self.speed     = 300
        self.damage    = damage
        self.owner     = owner
        self.team      = getattr(owner, "team", None)
        self.target    = target
        self.alive     = True

        self._collider = CircleCollider(self, 8)

        if self._base_image is None:
            self._base_image = pygame.image.load("Assets/Weapons/projectile.png").convert_alpha()

        base_angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
        self.image = pygame.transform.rotate(self._base_image, (base_angle + 180) % 360)
       
        self.rect = self.image.get_rect()

    def reset(self, pos, direction, damage, owner, target=None):
        self._pos      = pos.copy()
        self.spawn_pos = pos.copy()
        self.direction = direction.normalize()
        self.damage    = damage
        self.owner     = owner
        self.team      = getattr(owner, "team", None)
        self.target    = target
        self.alive     = True

        base_angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
        self.image = pygame.transform.rotate(self._base_image, (base_angle + 180) % 360)
        self.rect = self.image.get_rect()


    @property
    def pos(self) -> pygame.Vector2:
        return self._pos
    
    @property
    def is_active(self) -> bool:
        return self.alive

    @property
    def collider(self) -> Collider:
        return self._collider

    def occupy(self):
        self.alive = True
    
    def release(self):
        self.alive = False

    def update(self, dt: float):
        self._pos += self.direction * self.speed * dt

    def draw(self, screen: pygame.Surface, camera: Camera):
        screen_pos       = camera.apply(self.pos)
        self.rect.center = screen_pos
        screen.blit(self.image, self.rect)