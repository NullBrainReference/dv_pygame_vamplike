from .Effect import Effect

class DamageBoostEffect(Effect):

    def __init__(self, amount: float):
        super().__init__(None)
        self.amount   = amount
        self._applied = False

    def apply(self,
              dt: float,
              unit,
              event: str | None = None,
              **kwargs):

        if self._applied:
            return

        for weapon in getattr(unit, "weapons", {}).values():
            weapon.damage += self.amount

        self._applied = True
        self.elapsed  = self.duration