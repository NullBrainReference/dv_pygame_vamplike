import pygame

class NameInput:
    def __init__(self, font, score, on_submit):
        self.font = font
        self.score = score
        self.username = ""
        self.alive = True
        self.on_submit = on_submit  # callback to trigger ScoreUI

        self.input_rect = pygame.Rect(200, 200, 240, 40)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active   = pygame.Color('dodgerblue2')
        self.color = self.color_active
        self.focused = True

    def update(self, dt):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.username.strip():
                # Call back to GameManager (or whoever owns this UI)
                self.on_submit(self.username, self.score)
                self.alive = False
            elif event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]
            else:
                self.username += event.unicode

    def draw(self, screen, camera=None):
        pygame.draw.rect(screen, self.color, self.input_rect, 2)
        txt_surface = self.font.render(self.username, True, (255,255,255))
        screen.blit(txt_surface, (self.input_rect.x+5, self.input_rect.y+5))
        prompt = self.font.render("Enter your name:", True, (255,255,0))
        screen.blit(prompt, (self.input_rect.x, self.input_rect.y-30))
