
import pygame
from Animation.AnimationLibrary import ANIMATION_LIBRARY

def setup_animations():
    pygame.init()

    ANIMATION_LIBRARY.load_unit_animations(
        unit_name="Player",
        dir_path="Assets/Units/Player",
        frame_size=(16, 16),
        frame_rate=8
    )

    # ANIMATION_LIBRARY.load_unit_animations(
    #     unit_name="Enemy",
    #     dir_path="Assets/Units/Enemy",
    #     frame_size=(16, 16),
    #     frame_rate=6
    # )
