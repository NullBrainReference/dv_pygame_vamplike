
from .SpawnController import SpawnController

class SummonController(SpawnController):
    def __init__(self,
                 owner,
                 field,
                 **kwargs):
        super().__init__(**kwargs)
        self.owner = owner
        self.field = field

    def summon(self,
               progression: float) -> None:
        """
        Spawn immediately around self.owner.pos
        """
        # origin is always owner.pos here
        self.spawn_now(
            progression=progression,
            field=self.field,
            origin=self.owner.pos,
            radius=60
        )
