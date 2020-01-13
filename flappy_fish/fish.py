import pygame
import gc
import numpy as np
from keras.models import Sequential, clone_model
from keras.layers import Dense, Activation
from keras.optimizers import Adam

import config
from nn import NN

class Fish(NN):
    """
    Fish class, predict action, update position and
    draw the bird.
    """

    def __init__(self, image):
        """
        :param color: rgb bird color
        """
        super().__init__()
        self.image = image
        self.x = 2 * config.CIRCLE_RADIUS
        self.y = int(config.HEIGHT/2.0)
        self.radius = config.CIRCLE_RADIUS
        self.gravity_force = config.GRAVITY / config.BIRD_MASS
        self.velocity = 0
        self.acceleration = 0
        self.score = 0
        self.create_NN()


    def reset_fish(self):
        """Reset Fish to start posistion"""
        self.y = int(config.HEIGHT/2.0)
        self.velocity = 0
        self.score = 0


    def draw(self, screen):
        """
        Draw the Fish object to the screen

        :param screen: pygame screen object
        """
        r = pygame.Rect(self.x-self.radius,
                        self.y-self.radius,
                        2*self.radius,
                        2*self.radius)
        screen.blit(self.image, r)


    def check_off_screen(self):
        """
        Check if Fish position is off screen

        :retrun: boolean, True when off screen
        """
        if self.y - self.radius <= 0 or self.y + self.radius >= config.HEIGHT:
            return True


    def update(self, pipe_info):
        """
        predict (using the Fish neural network) an action based on environment
        input, then update acceleration, velocity and finally, bird position.

        :param pipe_info: tuple with environment variables
        """
        # Create NN input
        # x, y, y
        nn_input = np.array([[self.velocity] + [self.y] + [i for i in pipe_info]], dtype=np.float32)
        nn_input[0,2] = self.x - nn_input[0,2]
        nn_input[0,3] = self.y - nn_input[0,3]
        nn_input[0,4] = self.y - nn_input[0,4]
        # Based on NN output, jump or not
        # can only jump when fish is falling
        if self.model.predict(nn_input)[0,0] > 0.5 and self.velocity >= 0.0:
            self.acceleration += config.JUMP_FORCE
        else:
            self.acceleration += self.gravity_force
        # update position
        self.velocity += self.acceleration
        self.y += int(self.velocity)
        self.acceleration = 0
        self.score += 1
