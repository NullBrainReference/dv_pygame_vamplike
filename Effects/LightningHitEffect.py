
import random
from Effects.Effect import Effect
from Events.EventBus    import bus
from Events.Events      import RequestTargets, ProvideTargets, SpawnEffect
from Effects.Spells.BoltChain import BoltChainEffect

class LightningHitEffect(Effect):
    def __init__(self,
                 chance: float   = 0.20,
                 cooldown: float = 1.4,
                 chain_range: float  = 100,
                 chain_limit: int    = 7,
                 chain_damage: float = 8):
        super().__init__(duration=None)
        self.chance       = chance
        self.cooldown     = cooldown
        self.chain_range  = chain_range
        self.chain_limit  = chain_limit
        self.chain_damage = chain_damage

        self.cd_timer        = cooldown
        self._primary_target = None

        # subscribe to receive candidate list
        bus.subscribe(ProvideTargets, self._on_provide_targets)

    def apply(self,
              dt: float,
              unit,
              event: str | None = None,
              **kwargs):

        if event is None:
            self.cd_timer = min(self.cd_timer + dt, self.cooldown)
            return

        if event != "attack" or self.cd_timer < self.cooldown:
            return

        if random.random() >= self.chance:
            return

        hit_targets = kwargs.get("targets", [])
        if not hit_targets:
            return

        self._primary_target = hit_targets[0]

        for eff in unit.effects:
            if isinstance(eff, LightningHitEffect):
                eff.cd_timer = 0.0

        # request a list of nearby units via EventBus
        bus.emit(RequestTargets(
            effect=self,
            origin=self._primary_target.pos,
            radius=self.chain_range
        ))

    def _on_provide_targets(self, e: ProvideTargets):
        if e.effect is not self:
            return

        bolt = BoltChainEffect(
            start_unit=self._primary_target,
            limit=self.chain_limit,
            range=self.chain_range,
            damage=self.chain_damage
        )

        remaining = [
            u for u in e.candidates
            if u not in bolt.targets
               and u.team == self._primary_target.team
        ]

        while len(bolt.targets) < bolt.limit and remaining:
            last = bolt.targets[-1]
            next_unit = min(
                remaining,
                key=lambda u: (u.pos - last.pos).length()
            )
            if (next_unit.pos - last.pos).length() > bolt.range:
                break

            bolt.apply(0.0, next_unit)
            remaining.remove(next_unit)

        bus.emit(SpawnEffect(bolt))
