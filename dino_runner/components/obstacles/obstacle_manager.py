import pygame
import random
from dino_runner.components.obstacles.bird import Bird

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import BIRD, SHIELD_TYPE

class ObstacleManager:
    def __init__(self):
        self.obstacles = [] 
    
    def update(self, game):
        if len(self.obstacles) == 0:
            random_obstacle = random.randint(0,2)
            if random_obstacle == 0:
                cactus_type = "SMALL"  
                self.obstacles.append(Cactus(cactus_type))   
            elif random_obstacle == 1:
                cactus_type = "LARGE"
                self.obstacles.append(Cactus(cactus_type))
            else:
                self.obstacles.append(Bird(BIRD))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.type != SHIELD_TYPE:
                    pygame.time.delay(500)
                    #game.playing = False
                    game.death_count += 1
                    game.lives -= 1
                    self.obstacles.remove(obstacle)
                    break
                else:
                    self.obstacles.remove(obstacle)
        

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []