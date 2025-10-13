import pygame, requests

class ScoreUI:
    def __init__(self, font):
        self.font = font
        self.leaderboard = []
        self._fetch()

    def _fetch(self):
        try:
            r = requests.get("http://127.0.0.1:8000/leaderboard?limit=10")
            if r.status_code == 200:
                self.leaderboard = r.json()
        except Exception as e:
            print("Error fetching leaderboard:", e)

    def update(self, dt):
        pass

    def handle_event(self, event):
        # Could add "press Enter to continue" here
        pass

    def draw(self, screen, camera=None):
        y = 150
        title = self.font.render("=== Leaderboard ===", True, (255,255,0))
        screen.blit(title, (200, y))
        y += 40
        for idx, entry in enumerate(self.leaderboard, start=1):
            txt = self.font.render(f"{idx}. {entry['username']} - {entry['score']}", True, (255,255,255))
            screen.blit(txt, (200, y))
            y += 30
