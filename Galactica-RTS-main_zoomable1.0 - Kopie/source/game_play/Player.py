import time

import source.utils.Globals
from source import utils


class Player:
    """
    this holds the players values like population, production, population_limit
    """
    def __init__(self, **kwargs):
        self.city = 0
        self.technology = 0
        self.water = 0
        self.minerals = 0
        self.food = 0
        self.energy = 0
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.clock_ = 2367
        self.start_wait = kwargs.get("wait", 5.0)
        self.wait = kwargs.get("wait", 5.0)
        self.start_time = time.time()
        self.game_start_time = time.time()

        self.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "technology": 0,
            "city": 0
            }

        self.stock = None
        self.get_stock()
        self.population = 0
        self.population_limit = 0

    def get_stock(self):
        self.stock = {"energy": self.energy,
                      "food": self.food,
                      "minerals": self.minerals,
                      "water": self.water,
                      "technology": self.technology,
                      "city": self.city
                      }
        return self.stock

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
        self.clock_ += 0.01 * source.utils.Globals.time_factor * source.utils.Globals.game_speed
        self.clock = "Year: " + str(int(self.clock_))
        self.wait = self.start_wait / utils.Globals.time_factor / source.utils.Globals.game_speed
        self.produce()
