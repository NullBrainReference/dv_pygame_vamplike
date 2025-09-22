
from abc import ABC, abstractmethod
import math


class Effect(ABC):
    def __init__(self, duration: float | None):
        # None → бесконечно
        self.duration = math.inf if duration is None else duration
        self.elapsed  = 0.0

    def update(self, dt: float, unit):
        # вызываем только если ещё есть время
        if self.is_expired:
            return
        
        # per-frame-применение
        self.apply(dt, unit)
        self.elapsed += dt

    @abstractmethod
    def apply(self,
              dt: float,
              unit,
              event: str | None = None,
              **kwargs):
        """
        Общий хук: 
        - без event → per-frame-эффект
        - с event    → реакция на событие
        """
        pass

    @property
    def is_expired(self) -> bool:
        return self.elapsed >= self.duration
