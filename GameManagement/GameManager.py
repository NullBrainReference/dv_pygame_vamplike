
import pygame
import random
import math

from Events.EventBus      import bus
from Events.Events        import (
    SpawnProjectile,
    SpawnEffect,
    GainExp,
    LevelUp,
    ShowBonusSelector,
    BonusSelected,
)
from Unit.Enemy           import Enemy
from Weapon.Weapon        import Sword
from Weapon.Bow           import Bow
from GameManagement.GameField import GameField
from .Camera              import Camera
from Effects.BonusSelectorEffect  import BonusSelectorEffect
from Effects.RegenerationEffect   import RegenerationEffect
from Effects.DamageBoostEffect    import DamageBoostEffect
from Effects.SpeedBoostEffect     import SpeedBoostEffect


MAX_PROJECTILE_DIST_SQ = 1000 ** 2
HIT_RADIUS_SQ          = 20 ** 2

class GameManager:
    def __init__(self, screen):
        self.screen      = screen
        self.clock       = pygame.time.Clock()
        self.field       = GameField()
        self.spawn_timer = 0.0
        self.spawn_rate  = 2.0   # seconds between spawns
        self.paused      = False

        self.camera = Camera(screen.get_size())

        bus.subscribe(SpawnProjectile,  lambda e: self.field.projectiles.append(e.projectile))
        bus.subscribe(SpawnEffect,      lambda e: self.field.effects.append(e.effect))
        bus.subscribe(LevelUp,          self._on_level_up)
        bus.subscribe(ShowBonusSelector,
                      lambda e: self.field.effects.append(BonusSelectorEffect(e.options)))
        bus.subscribe(BonusSelected,    self._on_bonus_selected)

    def _on_level_up(self, e: LevelUp):
        # Ставим игру на паузу и показываем селектор
        self.paused = True
        self.field.player.max_hp += 5

        options = [
            ("Healing regen",  RegenerationEffect(regen_rate=10, duration=20)),
            ("Regen +2",  RegenerationEffect(regen_rate=2)),
            ("Damage +2", DamageBoostEffect(amount=2)),
            ("Speed +8",  SpeedBoostEffect(amount=8)),
        ]
        bus.emit(ShowBonusSelector(options=options))

    def _on_bonus_selected(self, e: BonusSelected):

        self.paused = False

    def _random_spawn_pos(self, radius: float,
                          center: pygame.Vector2) -> pygame.Vector2:
        angle = random.uniform(0, 2 * math.pi)
        x     = center.x + radius * math.cos(angle)
        y     = center.y + radius * math.sin(angle)
        return pygame.Vector2(x, y)

    def update(self, dt: float):
        # 1) Всегда обновляем все эффекты (включая селектор)
        for effect in self.field.effects:
            effect.update(dt)

        # 2) In-place очистка списков по «жизни» и дистанции
        px, py      = self.field.player.pos
        max_dist_sq = 800 * 800

        for lst, attr in [
            (self.field.projectiles, 'alive'),
            (self.field.effects,     'alive'),
            (self.field.enemies,     'hp'),
        ]:
            for i in range(len(lst) - 1, -1, -1):
                item = lst[i]

                # удаляем по признаку «мертв»
                if not getattr(item, attr, True):
                    del lst[i]
                    continue

                # удаляем по дистанции, если есть .pos
                if hasattr(item, 'pos'):
                    dx = item.pos.x - px
                    dy = item.pos.y - py
                    if dx*dx + dy*dy > max_dist_sq:
                        del lst[i]

        # 3) Если пауза — пропускаем всю остальную логику
        if self.paused:
            return

        # 4) Спавн врагов
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_rate:
            self.spawn_timer -= self.spawn_rate
            pos = self._random_spawn_pos(400, self.field.player.pos)

            if random.random() < 0.5:
                weapon, etype, speed, scale = Bow(range=300, rate=1.2, damage=6), "Spider", 25, 1.6
            else:
                weapon, etype, speed, scale = Sword(range=20, rate=1.5, damage=12), "Zombie", 48, 2.4

            self.field.enemies.append(
                Enemy(pos, weapon, etype, speed, scale)
            )

        # 5) Обновляем игрока и камеру
        self.field.player.update(dt)
        self.camera.update(self.field.player.pos)

        # 6) Обновляем врагов и их атаки
        for en in self.field.enemies:
            en.update(dt, self.field.player.pos)
            if en.weapon:
                en.weapon.on_attack(en.pos, [self.field.player], owner=en)

        # 7) Игрок атакует
        self.field.player.weapon.on_attack(
            self.field.player.pos,
            self.field.enemies,
            owner=self.field.player
        )

        # 8) Обновляем снаряды
        for p in self.field.projectiles:
            p.update(dt)

        # 9) Проверка попаданий
        units = [self.field.player] + self.field.enemies

        # collision & cleanup: iterate backwards
        for i in range(len(self.field.projectiles) - 1, -1, -1):
            proj = self.field.projectiles[i]
            # out-of-range or dead
            if not proj.alive or (proj.pos - proj.spawn_pos).length_squared() > MAX_PROJECTILE_DIST_SQ:
                del self.field.projectiles[i]
                continue

            if proj.target:
                # directed projectile
                if (proj.pos - proj.target.pos).length_squared() < HIT_RADIUS_SQ:
                    proj.target.take_damage(proj.damage)
                    proj.alive = False
            else:
                # free projectile: hit any enemy of opposite team
                for unit in units:
                    if unit.team != proj.team and (proj.pos - unit.pos).length_squared() < HIT_RADIUS_SQ:
                        unit.take_damage(proj.damage)
                        proj.alive = False
                        break

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

        pygame.quit()
