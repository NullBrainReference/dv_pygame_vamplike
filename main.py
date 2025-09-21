import pygame
from GameManagement.GameManager import GameManager

pygame.init()
screen = pygame.display.set_mode((800, 600))
game = GameManager(screen)
game.run()
