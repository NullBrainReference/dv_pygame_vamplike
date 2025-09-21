
from abc import ABC, abstractmethod
from Weapon.Weapon import Weapon

class Unit(ABC):
    def __init__(self, hp: float, weapon: Weapon):
        self.max_hp = hp
        self.hp     = hp
        self.weapon = weapon
        self.scale  = 1.0

        self.effects: list = []

    def add_effect(self, effect):
        self.effects.append(effect)

    def update_effects(self, dt: float):
        for i in range(len(self.effects)-1, -1, -1):
            eff = self.effects[i]
            eff.update(dt, self)
            if eff.is_expired:
                del self.effects[i]

    def take_damage(self, amount: float):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.on_death()

    def heal(self, amount: float):
        self.hp = min(self.hp + amount, self.max_hp)

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self, screen, camera):
        pass

    @abstractmethod
    def on_death(self):
        pass
