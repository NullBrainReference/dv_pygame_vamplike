# Unit/Enemy.py
import pygame
from Unit.Unit import Unit
from Weapon.Weapon import Weapon
from UI.HPBar import draw_hp_bar
from Animation.AnimationLibrary import ANIMATION_LIBRARY
from GameManagement.Camera import Camera

class Enemy(Unit):
    def __init__(self,
                 pos: pygame.Vector2,
                 weapon: Weapon,
                 enemy_type: str,
                 speed: float = 4,
                 scale: int = 1):
        super().__init__(hp=30, weapon=weapon)
        self.pos = pos
        self.speed = speed
        self.enemy_type = enemy_type

        self.scale = scale

        # Загрузка анимаций для этого типа (idle, side, up, down)
        self.animations = {
            state: ANIMATION_LIBRARY.get(f"{enemy_type}.{state}")
            for state in ("idle", "side", "up", "down")
        }

        # Состояние анимации
        self.current_anim   = self.animations["idle"]
        self.anim_timer     = 0.0
        self.anim_frame_idx = 0
        self.flip_horiz     = False  # отразить по горизонтали (для side)

    def update(self, dt: float, player_pos: pygame.Vector2):
        # Обновляем оружие
        self.weapon.update(dt)

        # Движемся к игроку
        direction = player_pos - self.pos
        
        # if direction.length_squared() > 0 and direction.length() >= 10:
        if direction.length() >= 10:
            dir_norm = direction.normalize()
            self.pos += dir_norm * self.speed * dt

            # Выбираем анимацию по направлению
            if abs(dir_norm.x) > abs(dir_norm.y):
                self.current_anim = self.animations["side"]
                self.flip_horiz = dir_norm.x < 0
            elif dir_norm.y < 0:
                self.current_anim = self.animations["up"]
                self.flip_horiz = False
            else:
                self.current_anim = self.animations["down"]
                self.flip_horiz = False

        else:
            self.current_anim = self.animations["idle"]
            self.flip_horiz = False

        # Animation frame update
        self.anim_timer += dt
        frame_duration = 1.0 / self.current_anim.frame_rate
        if self.anim_timer >= frame_duration:
            self.anim_timer -= frame_duration
            self.anim_frame_idx = (self.anim_frame_idx + 1) % len(self.current_anim.frames)

# Unit/Enemy.py
    def draw(self, screen: pygame.Surface, camera: Camera):
        # frame = self.current_anim.frames[self.anim_frame_idx]
        orig = self.current_anim.frames[self.anim_frame_idx]
        sc = self.scale
        frame = pygame.transform.scale(orig, (orig.get_width()*sc, orig.get_height()*sc))
        if self.flip_horiz:
            frame = pygame.transform.flip(frame, True, False)

        screen_pos = camera.apply(self.pos)
        rect = frame.get_rect(center=screen_pos)
        screen.blit(frame, rect)

        bar_pos = screen_pos + pygame.Vector2(0, -20)
        draw_hp_bar(screen, self, pos=bar_pos)

    def on_death(self):
        print(f"{self.enemy_type} уничтожен!")
