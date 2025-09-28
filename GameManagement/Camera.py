
import pygame

class Camera:
    def __init__(self, screen_size, smoothing=5.0):
        self.screen_w, self.screen_h = screen_size
        # фактический центр камеры в мировых координатах
        self.cam_pos = pygame.Vector2(0, 0)
        # коэффициент сглаживания: больше — жёстче, меньше — мягче
        self.smoothing = smoothing
        self.offset = pygame.Vector2(0, 0)

    def update(self, target_pos: pygame.Vector2, dt: float):
        # 1) Вычисляем разницу к игроку
        delta = target_pos - self.cam_pos
        # 2) Прибавляем к cam_pos кусочек дельты
        #    dt делает сглаживание независимым от FPS
        self.cam_pos += delta * min(self.smoothing * dt, 1.0)

        # 3) Считаем смещение, чтобы cam_pos оказался в центре экрана
        self.offset = pygame.Vector2(
            self.screen_w  / 2 - self.cam_pos.x,
            self.screen_h / 2 - self.cam_pos.y,
        )

    def apply(self, world_pos: pygame.Vector2) -> pygame.Vector2:
        return pygame.Vector2(
            world_pos.x + self.offset.x,
            world_pos.y + self.offset.y,
        )
