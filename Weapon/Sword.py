from .Weapon import Weapon
from .SwordSwingEffect import SwordSwingEffect
from Events.Events import SpawnEffect

from Events.EventBus import bus
from Pool.pools import sword_swing_pool as pool

class Sword(Weapon):
    def on_attack(self, origin, targets, owner=None):
        if not self.can_attack():
            return
        # self.reset_timer()

        in_range = False
        for target in targets:
            if (target.pos - origin).length() <= self.range:
                target.take_damage(self.damage)
                self.reset_timer()
                in_range = True
        if not in_range:
            return
        
        owner.on_attack(in_range)
        
        e = pool.get_free()
        if e is None:
            e = SwordSwingEffect(
                origin.copy(), 
                self.range, 
                on_expired=lambda eff: pool.release(eff))
            pool.add(e);
        else:
            e.reset(origin.copy(), self.range)
            

        bus.emit(SpawnEffect(e))