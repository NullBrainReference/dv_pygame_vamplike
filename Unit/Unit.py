
import pygame
from abc import ABC, abstractmethod
from Collision.IPosition import IPosition
from Collision.Collider import Collider

from Effects.Effect import Effect
from Effects.Visual.DamageFlashEffect import DamageFlashEffect

class Unit(ABC, IPosition):
    def __init__(self, hp: float, weapon):
        self.max_hp = hp
        self.hp     = hp
        self.weapon = weapon
        self.effects: list[Effect] = []
        self.is_dead = False
        self.team    = None
        self.flash_tint = None

        self.desired_velocity = pygame.Vector2(0,0)
        self.impulse_velocity = pygame.Vector2(0,0)
        self.mass       = 1.0

        self.add_effect(DamageFlashEffect(half_duration=0.15))

    @property
    @abstractmethod
    def pos(self) -> pygame.Vector2:
        pass

    @property
    @abstractmethod
    def collider(self) -> Collider:
        pass

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
