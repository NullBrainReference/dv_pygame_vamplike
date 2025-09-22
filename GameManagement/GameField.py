import pygame
from Unit.Player import Player
from Weapon.Bow import Bow

class GameField:
    def __init__(self):
        self.player = Player(Bow(range=300, rate=1.0, damage=10))
        self.enemies = []
        self.projectiles = []
        self.effects = []
