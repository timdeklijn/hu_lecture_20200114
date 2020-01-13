import random
import pygame

import config


class Pipe():
    def __init__(self):
        self.x = config.WIDTH
        self.y = random.randint(config.HALF_GAP_SIZE + config.PIPE_MARGIN,
                                config.HEIGHT - config.PIPE_MARGIN - config.HALF_GAP_SIZE)
        self.y_bottom = self.y + config.HALF_GAP_SIZE
        self.y_top = self.y - config.HALF_GAP_SIZE

    def update(self):
        self.x -= config.PIPE_SPEED

    def draw(self, screen):

        # Get Rect boundaries for top and bottom pipes
        r1 = pygame.Rect(self.x, 0,
            config.PIPE_WIDTH, self.y_top)
        r2 = pygame.Rect(self.x, self.y_bottom,
                         config.PIPE_WIDTH, config.HEIGHT - self.y_top)
        # Draw pipes
        pygame.draw.rect(screen, (100, 200, 100), r1)
        pygame.draw.rect(screen, (100, 200, 100), r2)
