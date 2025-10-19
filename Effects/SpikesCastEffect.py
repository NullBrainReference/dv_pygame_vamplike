
import math
import random
import pygame
from .Effect import Effect
from Events.EventBus import bus
from Events.Events import SpawnProjectile
from Weapon.Projectile import Projectile
from Pool.pools import projectile_pool

class SpikesCastEffect(Effect):
    """
    On damage: each instance has a chance to fire spikes in circle,
    then all SpikesCastEffect on the same unit go on cooldown.
    """
    def __init__(self,
                 count: int = 12,
                 damage: float = 20,
                 chance: float = 0.25,
                 cooldown: float = 0.2):
        super().__init__(None)
        self.count    = count
        self.damage   = damage
        self.chance   = chance
        self.cooldown = cooldown
        # start ready
        self.cd_timer = cooldown

    def apply(self,
              dt: float,
              unit,
              event: str | None = None,
              **kwargs):
        # per-frame: recharge own CD
        if event is None:
            self.cd_timer = min(self.cd_timer + dt, self.cooldown)
            return

        # on damage: attempt trigger
        if event != "damage":
            return
        if self.cd_timer < self.cooldown:
            return
        if random.random() >= self.chance:
            return

        # spawn spikes
        origin     = unit.pos.copy()
        angle_step = 2 * math.pi / self.count
        for i in range(self.count):
            angle     = angle_step * i
            direction = pygame.Vector2(math.cos(angle),
                                       math.sin(angle))
            
            proj = projectile_pool.get_free()
            if proj is None:
                proj = Projectile(
                    pos         = origin,
                    direction   = direction,
                    damage      = self.damage,
                    owner       = unit,
                    target      = None
                )
                projectile_pool.add(proj)
            else:
                proj.reset(
                    pos         = origin,
                    direction   = direction,
                    damage      = self.damage,
                    owner       = unit,
                    target      = None)
                proj.occupy()

            # proj = Projectile(
            #     pos       = origin,
            #     direction = direction,
            #     damage    = self.damage,
            #     owner     = unit,
            #     target    = None
            # )
            bus.emit(SpawnProjectile(proj))

        # reset CD on every SpikesCastEffect on this unit
        for eff in unit.effects:
            if isinstance(eff, SpikesCastEffect):
                eff.cd_timer = 0.0
