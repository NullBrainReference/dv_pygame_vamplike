# Weapon.py
import pygame
from Events.Events import SpawnProjectile, SpawnEffect
from Events.EventBus import bus
from GameManagement.Camera import Camera
import math

class Weapon:
    def __init__(self, range: float, rate: float, damage: float):
        self.range = range
        self.rate = rate
        self.damage = damage
        self.timer = 0.0

    def update(self, dt):
        self.timer += dt

    def can_attack(self):
        return self.timer >= self.rate

    def reset_timer(self):
        self.timer = 0.0

    def on_attack(self, origin, targets, owner=None):
        raise NotImplementedError
    
    @property
    def icon_path(self) -> str:
        return "Assets/Weapons/projectile.png"


class Projectile:
    def __init__(self, pos, direction, damage, target):
        self.pos       = pos
        self.direction = direction.normalize()
        self.speed     = 300
        self.damage    = damage
        self.alive     = True
        self.target    = target

        self.original = pygame.image.load(
            "Assets/Weapons/projectile.png"
        ).convert_alpha()

        #    math.atan2 wants (y, x) where +Y is up, so we negate direction.y
        base_angle = math.degrees(
            math.atan2(-self.direction.y, self.direction.x)
        )
        self.angle = (base_angle + 180) % 360

        self.image = pygame.transform.rotate(self.original, self.angle)
        self.rect  = self.image.get_rect()

    def update(self, dt: float):
        self.pos += self.direction * self.speed * dt

    def draw(self, screen: pygame.Surface, camera: Camera):
        screen_pos       = camera.apply(self.pos)
        self.rect.center = screen_pos
        screen.blit(self.image, self.rect)


class Bow(Weapon):
    def on_attack(self, origin, targets, owner=None):
        if not self.can_attack():
            return
        self.reset_timer()

        # targets in range
        in_range = [
            t for t in targets
            if (t.pos - origin).length_squared() <= self.range * self.range
        ]
        if not in_range:
            return

        owner.on_attack(targets)

        # Выбираем самую близкую из тех, что в пределах range
        target    = min(in_range, key=lambda t: (t.pos - origin).length_squared())
        direction = (target.pos - origin).normalize()

        projectile = Projectile(origin.copy(), direction, self.damage, target)
        bus.emit(SpawnProjectile(projectile))



class Sword(Weapon):
    def on_attack(self, origin, targets, owner=None):
        if not self.can_attack():
            return
        # self.reset_timer()

        in_range = False
        for target in targets:
            if (target.pos - origin).length() <= self.range:
                target.take_damage(self.damage)
                self.reset_timer()
                in_range = True
        if not in_range:
            return
        
        owner.on_attack(targets)
        
        e = SwordSwingEffect(origin.copy(), self.range)
        bus.emit(SpawnEffect(e))


class SwordSwingEffect:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius
        self.timer = 0.3
        self.alive = True

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.alive = False

    def draw(self, screen: pygame.Surface, camera: Camera):
        if not self.alive:
            return
        screen_pos = camera.apply(self.pos)
        alpha = int(255 * (self.timer / 0.3))
        color = (255, 255, 255, alpha)
        pygame.draw.circle(screen, color, screen_pos, int(self.radius), 2)

class Halberd(Weapon):
    def __init__(self,
                 range: float,
                 rate: float,
                 damage: float,
                 sprite_path: str,
                 spin_speed: float = 720,
                 duration: float = 0.5):
        super().__init__(range, rate, damage)
        # self.sprite      = pygame.image.load(sprite_path).convert_alpha()
        raw = pygame.image.load(sprite_path).convert_alpha()
        w, h = raw.get_size()
        self.sprite = pygame.transform.scale(
            raw,
            (int(w * 2), int(h * 2))
        )
        self.spin_speed  = spin_speed
        self.duration    = duration

    def on_attack(self, origin, targets, owner):
        if not self.can_attack():
            return
        # self.reset_timer()

        # 1) мгновенный урон всем в радиусе
        in_range = False

        for t in targets:
            if (t.pos - origin).length() <= self.range:
                t.take_damage(self.damage)
                self.reset_timer()
                in_range = True
        
        if not in_range:
            return
        
        owner.on_attack(targets)

        effect = HalberdSpinEffect(owner,
                                   self.sprite,
                                   self.spin_speed,
                                   self.duration)
        bus.emit(SpawnEffect(effect))

    @property
    def icon_path(self) -> str:
        return "Assets/Weapons/halberd.png"


class HalberdSpinEffect:
    def __init__(self, owner, sprite: pygame.Surface,
                 spin_speed: float, duration: float):
        self.owner      = owner
        self.sprite     = sprite
        self.spin_speed = spin_speed
        self.duration   = duration
        self.timer      = 0.0
        self.angle      = 0.0
        self.alive      = True

        # вычисляем pivot-внутри-спрайта: центр по X, 3/4 вниз по Y
        w, h = sprite.get_size()
        self.pivot = (w//2, int(0.75*h))

        # заранее определяем размер контейнера —
        # достаточно квадрат, который вмещает любой поворот:
        side = max(w, h) * 2
        self.container_size = (side, side)

    def update(self, dt: float):
        self.timer += dt
        if self.timer >= self.duration:
            self.alive = False
            return
        self.angle = (self.angle + self.spin_speed * dt) % 360

    def draw(self, screen: pygame.Surface, camera):
        if not self.alive:
            return

        # 1) куда на экране ставим нашу pivot-точку (центр игрока)
        screen_pos = camera.apply(self.owner.pos)

        # 2) создаём чистый контейнер с альфой
        container = pygame.Surface(self.container_size, pygame.SRCALPHA)

        # 3) вычисляем где внутри контейнера рисовать спрайт,
        #    чтобы его pivot лег в центр контейнера
        cx, cy = self.container_size[0]//2, self.container_size[1]//2
        px, py = self.pivot
        blit_x = cx - px
        blit_y = cy - py

        # 4) заливаем контейнер спрайтом
        container.blit(self.sprite, (blit_x, blit_y))

        # 5) поворачиваем контейнер вокруг его же центра
        rotated = pygame.transform.rotate(container, self.angle)

        # 6) рисуем так, чтобы центр контейнера совпал с screen_pos
        rect = rotated.get_rect(center=screen_pos)
        screen.blit(rotated, rect)