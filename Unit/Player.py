
import pygame
from Animation.AnimationLibrary import ANIMATION_LIBRARY
from .Unit import Unit
from Weapon.Weapon import Weapon
from UI.HPBar import draw_hp_bar
from UI.WeaponSelector import draw_weapon_icons
from UI.LevelBar import draw_level_progress
from GameManagement.Camera import Camera
from Effects.RegenerationEffect import RegenerationEffect
from Weapon.Bow import Bow
from Weapon.Weapon import Halberd
from Events.Events import GainExp, LevelUp, BonusSelected
from Events.EventBus import bus


class Player(Unit):
    def __init__(self, weapon: Weapon):
        super().__init__(hp=100, weapon=weapon)
        self.pos   = pygame.Vector2(400, 300)
        self.speed = 42
        self.scale = 2

        # exp / level
        self.exp       = 0
        self.level     = 1
        self.max_exp   = 100

        # Словарь анимаций, включая death
        self.animations = {
            "idle":  ANIMATION_LIBRARY.get("Player.idle"),
            "side":  ANIMATION_LIBRARY.get("Player.side"),
            "up":    ANIMATION_LIBRARY.get("Player.up"),
            "down":  ANIMATION_LIBRARY.get("Player.down"),
            "death": ANIMATION_LIBRARY.get("Player.death"),
        }

        self.weapons = {
            "bow":   Bow(range=320, rate=1.5, damage=8),
            "halberd": Halberd(range=75,
                              rate=1.2,
                              damage=18,
                              sprite_path="Assets/Weapons/halberd.png",
                              spin_speed=-360,
                              duration=1)
        }
        self.selected_weapon = "bow"
        self.weapon = self.weapons[self.selected_weapon]

        # Anim state
        self.current_anim   = self.animations["idle"]
        self.anim_timer     = 0.0
        self.anim_frame_idx = 0
        self.flip_horiz     = False

        self.is_dead = False
        self.team = "player"

        bus.subscribe(GainExp,       self._on_gain_exp)
        bus.subscribe(BonusSelected, self._on_bonus_selected)

        self.add_effect(RegenerationEffect(regen_rate=3, duration=None))

    def update(self, dt: float):
        if self.is_dead:
            self._update_death_animation(dt)
            return

        self.update_effects(dt)
        self.weapon.update(dt)

        keys = pygame.key.get_pressed()
        move = pygame.Vector2(
            (keys[pygame.K_d] - keys[pygame.K_a]),
            (keys[pygame.K_s] - keys[pygame.K_w])
        )

        if move.length_squared() > 0:
            # Movement
            dir_norm = move.normalize()
            self.pos += dir_norm * self.speed * dt

            # anim selection
            if abs(dir_norm.x) > abs(dir_norm.y):
                self.current_anim = self.animations["side"]
                self.flip_horiz   = dir_norm.x < 0
            elif dir_norm.y < 0:
                self.current_anim = self.animations["up"]
                self.flip_horiz   = False
            else:
                self.current_anim = self.animations["down"]
                self.flip_horiz   = False
        else:
            self.current_anim = self.animations["idle"]
            self.flip_horiz   = False

        if keys[pygame.K_1] and self.selected_weapon != "bow":
            self.switch_weapon("bow")
        elif keys[pygame.K_2] and self.selected_weapon != "halberd":
            self.switch_weapon("halberd")

        self._advance_frame(dt)

    def draw(self, screen: pygame.Surface, camera: Camera):
        orig = self.current_anim.frames[self.anim_frame_idx]
        sc = self.scale
        frame = pygame.transform.scale(orig, (orig.get_width()*sc, orig.get_height()*sc))
        # frame = self.current_anim.frames[self.anim_frame_idx]
        if self.flip_horiz:
            frame = pygame.transform.flip(frame, True, False)

        screen_pos = camera.apply(self.pos)
        rect = frame.get_rect(center=screen_pos)
        screen.blit(frame, rect)

        if not self.is_dead:

            bar_pos = camera.apply(self.pos) + pygame.Vector2(0, -20)
            draw_hp_bar(screen, self, pos=bar_pos)
            draw_weapon_icons(self, screen)
            draw_level_progress(self, screen)


    def on_death(self):
        if self.is_dead:
            return
        self.is_dead        = True
        self.current_anim   = self.animations["death"]
        self.anim_timer     = 0.0
        self.anim_frame_idx = 0

    def _advance_frame(self, dt: float):

        self.anim_timer += dt
        frame_duration = 1.0 / self.current_anim.frame_rate

        if self.anim_timer >= frame_duration:
            self.anim_timer     -= frame_duration
            self.anim_frame_idx = (self.anim_frame_idx + 1) % len(self.current_anim.frames)

    def _update_death_animation(self, dt: float):

        if self.anim_frame_idx >= len(self.current_anim.frames) - 1:
            return

        self.anim_timer += dt
        frame_duration = 1.0 / self.current_anim.frame_rate

        if self.anim_timer >= frame_duration:
            self.anim_timer     -= frame_duration
            self.anim_frame_idx += 1
            # не выходим за границы
            if self.anim_frame_idx >= len(self.current_anim.frames):
                self.anim_frame_idx = len(self.current_anim.frames) - 1

    def switch_weapon(self, name: str):
        if name in self.weapons:
            self.selected_weapon = name
            self.weapon = self.weapons[name]

    def _on_gain_exp(self, e: GainExp):
        self.exp += e.amount
        if self.exp >= self.max_exp:
            self.exp -= self.max_exp
            self.level += 1
            self.max_exp = int(self.max_exp * 1.5)
            # Уведомляем об уровне и зовём селектор
            bus.emit(LevelUp(new_level=self.level))

    def _on_bonus_selected(self, e: BonusSelected):
        # Находим выбранный эффект и добавляем его
        self.add_effect(e.effect)