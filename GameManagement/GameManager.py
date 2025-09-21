# GameManager.py
import pygame, random, math
from Events.EventBus import bus
from Events.Events   import SpawnProjectile, SpawnEffect
from Unit.Enemy      import Enemy
from Weapon.Weapon   import Sword
from GameManagement.GameField import GameField

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.clock  = pygame.time.Clock()
        self.field  = GameField()
        self.spawn_timer = 0.0
        self.spawn_rate  = 2.0

        # Подписываемся на события
        bus.subscribe(SpawnProjectile, lambda e: self.field.projectiles.append(e.projectile))
        bus.subscribe(SpawnEffect,     lambda e: self.field.effects.append(e.effect))

    def spawn_enemy(self, radius, center):
        angle = random.uniform(0, 2 * math.pi)
        return pygame.Vector2(
            center.x + radius * math.cos(angle),
            center.y + radius * math.sin(angle)
        )

    def update(self, dt):
        # спавн врагов
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_rate:
            self.spawn_timer = 0.0
            pos = self.spawn_enemy(400, self.field.player.pos)
            self.field.enemies.append(Enemy(pos, weapon=Sword(range=30, rate=1, damage=8)))

        # обновление юнитов и оружия
        self.field.player.update(dt)
        for en in self.field.enemies:
            en.update(dt, self.field.player.pos)
            if en.weapon:
                en.weapon.on_attack(en.pos, [self.field.player])

        # игрок
        self.field.player.weapon.on_attack(self.field.player.pos, self.field.enemies)

        # обновление снарядов и эффектов
        for p in self.field.projectiles:
            p.update(dt)
        for e in self.field.effects:
            e.update(dt)

        # проверка попаданий
        for p in self.field.projectiles:
            for en in self.field.enemies:
                if (p.pos - en.pos).length() < 20:
                    en.take_damage(p.damage)
                    p.alive = False

        # in-place очистка списков
        for lst, attr in [(self.field.projectiles,  'alive'),
                    (self.field.effects,      'alive'),
                    (self.field.enemies,      'hp')]:
            # если у объекта нет нужного атрибута — пропускаем
            for i in range(len(lst)-1, -1, -1):
                item = lst[i]
                if not getattr(item, attr, True):
                    del lst[i]

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.field.player.draw(self.screen)
        for en in self.field.enemies:     en.draw(self.screen)
        for p in self.field.projectiles:  p.draw(self.screen)
        for e in self.field.effects:      e.draw(self.screen)
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
        pygame.quit()
