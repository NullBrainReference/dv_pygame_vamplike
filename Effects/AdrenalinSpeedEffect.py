
import random
from .Effect import Effect

class AdrenalinSpeedEffect(Effect):
    """
    On damage, with given chance grant a one-time speed boost,
    then remove it when the duration expires.
    """
    def __init__(self,
                 chance: float = 0.2,
                 amount: float = 16,
                 duration: float = 5.0):
        super().__init__(duration)
        self.chance    = chance
        self.amount    = amount
        self._boosted  = False
        self._removed  = False

    def apply(self,
              dt: float,
              unit,
              event: str | None = None,
              **kwargs):
        if event != "damage" or self._boosted:
            return
        if random.random() < self.chance:
            unit.speed += self.amount
            self._boosted = True

    def update(self, dt: float, unit):
        super().update(dt, unit)
        if self._boosted and self.is_expired and not self._removed:
            unit.speed -= self.amount
            self._removed = True
