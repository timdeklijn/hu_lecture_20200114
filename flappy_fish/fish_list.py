import keras
import gc
import os
import pygame
import numpy as np
import copy

from fish import Fish
from nn import NN
import config

class FishList(NN):

    def __init__(self):
        self.fish_image = pygame.image.load(os.path.join("flappy_fish", "images", "fish.png"))
        self.alive = [Fish(image=self.fish_image) for _ in range(config.FISH_NR)]
        self.dead = []
        self.max_score = 0

    def update(self, pipe_info):
        for b in self.alive:
            b.update(pipe_info)

    def draw(self, screen):
        for b in self.alive:
            b.draw(screen)

    def check_alive(self, pipe_list):
        for i in range(len(self.alive)-1, -1, -1):
            b = self.alive[i]
            if pipe_list.check_collision(b) or b.check_off_screen():
                self.dead.append(self.alive[i])
                self.alive.pop(i)
