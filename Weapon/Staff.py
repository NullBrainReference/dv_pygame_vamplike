# Weapon/SummoningStaff.py

import pygame
from Weapon.Weapon         import Weapon
from Weapon.Weapon         import Sword
from GameManagement.SummonController import SummonController

class SummoningStaff(Weapon):
    def __init__(self,
                 range: float,
                 rate: float,
                 damage: float,
                 owner,
                 field,
                 progression_lvl: float = 0.0):
        super().__init__(range, rate, damage)

        self.owner = owner
        self.field = field

        self.summoner = None
        
    def set_owner(self, owner):
        self.owner = owner

        self.summoner = SummonController(
            owner            = owner,
            field            = self.field,
            hp               = 20,
            weapon_cls       = Sword,
            spawn_rate       = 1.1,
            name             = "Ghost",
            chance           = 0.8,
            attack_rate      = 1.2,
            damage           = 16,
            speed            = 90,
            scale            = 1.0,
            target_range     = 35,
            progression_lvl  = 0,
            reward           = 8
        )
    

    def on_attack(self,
                  origin: pygame.Vector2,
                  targets: list,
                  owner=None):
        if self.summoner is None:
            return

        if not self.can_attack():
            return
        
        in_range = [
            t for t in targets
            if (t.pos - origin).length_squared() <= self.range ** 2
        ]
        if not in_range:
            return

        self.reset_timer()

        if owner:
            owner.on_attack(targets)

        progression = 0

        self.summoner.summon(progression)
