
import math
import random
import pygame
from .Effect import Effect


class VampiricEffect(Effect):

    def __init__(self,
                 amount: float = 2):
        super().__init__(None)
        self.amount = amount

    def apply(self,
              dt: float,
              unit,
              event: str | None = None,
              **kwargs):
        # per-frame: recharge own CD

        if event != "attack":
            return

        targets = kwargs.get("targets", [])
        unit.heal(self.amount * len(targets))
