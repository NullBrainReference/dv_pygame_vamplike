
import pygame
from Effects.Effect import Effect

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def lerp_color(c1: pygame.Color, c2: pygame.Color, t: float) -> pygame.Color:
    return pygame.Color(
        max(0, min(255, int(lerp(c1.r, c2.r, t)))),
        max(0, min(255, int(lerp(c1.g, c2.g, t)))),
        max(0, min(255, int(lerp(c1.b, c2.b, t)))),
        max(0, min(255, int(lerp(c1.a, c2.a, t)))),
    )

class DamageFlashEffect(Effect):
    """
    On damage → flash sprite tint original -> flash_color -> original
    over two phases of total duration = half_duration * 2.
    Never expires from unit.effects.
    """
    def __init__(self,
                 flash_color: pygame.Color = pygame.Color(255, 0, 0, 255),
                 half_duration: float = 0.15):
        super().__init__(duration=None)
        self.flash_color    = flash_color
        self.half_duration  = half_duration
        self.total_duration = half_duration * 2
        self._timer         = self.total_duration
        # default original tint = white, full alpha
        self._orig_color    = pygame.Color(255, 255, 255, 255)

    def apply(self,
              dt: float,
              unit,
              event: str | None = None,
              **kwargs):
        if event != "damage":
            return
        # retrigger only if previous flash finished
        if self._timer < self.total_duration:
            return
        self._timer = 0.0

    def update(self, dt: float, unit):
        # advance flash timer
        if self._timer < self.total_duration:
            self._timer = min(self._timer + dt, self.total_duration)
            # compute normalized t in [0,1]
            t = self._timer / self.total_duration
            # ramp up to 1 then down to 0
            if t <= 0.5:
                mix = t * 2
            else:
                mix = (1 - t) * 2
            unit.flash_tint = lerp_color(self._orig_color,
                                         self.flash_color,
                                         mix)
        else:
            # done flashing
            unit.flash_tint = None
