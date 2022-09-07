import random

from dino_runner.components.obstacles.obstacle import Obstacle

class Cactus(Obstacle):
    def __init__(self, image, image2):
        self.type = random.randint(0, 5)
        super().__init__(image, image2, self.type)
        self.rect.y = 325
