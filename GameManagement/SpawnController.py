# GameManagement/SpawnController.py

import math
import random
import pygame
import inspect
from dataclasses import dataclass, field
from Unit.Enemy import Enemy

@dataclass
class SpawnController:
    hp:               float
    weapon_cls:       type
    spawn_rate:       float
    name:             str
    chance:           float
    attack_rate:      float
    damage:           float
    speed:            float
    scale:            float
    target_range:     float
    progression_lvl:  float = 0.0
    reward:           float = 30

    spawn_timer:      float = field(default=0.0, init=False)

    def _random_spawn_pos(self,
                          radius: float,
                          center: pygame.Vector2) -> pygame.Vector2:
        """Return a random point on a circle around center."""
        angle = random.uniform(0, 2 * math.pi)
        return pygame.Vector2(
            center.x + radius * math.cos(angle),
            center.y + radius * math.sin(angle),
        )

    def spawn(self,
              dt: float,
              progression: float,
              field,
              origin: pygame.Vector2 = None,
              radius: float = 400) -> None:
        """Timed spawn: respects spawn_rate, chance and progression."""
        if progression < self.progression_lvl:
            return

        self.spawn_timer += dt
        effective_rate = max(0.1, self.spawn_rate - 0.8 * progression)
        if self.spawn_timer < effective_rate:
            return
        self.spawn_timer -= effective_rate

        if random.random() > self.chance:
            return

        self._do_spawn(progression, field, origin, radius)

    def spawn_now(self,
                  progression: float,
                  field,
                  origin: pygame.Vector2 = None,
                  radius: float = 400) -> None:
        """Immediate spawn: bypasses timer and chance."""
        if progression < self.progression_lvl:
            return

        self._do_spawn(progression, field, origin, radius)

    def _do_spawn(self,
                  progression: float,
                  field,
                  origin: pygame.Vector2,
                  radius: float) -> None:
        """Internal spawn logic: creates Enemy and assigns weapon."""

        # Determine spawn center (default to player)
        center = origin or field.player.pos
        pos = self._random_spawn_pos(radius, center)

        # 1) Create enemy without weapon
        enemy = Enemy(
            pos        = pos,
            hp         = self.hp,
            weapon     = None,
            enemy_type = self.name,
            speed      = self.speed + 10 * progression,
            scale      = self.scale,
            reward     = self.reward + 5 * progression
        )

        # 2) Prepare weapon constructor arguments
        kwargs = {
            'range':  self.target_range,
            'rate':   max(0.1, self.attack_rate - 0.2 * progression),
            'damage': self.damage + 4 * progression
        }

        # 3) Detect if weapon_cls __init__ has 'owner' parameter
        sig = inspect.signature(self.weapon_cls)
        if 'owner' in sig.parameters:
            kwargs['owner'] = enemy

        weapon = self.weapon_cls(**kwargs)
        enemy.weapon = weapon

        field.enemies.append(enemy)
