
import random
from .Effect import Effect

class AdrenalinSpeedEffect(Effect):
    """
    On damage → with given chance grant a one-time speed boost.
    After boost_duration expires, remove speed bonus and
    effect is ready to trigger again on next damage.
    """
    def __init__(self,
                 chance: float = 0.25,
                 amount: float = 32.0,
                 boost_duration: float = 7.0):
        super().__init__(None)
        self.chance         = chance
        self.amount         = amount
        self.boost_duration = boost_duration
        self._boosted       = False

        self._timer         = boost_duration

    def apply(self,
              dt: float,
              unit,
              event: str | None = None,
              **kwargs):
        if event != "damage":
            return
        # only trigger if not currently boosted and timer indicates ready
        if self._boosted or self._timer < self.boost_duration:
            return
        if random.random() < self.chance:
            unit.speed += self.amount
            self._boosted = True
            self._timer   = 0.0

    def update(self, dt: float, unit):
        if self._boosted:
            self._timer += dt
            if self._timer >= self.boost_duration:
                # boost ended: remove bonus
                unit.speed -= self.amount
                self._boosted = False
                # clamp timer to allow next trigger
                self._timer   = self.boost_duration
