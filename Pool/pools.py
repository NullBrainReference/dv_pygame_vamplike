from Weapon.Projectile import Projectile
from Weapon.SwordSwingEffect import SwordSwingEffect
from .ObjectPool import ObjectPool


projectile_pool = ObjectPool[Projectile]()

sword_swing_pool = ObjectPool[SwordSwingEffect]()