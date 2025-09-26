# Unit/Enemy.py
import pygame
from Unit.Unit import Unit
from Weapon.Weapon import Weapon
from UI.HPBar import draw_hp_bar
from Animation.AnimationLibrary import ANIMATION_LIBRARY
from GameManagement.Camera import Camera
from Events.Events      import GainExp
from Events.EventBus    import bus
from Effects.Visual.DamageFlashEffect import DamageFlashEffect

class Enemy(Unit):
    def __init__(self,
                 pos: pygame.Vector2,
                 hp: float,
                 weapon: Weapon,
                 enemy_type: str,
                 speed: float = 4,
                 scale: int = 1,
                 reward: int = 30):
        super().__init__(hp=hp, weapon=weapon)
        self.pos = pos
        self.speed = speed
        self.enemy_type = enemy_type
        self.reward = reward

        self.scale = scale

        self.animations = {
            state: ANIMATION_LIBRARY.get(f"{enemy_type}.{state}")
            for state in ("idle", "side", "up", "down")
        }

        # Anim state
        self.current_anim   = self.animations["idle"]
        self.anim_timer     = 0.0
        self.anim_frame_idx = 0
        self.flip_horiz     = False
        self.flash_tint     = None

        self.team = "enemy"

    def update(self, dt: float, player_pos: pygame.Vector2):
        self.update_effects(dt)

        if self.weapon:
            self.weapon.update(dt)

        direction = player_pos - self.pos
        

        if direction.length_squared() >= 100:
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

    def draw(self, screen: pygame.Surface, camera: Camera):
        orig = self.current_anim.frames[self.anim_frame_idx]
        sc   = self.scale
        frame = pygame.transform.scale(
            orig,
            (orig.get_width() * sc, orig.get_height() * sc)
        )
        if self.flip_horiz:
            frame = pygame.transform.flip(frame, True, False)

        # apply tint if set by DamageFlashEffect
        tint = getattr(self, "flash_tint", None)
        if tint:
            overlay = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            overlay.fill(tint)
            frame.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        screen_pos = camera.apply(self.pos)
        rect       = frame.get_rect(center=screen_pos)
        screen.blit(frame, rect)

        bar_pos = screen_pos + pygame.Vector2(0, -20)
        draw_hp_bar(screen, self, pos=bar_pos)

    def on_death(self):
        bus.emit(GainExp(amount=self.reward))
        print(f"{self.enemy_type} Killed! Exp: +{self.reward}")

