
import pygame
from Animation.AnimationLibrary import ANIMATION_LIBRARY

def setup_animations():
    pygame.init()

    ANIMATION_LIBRARY.load_unit_animations(
        unit_name="Player",
        dir_path="Assets/Units/Player",
        frame_size=(16, 16),
        frame_rate=4
    )

    ANIMATION_LIBRARY.load_unit_animations(
        unit_name="Spider",
        dir_path="Assets/Units/Spider",
        frame_size=(16, 16),
        frame_rate=4
    )

    
    ANIMATION_LIBRARY.load_unit_animations(
        unit_name="Zombie",
        dir_path="Assets/Units/Zombie",
        frame_size=(16, 16),
        frame_rate=4
    )

    
    ANIMATION_LIBRARY.load_unit_animations(
        unit_name="Staffdude",
        dir_path="Assets/Units/Staffdude",
        frame_size=(16, 16),
        frame_rate=4
    )

    ANIMATION_LIBRARY.load_unit_animations(
        unit_name="Ghost",
        dir_path="Assets/Units/Ghost",
        frame_size=(16, 16),
        frame_rate=1
    )


