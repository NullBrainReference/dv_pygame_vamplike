from .Effect import Effect

class RegenerationEffect(Effect):

    def __init__(self, regen_rate: float, duration: float | None = None):
        super().__init__(duration)
        self.regen_rate = regen_rate

    def apply(self,
              dt: float,
              unit,
              event: str | None = None,
              **kwargs):
        # event ignore
        if event is not None:
            return
        unit.heal(self.regen_rate * dt)