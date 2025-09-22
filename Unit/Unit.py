
import pygame
from abc import ABC, abstractmethod
from Effects.Effect import Effect

class Unit(ABC):
    def __init__(self, hp: float, weapon):
        self.max_hp = hp
        self.hp     = hp
        self.weapon = weapon
        self.effects: list[Effect] = []
        self.is_dead = False

    def add_effect(self, effect: Effect):
        self.effects.append(effect)

    def update_effects(self, dt: float):
        for eff in self.effects:
            eff.update(dt, self)
        self.effects = [e for e in self.effects if not e.is_expired]

    def take_damage(self, amount: float):
        if self.is_dead:
            return
        self.hp = max(self.hp - amount, 0)
        for eff in self.effects:
            eff.apply(0.0, self, event="damage", amount=amount)
        # self.effects = [e for e in self.effects if not e.is_expired]
        if self.hp == 0:
            self.on_death()

    def heal(self, amount: float):
        if self.is_dead:
            return
        self.hp = min(self.hp + amount, self.max_hp)
        for eff in self.effects:
            eff.apply(0.0, self, event="heal", amount=amount)
        # self.effects = [e for e in self.effects if not e.is_expired]

    # def attack(self, target):
    #     if self.is_dead:
    #         return
    #     for eff in self.effects:
    #         eff.apply(0.0, self, event="attack", target=target)
    #     self.weapon.on_attack(origin=self.pos, targets=[target], owner=self)
    #     self.effects = [e for e in self.effects if not e.is_expired]

    def on_attack(self, targets):
        if self.is_dead:
            return
        for eff in self.effects:
            eff.apply(0.0, self, event="attack", targets=targets)

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface, camera):
        pass

    @abstractmethod
    def on_death(self):
        pass
