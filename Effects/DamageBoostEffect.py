from .Effect import Effect

class DamageBoostEffect(Effect):

    def __init__(self, amount: float):
        # duration=0.0 — эффект мгновенный
        super().__init__(duration=0.0)
        self.amount   = amount
        self._applied = False

    def apply(self, dt: float, unit):
        if self._applied:
            return

        if hasattr(unit, "weapons"):
            for weapon in unit.weapons.values():
                weapon.damage += self.amount

        self._applied = True
        # makes expired
        self.elapsed = self.duration