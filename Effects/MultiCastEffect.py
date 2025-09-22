
import math
import random
import pygame
from .Effect import Effect


class MultiCastEffect(Effect):

    def __init__(self,
                 chance: float = 0.2,
                 cooldown: float = 0.3):
        super().__init__(None)
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
        if event != "attack":
            return
        if self.cd_timer < self.cooldown:
            return
        if random.random() >= self.chance:
            return

        unit.weapon.timer += unit.weapon.rate * 0.8

        # reset CD on every SpikesCastEffect on this unit
        for eff in unit.effects:
            if isinstance(eff, MultiCastEffect):
                eff.cd_timer = 0.0
