# Weapon.py
import pygame
from Events.Events import SpawnProjectile, SpawnEffect
from Events.EventBus import bus

class Weapon:
    def __init__(self, range: float, rate: float, damage: float):
        self.range = range
        self.rate = rate
        self.damage = damage
        self.timer = 0.0

    def update(self, dt):
        self.timer += dt

    def can_attack(self):
        return self.timer >= self.rate

    def reset_timer(self):
        self.timer = 0.0

    def on_attack(self, origin, targets):
        raise NotImplementedError



class Projectile:
    def __init__(self, pos, direction, damage, target):
        self.pos = pos
        self.direction = direction
        self.speed = 300
        self.damage = damage
        self.radius = 5
        self.alive = True
        self.target = target

    def update(self, dt):
        self.pos += self.direction * self.speed * dt

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), self.pos, self.radius)



class Bow(Weapon):
    def on_attack(self, origin, targets):
        if not self.can_attack():
            return
        self.reset_timer()

        # Отбираем только цели в пределах дальности
        in_range = [
            t for t in targets
            if (t.pos - origin).length_squared() <= self.range * self.range
        ]
        if not in_range:
            return

        # Выбираем самую близкую из тех, что в пределах range
        target = min(in_range, key=lambda t: (t.pos - origin).length_squared())
        direction = (target.pos - origin).normalize()

        projectile = Projectile(origin.copy(), direction, self.damage, target)
        bus.emit(SpawnProjectile(projectile))



class Sword(Weapon):
    def on_attack(self, origin, targets):
        if not self.can_attack():
            return
        self.reset_timer()
        for target in targets:
            if (target.pos - origin).length() <= self.range:
                target.take_damage(self.damage)
        from Weapon.Weapon import SwordSwingEffect
        e = SwordSwingEffect(origin.copy(), self.range)
        bus.emit(SpawnEffect(e))


class SwordSwingEffect:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius
        self.timer = 0.3
        self.alive = True

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.alive = False

    def draw(self, screen):
        if self.alive:
            alpha = int(255 * (self.timer / 0.3))
            color = (255, 255, 255)
            pygame.draw.circle(screen, color, self.pos, int(self.radius), 2)
