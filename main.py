import pygame
import requests
from GameManagement.GameManager import GameManager
from Animation.AnimationSetup import setup_animations

pygame.init()
screen = pygame.display.set_mode((800, 600))

setup_animations()

game = GameManager(screen)
game.run()

def print_leaderboard():
    try:
        response = requests.get("http://127.0.0.1:8000/leaderboard?limit=10")
        if response.status_code == 200:
            leaderboard = response.json()
            print("=== Leaderboard ===")
            for idx, entry in enumerate(leaderboard, start=1):
                print(f"{idx}. {entry['username']} - {entry['score']}")
        else:
            print("Error fetching leaderboard:", response.text)
    except Exception as e:
        print("Failed to connect to API:", e)

print_leaderboard()