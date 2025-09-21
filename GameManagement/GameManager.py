# GameManager.py
import pygame
import random
import math

from Events.EventBus    import bus
from Events.Events      import SpawnProjectile, SpawnEffect
from Unit.Enemy        import Enemy
from Weapon.Weapon     import Bow, Sword
from GameManagement.GameField import GameField
from .Camera     import Camera

class GameManager:
    def __init__(self, screen):
        self.screen     = screen
        self.clock      = pygame.time.Clock()
        self.field      = GameField()
        self.spawn_timer = 0.0
        self.spawn_rate  = 2.0  # сек

        self.camera = Camera(screen.get_size())

        bus.subscribe(SpawnProjectile, lambda e: self.field.projectiles.append(e.projectile))
        bus.subscribe(SpawnEffect,     lambda e: self.field.effects.append(e.effect))

    def _random_spawn_pos(self, radius: float, center: pygame.Vector2) -> pygame.Vector2:
        angle = random.uniform(0, 2 * math.pi)
        x = center.x + radius * math.cos(angle)
        y = center.y + radius * math.sin(angle)
        return pygame.Vector2(x, y)

    def update(self, dt: float):
        # spawn
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_rate:
            self.spawn_timer -= self.spawn_rate
            pos = self._random_spawn_pos(400, self.field.player.pos)
            speed = 25
            scale = 1.6

            if random.random() < 0.5:
                weapon     = Bow(range=300, rate=1.2, damage=6)
                enemy_type = "Spider"
            else:
                weapon     = Sword(range=20, rate=1.5, damage=12)
                enemy_type = "Zombie"
                speed      = 48
                scale      = 2.4

            self.field.enemies.append(Enemy(pos, weapon, enemy_type, speed, scale))

        self.field.player.update(dt)

        self.camera.update(self.field.player.pos)

        for en in self.field.enemies:
            en.update(dt, self.field.player.pos)
            if en.weapon:
                en.weapon.on_attack(en.pos, [self.field.player], owner=en)

        self.field.player.weapon.on_attack(
            self.field.player.pos, 
            self.field.enemies, 
            owner=self.field.player)

        for p in self.field.projectiles:
            p.update(dt)
        for e in self.field.effects:
            e.update(dt)

        # Hit detection
        for p in self.field.projectiles:
            if p.target == None:
                p.alive = False

            elif self.field.player == p.target and (p.pos - self.field.player.pos).length() < 20:
                self.field.player.take_damage(p.damage)
                p.alive = False
            elif self.field.player != p.target:
                for en in self.field.enemies:
                    if (p.pos - en.pos).length() < 20:
                        en.take_damage(p.damage)
                        p.alive = False

        px, py = self.field.player.pos
        max_dist_sq = 800 * 800

        for lst, attr in [
            (self.field.projectiles, 'alive'),
            (self.field.effects,     'alive'),
            (self.field.enemies,     'hp')
        ]:
            for i in range(len(lst)-1, -1, -1):
                item = lst[i]
                                
                dead = not getattr(item, attr, True)
                if dead:
                    del lst[i]
                    continue
                
                if not hasattr(item, 'pos'):
                    continue
                
                too_far = (item.pos.x - px) ** 2 + (item.pos.y - py) ** 2 > max_dist_sq
                if too_far:
                    del lst[i]

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.field.player.draw(self.screen, self.camera)

        for en in self.field.enemies:
            en.draw(self.screen, self.camera)
        for p in self.field.projectiles:
            p.draw(self.screen, self.camera)
        for e in self.field.effects:
            e.draw(self.screen, self.camera)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False

            self.update(dt)
            self.draw()

            # if self.field.player.hp <= 0:
            #     running = False

        pygame.quit()
