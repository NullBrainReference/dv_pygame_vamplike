
import pygame, requests
import random
import math

from Events.EventBus      import bus
from Events.Events        import (
    SpawnProjectile,
    SpawnEffect,
    # GainExp,
    LevelUp,
    ShowBonusSelector,
    BonusSelected,
    RequestTargets,
    ProvideTargets,
    HideEscMenu,
    ShowEscMenu,
    QuitGame,
    # Continue,
    PlayerDied
)
# from Unit.Enemy           import Enemy
# from Weapon.Sword        import Sword
# from Weapon.Bow           import Bow
# from Weapon.Staff         import SummoningStaff 
from GameManagement.GameField import GameField
from .Camera              import Camera
from Effects.BonusSelectorEffect  import BonusSelectorEffect
from Effects.RegenerationEffect   import RegenerationEffect
from Effects.DamageBoostEffect    import DamageBoostEffect
from Effects.SpeedBoostEffect     import SpeedBoostEffect
from Effects.AdrenalinSpeedEffect import AdrenalinSpeedEffect
from Effects.SpikesCastEffect     import SpikesCastEffect
from Effects.MultiCastEffect      import MultiCastEffect
from Effects.VampiricEffect       import VampiricEffect
from Effects.LightningHitEffect   import LightningHitEffect

# from .SpawnController         import SpawnController
# from .SummonerSpawnController import SummonerSpawnController
from .SpawnersSetup import get_spawners
from Weapon.Weapon  import MAX_PROJECTILE_DIST_SQ

from Collision.Physics import physics_step
from UI.FPSCounter     import FPSCounter 
from UI.EscMenu        import EscMenu
from UI.NameInput      import NameInput
from UI.ScoreUI        import ScoreUI

from Pool.pools import projectile_pool

class GameManager:
    def __init__(self, screen):
        self.screen      = screen
        self.clock       = pygame.time.Clock()
        self.field       = GameField()
        self.spawn_timer = 0.0
        self.spawn_rate  = 2.0   # seconds between spawns
        self.paused      = False
        self.running     = True
        self.menu_opened = False
        self.selecting   = False

        self.camera = Camera(screen.get_size())

        self.font = pygame.font.Font("Assets/Font/Caudex-Regular.ttf", 20)
        self.fps_counter = FPSCounter(self.font)

        self.spawners = get_spawners()

        bus.subscribe(ShowEscMenu, lambda e: self._show_esc_menu())
        bus.subscribe(HideEscMenu, lambda e: self._hide_esc_menu())
        bus.subscribe(QuitGame,    lambda e: self._quit_game())

        bus.subscribe(SpawnProjectile,  lambda e: self.field.projectiles.append(e.projectile))
        bus.subscribe(SpawnEffect,      lambda e: self.field.effects.append(e.effect))
        bus.subscribe(LevelUp,          self._on_level_up)
        bus.subscribe(ShowBonusSelector,
                      lambda e: self.field.effects.append(BonusSelectorEffect(e.options)))
        bus.subscribe(BonusSelected,    self._on_bonus_selected)
        bus.subscribe(RequestTargets,   self._on_request_targets)
        bus.subscribe(PlayerDied,       self._on_player_died)

        self._select_start_ability()

    def _on_request_targets(self, e: RequestTargets):
        units = self.field.enemies + [self.field.player]
        
        candidates = [
            u for u in units
            if (u.pos - e.origin).length() <= e.radius
        ]
        
        bus.emit(ProvideTargets(effect=e.effect, candidates=candidates))

    def _on_level_up(self, e: LevelUp):
        self.paused = True
        self.selecting = True
        self.field.player.max_hp += 5

        bonus_options = [
            ("Spikes: Cast spikes on hit taken (25%)",  SpikesCastEffect()),
            ("Adrenalin: 40 speed on hit taken (25%)",  AdrenalinSpeedEffect()),
            ("Multicast: 3/4 attack cd recuction (20%)\nOn your attack", MultiCastEffect()),
            ("Lightning: Casts lightning (20%)\nOn your attack", LightningHitEffect())
        ]

        options = [
            ("Vampiric + 3",  VampiricEffect(amount=3)),
            ("Regen +2",  RegenerationEffect(regen_rate=2)),
            ("Damage +4", DamageBoostEffect(amount=4)),
            ("Speed +8",  SpeedBoostEffect(amount=8)),
        ]

        extra_name, extra_cls = random.choice(bonus_options)
        options.append((extra_name, extra_cls))

        bus.emit(ShowBonusSelector(options=options))

    def _on_bonus_selected(self, e: BonusSelected):
        self.selecting = False
        self.paused = False

    def _random_spawn_pos(self, radius: float,
                          center: pygame.Vector2) -> pygame.Vector2:
        angle = random.uniform(0, 2 * math.pi)
        x     = center.x + radius * math.cos(angle)
        y     = center.y + radius * math.sin(angle)
        return pygame.Vector2(x, y)

    def _select_start_ability(self):
        self.paused = True
        self.selecting = True

        options = [
            ("Spikes: Cast spikes on hit taken (25%)",  SpikesCastEffect()),
            ("Adrenalin: 40 speed on hit taken (25%)",  AdrenalinSpeedEffect()),
            ("Multicast: 3/4 attack cd recuction (20%)\nOn your attack", MultiCastEffect()),
            ("Lightning: Casts lightning (20%)\nOn your attack", LightningHitEffect())
        ]

        bus.emit(ShowBonusSelector(options=options))

    def _show_esc_menu(self):
        self.menu_opened = True
        self.paused = True
        self.field.effects.append(EscMenu(self.font))

    def _hide_esc_menu(self):
        self.menu_opened = False
        if not self.selecting:
            self.paused = False


    def _on_player_died(self, event):
        def submit_callback(username, score):
            try:
                payload = {"username": username, "score": int(score)}
                requests.post("http://127.0.0.1:8000/submit", json=payload)
            except Exception as e:
                print("Error posting score:", e)
            self.field.effects.append(ScoreUI(self.font))

        self.paused = True
        self.field.effects.append(NameInput(self.font, self.field.player.score, submit_callback))



    def _quit_game(self):
        self.running = False

    def update(self, dt: float):
        for effect in self.field.effects:
            effect.update(dt)

        px, py      = self.field.player.pos
        max_dist_sq = 800 * 800

        for lst, attr in [
            (self.field.projectiles, 'alive'),
            (self.field.effects,     'alive'),
            (self.field.enemies,     'hp'),
        ]:
            for i in range(len(lst) - 1, -1, -1):
                item = lst[i]

                # remove by attribute
                if not getattr(item, attr, True):
                    del lst[i]
                    continue

                # remove by distance
                if hasattr(item, 'pos'):
                    dx = item.pos.x - px
                    dy = item.pos.y - py
                    if dx*dx + dy*dy > max_dist_sq:
                        del lst[i]

        if self.paused:
            return

        progression = min(self.field.player.level / 10, 1.0)

        for spawner in self.spawners:
            spawner.spawn(dt, progression, self.field)

        self.field.player.update(dt)
        self.camera.update(self.field.player.pos, dt)

        for en in self.field.enemies:
            en.update(dt, self.field.player.pos)
            if en.weapon:
                en.weapon.on_attack(en.pos, [self.field.player], owner=en)

        self.field.player.weapon.on_attack(
            self.field.player.pos,
            self.field.enemies,
            owner=self.field.player
        )

        for p in self.field.projectiles:
            p.update(dt)

        # Collision & cleanup: iterate backwards
        units = [self.field.player] + self.field.enemies

        physics_step(units, dt)

        for i in range(len(self.field.projectiles) - 1, -1, -1):
            proj = self.field.projectiles[i]

            # out-of-range or dead
            if (not proj.alive
                or (proj.pos - self.field.player.pos).length_squared() > 600 * 600):
                projectile_pool.release(proj)
                del self.field.projectiles[i]
                print("proj released")
                continue

            if proj.target:
                # directed projectile
                if proj.collider.intersects(proj.target.collider):
                    proj.target.take_damage(proj.damage)
                    projectile_pool.release(proj)
                    del self.field.projectiles[i]
                    continue
            else:
                # free projectile
                for unit in units:
                    if unit.team != proj.team \
                    and proj.collider.intersects(unit.collider):
                        unit.take_damage(proj.damage)
                        projectile_pool.release(proj)
                        del self.field.projectiles[i]
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
        
        self.fps_counter.draw(self.screen, self.clock)

        pygame.display.flip()

    def _handle_event(self, ev):
        if ev.type == pygame.QUIT:
            self.running = False
            return

        # forward to effects
        for effect in self.field.effects:
            if hasattr(effect, "handle_event"):
                effect.handle_event(ev)

        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            if self.menu_opened:
                bus.emit(HideEscMenu())
            else:
                bus.emit(ShowEscMenu())


    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            for ev in pygame.event.get():
                self._handle_event(ev)

            self.update(dt)
            self.draw()
            
        pygame.quit()
