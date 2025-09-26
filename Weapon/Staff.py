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
            hp               = 30,
            weapon_cls       = Sword,
            spawn_rate       = 1.1,
            name             = "Ghost",
            chance           = 1.0,
            attack_rate      = 1.2,
            damage           = 5,
            speed            = 80,
            scale            = 1.0,
            target_range     = 30,
            progression_lvl  = 0,
            reward           = 0
        )
    

    def on_attack(self,
                  origin: pygame.Vector2,
                  targets: list,
                  owner=None):
        if self.summoner is None:
            return

        if not self.can_attack():
            return
        self.reset_timer()

        if owner:
            owner.on_attack(targets)

        progression = 0

        self.summoner.summon(progression)
