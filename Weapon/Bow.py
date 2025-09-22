# Weapon/Bow.py

import pygame
from Weapon.Weapon import Weapon
from Weapon.Weapon import Projectile
from Events.Events import SpawnProjectile
from Events.EventBus import bus

class Bow(Weapon):
    def __init__(self, range: float, rate: float, damage: float, sprite_path=None):
        super().__init__(range, rate, damage)
        if sprite_path:
            self.icon_path = sprite_path

    def on_attack(self,
                  origin: pygame.Vector2,
                  targets: list,
                  owner=None):
        if not self.can_attack():
            return
        self.reset_timer()

        # filter targets within weapon range
        in_range = [
            t for t in targets
            if (t.pos - origin).length_squared() <= self.range ** 2
        ]
        if not in_range:
            return

        # notify owner about the attack event
        if owner:
            owner.on_attack(targets)

        # choose nearest target
        target = min(
            in_range,
            key=lambda t: (t.pos - origin).length_squared()
        )
        direction = (target.pos - origin).normalize()

        # spawn and emit projectile
        proj = Projectile(
            pos=origin.copy(),
            direction=direction,
            damage=self.damage,
            owner=owner,
            target=target
        )
        bus.emit(SpawnProjectile(proj))
