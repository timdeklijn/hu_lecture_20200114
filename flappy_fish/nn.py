import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam

import config

class NN():

    def __init__(self):
        pass


    def create_NN(self):
        """Create neural network

        Create and compile a model and save it in:
        self.model
        """
        self.model = Sequential()
        self.model.add(Dense(8, input_dim=5, activation="relu"))
        self.model.add(Dense(32, input_dim=8, activation="relu"))
        self.model.add(Dense(1, input_dim=32, activation="softplus"))
        self.model.compile(loss="categorical_crossentropy",
                           optimizer=Adam(),
                           metrics=["accuracy"])


    def mutate(self, weights_list):
        """
        Mutate weights.

        Returns a weight list.
        """
        chance = 0.005
        mutate_range = 0.025
        new_weights_list = []
        for weights in weights_list:
            new_weights = []
            for w in weights:
                rand_weights = (np.random.random(size=w.shape) - 0.5) * mutate_range
                w = np.where(np.random.random(size=w.shape) < chance, w, w + rand_weights)
                new_weights.append(w)
            new_weights_list.append(new_weights)
        return new_weights_list


    def change_weights(self, weights):
        """Replace weights in self.model with weights"""
        for i, layer in enumerate(self.model.layers):
            layer.set_weights(weights[i])

    def determine_pairs(self):
        score_list = [f.score for f in self.dead]
        tot = sum(score_list)
        prob_list = [float(i) / tot for i in score_list]
        f_list = [i for i in range(config.FISH_NR)]
        pair_list = []
        for _ in range(config.FISH_NR):
            a = np.random.choice(f_list, p=prob_list)
            b = np.random.choice(f_list, p=prob_list)
            pair_list.append([a,b])
        return pair_list

    def reproduce(self, pair):
        w_a = [np.array(l.get_weights()) for l in self.dead[pair[0]].model.layers]
        w_b = [np.array(l.get_weights()) for l in self.dead[pair[1]].model.layers]
        for l in range(len(w_a)):
            for w in range(len(w_a[l])):
                chance = random.uniform(0,1)
                if chance < 0.5:
                    w_a[l][w] = w_b[l][w]
        return w_a



    def next_generation(self):
        """
        Create the next generation by:
            * finding the fittest fish in self.dead (list of fish)
            * Extract the weights of the fish that need to reproduce
            * Mix/Mutate the weights and set weights to next generation
            * For all fish, run fish_reset()
            * Append all changed fish to self.alive (list of fish)
            * empty self.dead (list of fish)
        """

        # Sort fish on score
        self.dead.sort(key=lambda b: b.score, reverse=True)
        self.max_score = self.dead[0].score
        population_weights = []
        for f, pair in enumerate(self.determine_pairs()):
            new_weights = self.reproduce(pair)
            population_weights.append(self.mutate(new_weights))
        for i, f in enumerate(self.dead):
            f.change_weights(population_weights[i])
            f.reset_fish()
            self.alive.append(f)
        self.dead = []

