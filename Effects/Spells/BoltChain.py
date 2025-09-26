import pygame
import random
from GameManagement.Camera import Camera

class BoltChainEffect:
    def __init__(self,
                 start_unit,
                 limit: int     = 5,
                 range: float   = 50,
                 damage: float  = 8,
                 duration: float = 0.4,
                 jitter_interval: float = 0.1,
                 jitter_offset_range: float = 15):
        self.targets             = []
        self.limit               = limit
        self.range               = range
        self.damage              = damage
        self.timer               = 0.0
        self.duration            = duration
        self.alive               = True

        # jitter settings
        self.jitter_interval     = jitter_interval
        self._jitter_timer       = 0.0
        self.jitter_offset_range = jitter_offset_range
        self._offsets            = []  # will hold Vector2 offsets per segment

        # include the starting unit
        self.apply(0.0, start_unit)

    def apply(self,
              dt: float,
              unit,
              event: str | None = None,
              **kwargs):
        # limit jumps
        if len(self.targets) >= self.limit:
            return

        # distance check
        last_pos = self.targets[-1].pos if self.targets else unit.pos
        if last_pos.distance_to(unit.pos) > self.range:
            return

        # deal damage and add to chain
        unit.take_damage(self.damage)
        self.targets.append(unit)

        # rebuild offsets array to match new segment count
        seg_count = max(0, len(self.targets) - 1)
        self._offsets = [pygame.Vector2(0, 0) for _ in range(seg_count)]

    def update(self, dt: float):
        # lifetime expiration
        self.timer += dt
        if self.timer >= self.duration:
            self.alive = False
            return

        # update jitter timer
        self._jitter_timer += dt
        if self._jitter_timer >= self.jitter_interval:
            self._jitter_timer -= self.jitter_interval
            # recalc random offsets for each segment
            for i in range(len(self._offsets)):
                dx = random.uniform(-self.jitter_offset_range,
                                     self.jitter_offset_range)
                dy = random.uniform(-self.jitter_offset_range,
                                     self.jitter_offset_range)
                self._offsets[i] = pygame.Vector2(dx, dy)

    def draw(self,
             screen: pygame.Surface,
             camera: Camera):
        # need at least two points
        if len(self.targets) < 2:
            return

        color = (200, 240, 255)
        width = 3

        # get screen coords
        points = [camera.apply(u.pos) for u in self.targets]

        # draw each segment with jittered midpoint
        for i in range(len(points) - 1):
            p1 = pygame.Vector2(points[i])
            p2 = pygame.Vector2(points[i + 1])
            offset = self._offsets[i] if i < len(self._offsets) else pygame.Vector2(0, 0)
            midpoint = (p1 + p2) * 0.5 + offset

            # two sub-segments: p1→mid, mid→p2
            pygame.draw.line(screen, color, p1, midpoint, width)
            pygame.draw.line(screen, color, midpoint, p2, width)
