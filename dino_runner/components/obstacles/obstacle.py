from msilib.schema import Class
import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import SCREEN_WIDTH


class Obstacle(Sprite):
    def __init__(self, image, image2, obstacle_type):
        self.image = image + image2
        self.obstacle_type = obstacle_type
        self.rect = self.image[self.obstacle_type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

        if self.obstacle_type in [3,4,5]:
            self.rect.y = 300
        else:
            self.rect.y = 320


    def draw(self, screen):
        screen.blit(self.image[self.obstacle_type],(self.rect.x, self.rect.y))