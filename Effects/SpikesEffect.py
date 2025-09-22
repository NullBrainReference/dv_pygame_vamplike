
import math
import pygame
from .Effect import Effect
from Events.EventBus import bus
from Events.Events import SpawnProjectile
from Weapon.Weapon import Projectile

class SpikesEffect(Effect):
    """
    When unit takes damage, spawn N projectiles in a circle.
    """
    def __init__(self, count: int = 12, damage: float = 5):
        super().__init__(None)
        self.count     = count
        self.damage    = damage
        self._triggered = False

    def apply(self, dt: float, unit, event: str | None = None, **kwargs):
        if event != "damage" or self._triggered:
            return

        origin     = unit.pos.copy()
        angle_step = 2 * math.pi / self.count

        for i in range(self.count):
            angle     = angle_step * i
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            proj = Projectile(
                pos       = origin,
                direction = direction,
                damage    = self.damage,
                owner     = unit,
                target    = None
            )
            bus.emit(SpawnProjectile(proj))

        self._triggered = True
        self.elapsed    = self.duration
