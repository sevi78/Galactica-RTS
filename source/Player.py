# import pygame.examples.aacircle
#
# pygame.examples.aacircle.main()
import time

import source.Globals


class Player:
    """
    this holds the players values like population, production, population_limit
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.clock_ = 2367
        self.start_wait = kwargs.get("wait", 5.0)
        self.wait = kwargs.get("wait", 5.0)
        self.start_time = time.time()

        self.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "technology": 0,
            "city": 0
            }

        self.population = 0
        self.population_limit = 0

    def set_population_limit(self):
        population_buildings = ["town", "city", "metropole"]
        population_buildings_values = {"town": 1000, "city": 10000, "metropole": 100000}

        self.population_limit = sum([population_buildings_values[i] for i in self.buildings if
                                     i in population_buildings])

    def produce(self):
        if time.time() > self.start_time + self.wait:
            self.start_time = time.time()

            self.energy += self.production["energy"]
            self.food += self.production["food"]
            self.minerals += self.production["minerals"]
            self.water += self.production["water"]
            self.technology += self.production["technology"]
            self.city += self.production["city"]

    def update(self):

        self.clock_ += 0.01 * source.Globals.time_factor
        self.clock = "Year: " + str(int(self.clock_))
        self.wait = self.start_wait / source.Globals.time_factor
        self.produce()
