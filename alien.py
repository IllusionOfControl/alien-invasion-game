import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, settings, screen):
        super().__init__()

        self.screen = screen

        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.x = self.rect.height
        self.rect.y = self.rect.width

        self.settings = settings

        self.x = float(self.rect.x)

    def update(self):
        self.x += (self.settings.alien_speed_factor * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True