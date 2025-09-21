
import pygame

class AnimationFrames:
    def __init__(self, frames: list[pygame.Surface], frame_rate: float):
        # frames — список Surface по порядку
        # frame_rate — сколько кадров в секунду показывать
        self.frames = frames
        self.frame_rate = frame_rate