import pygame
from typing import Protocol

class IPosition(Protocol):
    @property
    def pos(self) -> pygame.Vector2:
        pass
