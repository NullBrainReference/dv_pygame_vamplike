import pygame
from Animation.AnimationLibrary import ANIMATION_LIBRARY
from .Unit import Unit
from Weapon.Weapon import Weapon
from UI.HPBar import draw_hp_bar

class Player(Unit):
    def __init__(self, weapon: Weapon):
        super().__init__(hp=100, weapon=weapon)
        self.pos = pygame.Vector2(400, 300)

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

        # Флаг смерти
        self.is_dead = False

    def update(self, dt: float):
        # Если умер — проигрываем только death-анимацию один раз
        if self.is_dead:
            self._update_death_animation(dt)
            return

        # Пока жив — обновляем оружие и idle-анимацию
        self.weapon.update(dt)
        self.current_anim = self.animations["idle"]

        self._advance_frame(dt)

    def draw(self, screen: pygame.Surface):
        frame = self.current_anim.frames[self.anim_frame_idx]
        rect  = frame.get_rect(center=self.pos)
        screen.blit(frame, rect)

        # HP-бар не рисуем, если уже умер
        if not self.is_dead:
            draw_hp_bar(screen, self, offset_y=-20)

    def on_death(self):
        if self.is_dead:
            return
        
        self.is_dead        = True
        self.current_anim   = self.animations["death"]
        self.anim_timer     = 0.0
        self.anim_frame_idx = 0

    def _advance_frame(self, dt: float):
        """Обычный цикл кадра для бесконечных анимаций."""
        self.anim_timer += dt
        frame_duration = 1.0 / self.current_anim.frame_rate

        if self.anim_timer >= frame_duration:
            self.anim_timer -= frame_duration
            self.anim_frame_idx = (self.anim_frame_idx + 1) % len(self.current_anim.frames)

    def _update_death_animation(self, dt: float):
        """Проигрываем death-анимацию один раз и останавливаемся на последнем кадре."""
        # Если анимация уже закончилась — ничего не делаем
        if self.anim_frame_idx >= len(self.current_anim.frames) - 1:
            return

        # Иначе продвигаем кадр по таймеру
        self.anim_timer += dt
        frame_duration = 1.0 / self.current_anim.frame_rate

        if self.anim_timer >= frame_duration:
            self.anim_timer -= frame_duration
            self.anim_frame_idx += 1
            # clamp на последний кадр
            if self.anim_frame_idx >= len(self.current_anim.frames):
                self.anim_frame_idx = len(self.current_anim.frames) - 1
