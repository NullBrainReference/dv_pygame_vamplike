import pygame, math, random
from dataclasses import dataclass, field
from Unit.Enemy import Enemy

@dataclass
class SpawnController:
    hp: float
    weapon_cls:    type
    spawn_rate:    float
    name:          str
    chance:        float
    attack_rate:   float
    damage:        float
    speed:         float
    scale:         float
    target_range:  float
    progression_lvl: float = 0.0
    reward: float = 30

    spawn_timer:   float = field(default=0.0, init=False)

    def _random_spawn_pos(self,
                          radius: float,
                          center: pygame.Vector2) -> pygame.Vector2:
        angle = random.uniform(0, 2 * math.pi)
        return pygame.Vector2(
            center.x + radius * math.cos(angle),
            center.y + radius * math.sin(angle),
        )

    def spawn(self,
              dt: float,
              progression: float,
              field) -> None:
        # if we haven't reached required progression — do nothing
        if progression < self.progression_lvl:
            return

        # advance timer and check if it's time to spawn
        self.spawn_timer += dt
        effective_rate = max(0.1, self.spawn_rate - 0.8 * progression)
        if self.spawn_timer < effective_rate:
            return

        self.spawn_timer -= effective_rate

        # chance check
        if random.random() > self.chance:
            return

        # choose random point вокруг игрока
        pos = self._random_spawn_pos(400, field.player.pos)

        # создаём оружие с учётом прогрессии
        weapon = self.weapon_cls(
            range=self.target_range,
            rate=max(0.1, self.attack_rate - 0.2 * progression),
            damage=self.damage + 4 * progression
        )

        # скорость тоже растёт с прокруткой
        speed = self.speed + 10 * progression
        reward = self.reward + 5 * progression

        # спавним врага
        field.enemies.append(
            Enemy(pos, self.hp, weapon, self.name, speed, self.scale, reward)
        )