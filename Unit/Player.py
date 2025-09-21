import pygame
from Unit.Unit import Unit
from Weapon.Weapon import Weapon
from UI.HPBar import draw_hp_bar

class Player(Unit):
    def __init__(self, weapon : Weapon):
        super().__init__(hp=100, weapon=weapon)
        self.pos = pygame.Vector2(400, 300)

    def update(self, dt):
        self.weapon.update(dt)

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), self.pos, 20)
        draw_hp_bar(screen, self, -10)

    def on_death(self):
        print("Игрок погиб!")
