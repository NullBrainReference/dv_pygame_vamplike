from Unit.Unit import Unit
import pygame

from collections import defaultdict
import math

# Подберите под свой максимальный радиус
MAX_RADIUS = 8*2
CELL_SIZE  = MAX_RADIUS * 2  

# Ячейки хранятся в словаре: (ix,iy) -> [Unit, …]
grid: dict[tuple[int,int], list[Unit]] = defaultdict(list)

def build_grid(units: list[Unit]) -> dict[tuple[int,int], list[Unit]]:
    grid.clear()
    for u in units:
        ix = math.floor(u.pos.x / CELL_SIZE)
        iy = math.floor(u.pos.y / CELL_SIZE)
        grid[(ix, iy)].append(u)
    return grid

def collide_via_grid(units: list[Unit]):
    # 1) Строим grid
    build_grid(units)

    # 2) Перебираем каждый юнит и соседние ячейки
    for u in units:
        ix = math.floor(u.pos.x / CELL_SIZE)
        iy = math.floor(u.pos.y / CELL_SIZE)

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                cell = grid.get((ix + dx, iy + dy))
                if not cell:
                    continue
                for v in cell:
                    # пропускаем себя и уже обработанные пары
                    if v is u or id(v) <= id(u):
                        continue

                    if not u.collider.intersects(v.collider):
                        continue

                    # narrow-phase + разрешение
                    separate_circles(u, v)
                    resolve_impulse(u, v)


def physics_step(units: list[Unit], dt: float):
    # 1) Интеграция позиций
    for u in units:
        total_v = u.desired_velocity + u.impulse_velocity
        u._pos  += total_v * dt

    # 2) Broad-phase: grid + локальные пары
    collide_via_grid(units)

    # 3) Демпфинг импульсной составляющей
    for u in units:
        u.impulse_velocity *= 0.9



# def physics_step(units: list[Unit], dt: float):
    
#     for u in units:
#         total_v = u.desired_velocity + u.impulse_velocity
#         u._pos  += total_v * dt

#     n = len(units)
#     for i in range(n):
#         for j in range(i+1, n):
#             a, b = units[i], units[j]
#             if not a.collider.intersects(b.collider):
#                 continue
#             separate_circles(a, b)
#             resolve_impulse(a, b)

#     for u in units:
#         u.impulse_velocity *= 0.9


def separate_circles(u1: Unit, u2: Unit):
    c1, c2 = u1.collider, u2.collider
    
    delta = c2.center - c1.center
    dist  = delta.length()
    if dist == 0:
        return
    overlap = c1.radius + c2.radius - dist
    if overlap > 0:
        
        push = delta.normalize() * (overlap + 1e-3)
        total_mass = u1.mass + u2.mass
        
        u1._pos -= push * (u2.mass / total_mass)
        u2._pos += push * (u1.mass / total_mass)


def resolve_impulse(u1: Unit, u2: Unit):
    n = u2.pos - u1.pos
    dist = n.length()
    if dist == 0:
        return
    n /= dist

    rel_vel = (u1.impulse_velocity - u2.impulse_velocity).dot(n)
    if rel_vel > 0:
        return
    e = 0.5  
    j = -(1 + e) * rel_vel / (1/u1.mass + 1/u2.mass)
    impulse = j * n
    u1.impulse_velocity += impulse / u1.mass
    u2.impulse_velocity -= impulse / u2.mass
