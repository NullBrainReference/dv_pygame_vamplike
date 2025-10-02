from dataclasses import dataclass
from pygame import Vector2

@dataclass
class SpawnProjectile:
    projectile: object

@dataclass
class SpawnEffect:
    effect: object

@dataclass
class GainExp:
    amount: int

@dataclass
class LevelUp:
    new_level: int

@dataclass
class ShowBonusSelector:
    options: list      # список кортежей (label: str, effect_instance)

@dataclass
class BonusSelected:
    effect: object

@dataclass
class RequestTargets:
    effect: object
    origin: Vector2
    radius: float

@dataclass
class ProvideTargets:
    effect: object
    candidates: list
    
@dataclass
class ShowEscMenu:
    pass

@dataclass
class HideEscMenu:
    pass

@dataclass
class QuitGame:
    pass

@dataclass
class Continue:
    pass