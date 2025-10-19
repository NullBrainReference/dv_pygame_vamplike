# Weapon/Bow.py

import pygame
from Weapon.Weapon import Weapon
from Weapon.Projectile import Projectile
from Events.Events import SpawnProjectile
from Events.EventBus import bus
from Pool.pools import projectile_pool

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

        # choose nearest target
        target = min(
            in_range,
            key=lambda t: (t.pos - origin).length_squared()
        )
        direction = (target.pos - origin).normalize()

        if owner:
            owner.on_attack([target])

        # spawn and emit projectile
        proj = projectile_pool.get_free()
        if proj is None:
            proj = Projectile(
                pos         = origin.copy(),
                direction   = direction,
                damage      = self.damage,
                owner       = owner,
                target      = target
            )
            projectile_pool.add(proj)
        else:
            proj.reset(
                pos         = origin,
                direction   = direction,
                damage      = self.damage,
                owner       = owner,
                target      = target)
            proj.occupy()
        # proj = Projectile(
        #     pos=origin.copy(),
        #     direction=direction,
        #     damage=self.damage,
        #     owner=owner,
        #     target=target
        # )
        bus.emit(SpawnProjectile(proj))
