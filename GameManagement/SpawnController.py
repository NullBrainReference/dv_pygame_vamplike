import pygame, math, random
from Unit.Enemy import Enemy


class SpawnController:
    def __init__(self, weapon, rate, name, chance, attack_rate, dmg, speed, scale, range):
        self.weapon = weapon

        self.spawn_timer = 0.0
        self.spawn_rate  = rate
        self.name = name
        self.chance = chance
        self.attack_rate = attack_rate
        self.dmg = dmg
        self.speed = speed
        self.scale = scale
        self.range = range


    def _random_spawn_pos(self, radius: float,
                          center: pygame.Vector2) -> pygame.Vector2:
        angle = random.uniform(0, 2 * math.pi)
        x     = center.x + radius * math.cos(angle)
        y     = center.y + radius * math.sin(angle)
        return pygame.Vector2(x, y)

    def spawn(self, dt, progression, field):
        rate = self.spawn_rate - 0.8 * progression
        self.spawn_timer += dt
        if self.spawn_timer >= rate:
            self.spawn_timer -= rate

            if random.random() > self.chance:
                return

            pos = self._random_spawn_pos(400, field.player.pos)

            weapon, etype, speed, scale = self.weapon(
                    range=self.range, rate=self.attack_rate - 0.2 * progression, damage=self.dmg + 4 * progression), self.name, self.speed + 10 * progression, self.scale

            field.enemies.append(
                Enemy(pos, weapon, etype, speed, scale)
            )
    