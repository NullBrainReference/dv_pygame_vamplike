from Unit.Unit import Unit
import pygame

def physics_step(units: list[Unit], dt: float):
    # 1) Интеграция позиций по итоговой скорости
    for u in units:
        total_v = u.desired_velocity + u.impulse_velocity
        u._pos  += total_v * dt

    # 2) Статическое разделение — удаляем проникновения
    n = len(units)
    for i in range(n):
        for j in range(i+1, n):
            separate_circles(units[i], units[j])

    # 3) Применяем импульсные столкновения, чтобы дать отскок
    for i in range(n):
        for j in range(i+1, n):
            a, b = units[i], units[j]
            if a.collider.intersects(b.collider):
                resolve_impulse(a, b)

    # 4) Демпфинг только на импульсную составляющую
    for u in units:
        u.impulse_velocity *= 0.9


def separate_circles(u1: Unit, u2: Unit):
    c1, c2 = u1.collider, u2.collider
    # вектор от центра u1 к u2
    delta = c2.center - c1.center
    dist  = delta.length()
    if dist == 0:
        return
    overlap = c1.radius + c2.radius - dist
    if overlap > 0:
        # небольшой ε, чтобы не залипало
        push = delta.normalize() * (overlap + 1e-3)
        total_mass = u1.mass + u2.mass
        # сдвигаем обратно по массе
        u1._pos -= push * (u2.mass / total_mass)
        u2._pos += push * (u1.mass / total_mass)


def resolve_impulse(u1: Unit, u2: Unit):
    n = u2.pos - u1.pos
    dist = n.length()
    if dist == 0:
        return
    n /= dist
    # относительная импульсная скорость вдоль нормали
    rel_vel = (u1.impulse_velocity - u2.impulse_velocity).dot(n)
    if rel_vel > 0:
        return
    e = 0.5  # коэффициент упругости [0..1]
    j = -(1 + e) * rel_vel / (1/u1.mass + 1/u2.mass)
    impulse = j * n
    u1.impulse_velocity += impulse / u1.mass
    u2.impulse_velocity -= impulse / u2.mass
