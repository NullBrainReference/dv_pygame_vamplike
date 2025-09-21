
from abc import ABC, abstractmethod

class Effect(ABC):
    def __init__(self, duration: float | None):
        # None → бесконечный эффект
        self.duration = float('inf') if duration is None else duration
        self.elapsed  = 0.0

    def update(self, dt: float, unit):
        if self.is_expired:
            return
        self.apply(dt, unit)
        self.elapsed += dt

    @abstractmethod
    def apply(self, dt: float, unit):
        pass

    @property
    def is_expired(self) -> bool:
        return self.elapsed >= self.duration
