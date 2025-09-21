
import pygame
from Animation.AnimationLibrary import ANIMATION_LIBRARY
from .Unit import Unit
from Weapon.Weapon import Weapon
from UI.HPBar import draw_hp_bar
from GameManagement.Camera import Camera
from Effects.RegenerationEffect import RegenerationEffect

class Player(Unit):
    def __init__(self, weapon: Weapon):
        super().__init__(hp=100, weapon=weapon)
        self.pos   = pygame.Vector2(400, 300)
        self.speed = 42
        self.scale = 2

        # Словарь анимаций, включая death
        self.animations = {
            "idle":  ANIMATION_LIBRARY.get("Player.idle"),
            "side":  ANIMATION_LIBRARY.get("Player.side"),
            "up":    ANIMATION_LIBRARY.get("Player.up"),
            "down":  ANIMATION_LIBRARY.get("Player.down"),
            "death": ANIMATION_LIBRARY.get("Player.death"),
        }

        # Состояние анимации
        self.current_anim   = self.animations["idle"]
        self.anim_timer     = 0.0
        self.anim_frame_idx = 0
        self.flip_horiz     = False

        self.is_dead = False
        self.add_effect(RegenerationEffect(regen_rate=1, duration=None))

    def update(self, dt: float):
        # Смерть: только death-анимация
        if self.is_dead:
            self._update_death_animation(dt)
            return

        self.update_effects(dt)
        self.weapon.update(dt)

        # 2) Обрабатываем ввод WASD
        keys = pygame.key.get_pressed()
        move = pygame.Vector2(
            (keys[pygame.K_d] - keys[pygame.K_a]),
            (keys[pygame.K_s] - keys[pygame.K_w])
        )

        if move.length_squared() > 0:
            # движение
            dir_norm = move.normalize()
            self.pos += dir_norm * self.speed * dt

            # выбираем анимацию по направлению
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
            # стоим на месте
            self.current_anim = self.animations["idle"]
            self.flip_horiz   = False

        # 3) Продвигаем кадр
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
            # HP-бар тоже смещаем через camera
            bar_pos = camera.apply(self.pos) + pygame.Vector2(0, -20)
            draw_hp_bar(screen, self, pos=bar_pos)


    def on_death(self):
        if self.is_dead:
            return
        self.is_dead        = True
        self.current_anim   = self.animations["death"]
        self.anim_timer     = 0.0
        self.anim_frame_idx = 0

    def _advance_frame(self, dt: float):
        """Зацикленная анимация (idle, walk...)."""
        self.anim_timer += dt
        frame_duration = 1.0 / self.current_anim.frame_rate

        if self.anim_timer >= frame_duration:
            self.anim_timer     -= frame_duration
            self.anim_frame_idx = (self.anim_frame_idx + 1) % len(self.current_anim.frames)

    def _update_death_animation(self, dt: float):
        """Проигрываем death-анимацию один раз."""
        # если уже на последнем кадре — выходим
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
