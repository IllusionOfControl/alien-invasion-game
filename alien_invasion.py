import pygame
from game_functions import GameFunctions
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from pygame.sprite import Group


def run_game():
    pygame.init()

    settings = Settings()

    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    ship = Ship(screen, settings)
    bullets = Group()
    aliens = Group()
    stats = GameStats(settings)
    play_button = Button(settings, screen, "Play")
    scoreboard = Scoreboard(screen, settings, stats)

    gf = GameFunctions(settings, screen, ship, bullets, aliens, stats, play_button, scoreboard)

    while True:
        gf.check_events()

        if stats.game_active:
            ship.update()

            gf.update_bullets()
            gf.update_aliens()
        gf.update_screen()


run_game()
