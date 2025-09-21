from Animation.AnimationFrames import AnimationFrames
import pygame
import os

class AnimationLibrary:
    def __init__(self):
        self._library: dict[str, AnimationFrames] = {}

    def load_animation(self,
                       key: str,
                       file_path: str,
                       frame_size: tuple[int,int] = (16, 16),
                       frame_rate: float = 10):
        sheet = pygame.image.load(file_path).convert_alpha()
        frames = self._slice_sheet(sheet, frame_size)
        self._library[key] = AnimationFrames(frames, frame_rate)

    def load_unit_animations(self,
                             unit_name: str,
                             dir_path: str,
                             frame_size: tuple[int,int] = (16, 16),
                             frame_rate: float = 10):

        for fname in os.listdir(dir_path):
            if not fname.lower().endswith(".png"):
                continue
            anim_name = os.path.splitext(fname)[0]
            key = f"{unit_name}.{anim_name}"
            full_path = os.path.join(dir_path, fname)
            self.load_animation(key, full_path, frame_size, frame_rate)

    def get(self, key: str) -> AnimationFrames | None:
        return self._library.get(key)

    def _slice_sheet(self, sheet: pygame.Surface, frame_size: tuple[int,int]):
        fw, fh = frame_size
        w, h = sheet.get_size()
        frames: list[pygame.Surface] = []
        for y in range(0, h, fh):
            for x in range(0, w, fw):
                rect = pygame.Rect(x, y, fw, fh)
                
                frame = sheet.subsurface(rect).copy()
                frames.append(frame)
        return frames

# Глобальный экземпляр, чтобы один раз загрузить всё
ANIMATION_LIBRARY = AnimationLibrary()
