import pygame
import game_functions as gf

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
    scoreboard = Scoreboard(settings, screen, stats)

    gf.create_fleet(settings, screen, ship, aliens)

    while True:
        gf.check_events(settings, screen, ship, bullets, stats, play_button, scoreboard)
        
        if stats.game_active:
            ship.update()

            gf.update_bullets(settings, screen, ship, bullets, aliens, stats, scoreboard)
            gf.update_aliens(settings, screen, ship, bullets, aliens, stats, scoreboard)
        gf.update_screen(settings, screen, ship, bullets, aliens, stats, play_button, scoreboard)


run_game()
