import pygame
from Unit.Unit import Unit
from Weapon.Weapon import Weapon
from UI.HPBar import draw_hp_bar

class Enemy(Unit):
    def __init__(self, pos, weapon : Weapon):
        super().__init__(hp=30, weapon=weapon)
        self.pos = pos
        self.speed = 1.5

    def update(self, dt, player_pos):
        direction = (player_pos - self.pos).normalize()
        self.pos += direction * self.speed
        self.weapon.update(dt)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (*self.pos, 20, 20))
        draw_hp_bar(screen, self)

    def on_death(self):
        print("Враг уничтожен")
