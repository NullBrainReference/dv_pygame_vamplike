import pygame
from GameManagement.GameManager import GameManager
from Animation.AnimationSetup import setup_animations

pygame.init()
screen = pygame.display.set_mode((800, 600))

setup_animations()

game = GameManager(screen)
game.run()
