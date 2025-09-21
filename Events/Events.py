from dataclasses import dataclass

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