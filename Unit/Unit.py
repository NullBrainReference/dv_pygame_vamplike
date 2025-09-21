from abc import ABC, abstractmethod
from Weapon.Weapon import Weapon

class Unit(ABC):
    def __init__(self, hp, weapon : Weapon):
        self.max_hp = hp
        self.hp = hp
        self.weapon = weapon

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.on_death()

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen, camera):
        pass

    @abstractmethod
    def on_death(self):
        pass
