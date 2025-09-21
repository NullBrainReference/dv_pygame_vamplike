from .Effect import Effect

class SpeedBoostEffect(Effect):

    def __init__(self, amount: float):
        super().__init__(None)
        self.amount   = amount
        self._applied = False

    def apply(self, dt: float, unit):
        if self._applied:
            return

        unit.speed += self.amount

        self._applied = True
        # makes expired
        self.elapsed = self.duration