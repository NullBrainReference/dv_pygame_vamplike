
import math
import random
import pygame
from dataclasses import dataclass, field
from .SpawnController import SpawnController
from Unit.Enemy      import Enemy
from Weapon.Staff import SummoningStaff

@dataclass
class SummonerSpawnController(SpawnController):
    """
    Specialized spawner that creates an Enemy with SummoningStaff.
    """
    def _do_spawn(self,
                  progression: float,
                  field,
                  origin: pygame.Vector2,
                  radius: float) -> None:

        center = origin or field.player.pos
        angle  = random.uniform(0, 2 * math.pi)
        pos    = pygame.Vector2(
            center.x + radius * math.cos(angle),
            center.y + radius * math.sin(angle),
        )

        weapon = SummoningStaff(
            range             = self.target_range,
            rate              = max(0.1, self.attack_rate - 0.2 * progression),
            damage            = self.damage + 4 * progression,
            owner             = None,
            field             = field,
            progression_lvl   = self.progression_lvl
        )

        speed_val = self.speed
        reward    = self.reward + 5 * progression

        enemy = Enemy(
            pos        = pos,
            hp         = self.hp,
            weapon     = weapon,
            enemy_type = self.name,
            speed      = speed_val,
            scale      = self.scale,
            reward     = reward
        )

        # 3) Now that enemy exists, fix the SummoningStaff.owner
        # weapon.owner = enemy
        weapon.set_owner(enemy)

        # 4) Add to the game field
        field.enemies.append(enemy)
