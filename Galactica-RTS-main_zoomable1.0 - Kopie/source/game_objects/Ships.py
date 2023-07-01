from source.game_objects.Ship import Ship
from source.utils import sounds


class Spaceship(Ship):
    def __init__(self, win, x, y, width, height, isSubWidget=False, *args, **kwargs):
        Ship.__init__(self, win, x, y, width, height, isSubWidget=False, *args, **kwargs)
        self.hum = sounds.hum1
        self.sound_channel = 1

        # setup Game variables
        self.speed = 0.1
        self.energy_max = 10000
        self.energy = 10000
        self.energy_use = 0.0005
        self.energy_reload_rate = 0.1
        # self.move_stop = 0
        self.energy_warning_level = 500
        self.noenergy_image_x = 0
        self.noenergy_image_y = -self.getHeight()
        self.rank_image_x = 0
        self.rank_image_y = -self.getHeight() / 1.5

        self.food_max = 500
        self.minerals_max = 200
        self.technology_max = 500
        self.minerals_max = 300
        self.water_max = 400
        self.crew = 7
        self.crew_members = ["john the cook", "jim the board engineer", "stella the nurse", "sam the souvenir dealer",
                             "jean-jaques the artist", "Nguyen thon ma, the captain", "dr. Hoffmann the chemist"]

        # fog of war
        self.fog_of_war_radius = 100

        # tooltip
        self.set_tooltip()


class Cargoloader(Ship):
    def __init__(self, win, x, y, width, height, isSubWidget=False, *args, **kwargs):
        Ship.__init__(self, win, x, y, width, height, isSubWidget=False, *args, **kwargs)
        self.hum = sounds.hum2
        self.sound_channel = 2

        # setup Game variables
        self.speed = 0.02
        self.energy_max = 20000
        self.energy = 15000
        self.energy_use = 0.001
        self.energy_reload_rate = 0.05
        # self.move_stop = 0
        self.energy_warning_level = 500
        self.noenergy_image_x = 0
        self.noenergy_image_y = -self.getHeight() / 2
        self.rank_image_x = 0
        self.rank_image_y = -self.getHeight() / 2.4

        self.food_max = 1500
        self.minerals_max = 2000
        self.technology_max = 1500
        self.minerals_max = 1000
        self.water_max = 1000

        self.crew = 7
        self.crew_members = ["john the cook", "jim the board engineer", "stella the nurse", "sam the souvenir dealer",
                             "jean-jaques the artist", "Nguyen thon ma, the captain", "dr. Hoffmann the chemist"]

        # fog of war
        self.fog_of_war_radius = 50

        # tooltip
        self.set_tooltip()


class Spacehunter(Ship):
    def __init__(self, win, x, y, width, height, isSubWidget=False, *args, **kwargs):
        Ship.__init__(self, win, x, y, width, height, isSubWidget=False, *args, **kwargs)
        self.hum = sounds.hum3
        self.sound_channel = 3
        # setup Game variables
        self.speed = 0.2
        self.energy_max = 5000
        self.energy = 5000
        self.energy_use = 0.0015
        self.energy_reload_rate = 0.15
        self.energy_warning_level = 500
        self.noenergy_image_x = 0
        self.noenergy_image_y = -self.getHeight()
        self.rank_image_x = 0
        self.rank_image_y = -self.getHeight() / 1.5

        self.food_max = 200
        self.minerals_max = 200
        self.technology_max = 150
        self.minerals_max = 100
        self.water_max = 100

        self.crew = 7
        self.crew_members = ["john the cook", "jim the board engineer", "stella the nurse", "sam the souvenir dealer",
                             "jean-jaques the artist", "Nguyen thon ma, the captain", "dr. Hoffmann the chemist"]

        # fog of war
        self.fog_of_war_radius = 30

        # tooltip
        self.set_tooltip()
