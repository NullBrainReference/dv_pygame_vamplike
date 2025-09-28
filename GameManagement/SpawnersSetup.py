from .SpawnController         import SpawnController
from .SummonerSpawnController import SummonerSpawnController
from Weapon.Bow import Bow
from Weapon.Weapon import Sword
from Weapon.Staff import SummoningStaff

def get_spawners():
    spawners = [
        SpawnController(
            hp               = 30,
            weapon_cls       = Bow,
            spawn_rate       = 2.0,
            name             = "Spider",
            chance           = 0.1,
            attack_rate      = 1.2,
            damage           = 6,
            speed            = 28,
            scale            = 1.6,
            target_range     = 300,
            progression_lvl  = 0.0,
        ),
        SpawnController(
            hp               = 30,
            weapon_cls       = Bow,
            spawn_rate       = 2.0,
            name             = "Spider",
            chance           = 0.2,
            attack_rate      = 1.2,
            damage           = 6,
            speed            = 28,
            scale            = 1.6,
            target_range     = 300,
            progression_lvl  = 0.9,
        ),
        SpawnController(
            hp               = 30,
            weapon_cls       = Sword,
            spawn_rate       = 1.6,
            name             = "Zombie",
            chance           = 0.8,
            attack_rate      = 1.4,
            damage           = 14,
            speed            = 48,
            scale            = 2.0,
            target_range     = 45,
            progression_lvl  = 0.0,
        ),
        SpawnController(
            hp               = 30,
            weapon_cls       = Sword,
            spawn_rate       = 1.6,
            name             = "Zombie",
            chance           = 0.5,
            attack_rate      = 1.4,
            damage           = 14,
            speed            = 52,
            scale            = 2.0,
            target_range     = 45,
            progression_lvl  = 1,
        ),
        SpawnController(
            hp               = 120,
            weapon_cls       = Sword,
            spawn_rate       = 12.5,
            name             = "Zombie",
            chance           = 0.7,
            attack_rate      = 1.4,
            damage           = 28,
            speed            = 62,
            scale            = 4.5,
            target_range     = 60,
            progression_lvl  = 0.8,
            reward           = 200
        ),
        SummonerSpawnController(
            hp               = 40,
            weapon_cls       = SummoningStaff,
            spawn_rate       = 12,
            name             = "Staffdude",
            chance           = 0.7,
            attack_rate      = 1.2,
            damage           = 0,
            speed            = 36,
            scale            = 2.0,
            target_range     = 280,
            progression_lvl  = 0.9,
            reward           = 200
        )

    ]

    return spawners
