# Unit/Player.py
import pygame
from Animation.AnimationLibrary import ANIMATION_LIBRARY
from .Unit import Unit
from Weapon.Weapon import Weapon
from UI.HPBar import draw_hp_bar

class Player(Unit):
    def __init__(self, weapon: Weapon):
        super().__init__(hp=100, weapon=weapon)
        self.pos = pygame.Vector2(400, 300)

        # Словарь анимаций
        self.animations = {
            "idle": ANIMATION_LIBRARY.get("Player.idle"),
            "side": ANIMATION_LIBRARY.get("Player.side"),
            "up":   ANIMATION_LIBRARY.get("Player.up"),
            "down": ANIMATION_LIBRARY.get("Player.down"),
        }

        # Текущая анимация и её состояние
        self.current_anim   = self.animations["idle"]
        self.anim_timer     = 0.0
        self.anim_frame_idx = 0

    def update(self, dt: float):
        # Обновляем таймер оружия
        self.weapon.update(dt)

        # Пока оставляем только idle-анимацию
        self.current_anim = self.animations["idle"]

        # Переключаем кадры по frame_rate
        self.anim_timer += dt
        frame_duration = 1.0 / self.current_anim.frame_rate
        if self.anim_timer >= frame_duration:
            self.anim_timer -= frame_duration
            self.anim_frame_idx = (self.anim_frame_idx + 1) % len(self.current_anim.frames)

    def draw(self, screen: pygame.Surface):
        # Отрисовываем текущий кадр анимации
        frame = self.current_anim.frames[self.anim_frame_idx]
        rect  = frame.get_rect(center=self.pos)
        screen.blit(frame, rect)

        # HP-бар над головой
        draw_hp_bar(screen, self, offset_y=-20)

    def on_death(self):
        print("Игрок погиб!")

