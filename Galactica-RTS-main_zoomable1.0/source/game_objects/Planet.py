import time
import pygame
from pygame import Vector2
from pygame_widgets.mouse import Mouse, MouseState

import source.utils.Globals
import source.utils.config
import source.game_objects
from source.game_objects.planet_buttons import PlanetButtons, PlanetConfig
from source.gui.Button import Button, ButtonArray, ImageButton
from source.utils import limit_positions, get_distance, colors, images
from source.utils.Globals import pictures_path
from source.utils.config import production
from source.utils.saveload import *
from source.utils.sounds import sounds





class Planet(Button, PlanetButtons):
    """ this is the planet class, inherited from:
    from pygame_widgets.button import Button
    """

    def __init__(self, win, x, y, width, height, isSubWidget, **kwargs):
        # inherit the base class
        Button.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        PlanetButtons.__init__(self)

        # setup variables
        self.fog_of_war_radius = self.getWidth() * 1.5
        self.layer = kwargs.get("layer", 1)
        self.name = kwargs.get("name")
        self.parent = kwargs.get("parent")
        self.image_raw = kwargs.get("image")
        self.image = kwargs.get("image")
        self.image_name_small = None
        self.image_name_big = None
        self.imageRect = self.image.get_rect()


        self.property = "planet"
        self.moveable = kwargs.get("moveable", False)

        self.orbit_object = kwargs.get("orbit_object", None)
        self.orbit_circle = None
        self.zoomable = True

        self.win = win
        self.database_path = "levels" + os.sep + "level1" + os.sep + "planets" + os.sep + self.name + ".json"
        self.x = load_file(self.database_path)["x"]#source.config.planet_positions[self.name][0]  # x
        self.y = load_file(self.database_path)["y"]#source.config.planet_positions[self.name][1]  # y
        self.orbit_speed = load_file(self.database_path)["orbit_speed"]

        self.size_x = width
        self.size_y = height
        self.start_time = time.time()
        self.wait = kwargs.get("wait", 1.0)

        self.pos = Vector2(self.getX(), self.getY())
        self.selected = False
        self.center = (self.getX() + self.getWidth() / 2, self.getY() + self.getHeight() / 2)

        self.inactiveColour = kwargs.get("inactiveColour", (0, 0, 0))
        self.hoverColour = kwargs.get("hoverColour", (150, 0, 0))
        self.pressedColour = kwargs.get("pressedColour", (0, 200, 20))
        self.radius = 5
        self.onClick = lambda: self.execute(kwargs)
        self.text.set_alpha(0)
        self.button_build_menu_open = None
        self.on_hover = False
        self.on_hover_release = False

        # setup Game variables
        self.info_text = kwargs.get("info_text")
        self.resources = {"energy": 0, "food": 0, "minerals": 0, "water": 0}
        self.explored = False
        self.just_explored = False
        self.buildings = []
        self.buildings_max = 10
        self.population = 0.0
        self.population_limit = 0.0
        self.population_grow = 0.0
        self.alien_population = 0

        self.building_slot_amount = 3
        self.building_slot_upgrades = 0
        self.building_slot_upgrade_prices = {0:500, 1:750, 2:1250, 3:2500, 4:5000, 5:25000, 6:100000}
        self.building_slot_upgrade_energy_consumption = {0: 0, 1: 2, 2: 3, 3: 5, 4: 10, 5: 15, 6: 25 }
        self.building_slot_max_amount = self.building_slot_amount + len(self.building_slot_upgrade_prices)

        self.building_cue = 0
        self.planet_button_array = None
        self.specials = []
        self.type = ""
        self.possible_resources = kwargs.get("possible_resources")

        self.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "city": 0,
            "technology": 0
            }

        self.production_water = self.production["water"]
        self.production_energy = self.production["energy"]
        self.production_food = self.production["food"]
        self.production_minerals = self.production["minerals"]
        self.production_city = self.production["city"]
        self.production_technology = self.production["technology"]

        # population buildings
        self.population_buildings = ["town", "city", "metropole"]
        self.population_buildings_values = {"town": 1000, "city": 10000, "metropole": 100000}

        # create building slots
        self.building_buttons_energy = []
        self.building_buttons_water = []
        self.building_buttons_food = []
        self.building_buttons_minerals = []

        self.building_buttons = {"energy": self.building_buttons_energy,
                                 "food": self.building_buttons_food,
                                 "minerals": self.building_buttons_minerals,
                                 "water": self.building_buttons_water
                                 }
        self.building_buttons_list = self.building_buttons_energy + self.building_buttons_food + \
                                     self.building_buttons_minerals + self.building_buttons_water

        self.create_planet_button_array()

        # register the button
        self.parent.game_objects.append(self)
        self.parent.planets.append(self)


        self.planet_config = PlanetConfig(**kwargs)

        self.setup()

    def setup(self):
        for key, value in load_file(self.database_path).items():
            if key in self.__dict__:
                # lists
                if "[" in str(value):
                    value = eval(value)
                setattr(self, key, value)

    def draw_orbit(self):
        if self.orbit_object:
            #if self.orbit_circle:
            if source.utils.Globals.show_orbit:
                pos = self.orbit_object.getX() + self.orbit_object.getWidth()/2,self.orbit_object.getY() + self.orbit_object.getHeight()/2
                pygame.draw.circle(source.utils.Globals.win, colors.frame_color, pos, self.orbit_distance * self.parent.pan_zoom_handler.zoom, 1, )
                    #self.orbit_circle.update()

    def set_population_limit(self):
        """
        sets the population limit for the planet, based on city buildongs:
        "town":1000,  "city":10000, "metropole":100000
        """
        self.population_limit = sum([self.population_buildings_values[i] for i in self.buildings if
                                     i in self.population_buildings])

    def update_game_variables(self):
        """
        updates the population
        :return:
        """
        # timed execute: wait = seconds
        self.calculate_production()
        self.parent.calculate_global_production()

        if time.time() > self.start_time + self.wait:
            self.start_time = time.time()
            if self.population_limit > self.population:
                self.population += self.population_grow

    def calculate_production(self):
        """
        calculates the production, sets the overview icons (smiley, thumpsup) for display the condition of the planet
        """
        self.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "technology": 0,
            "city": 0
            }

        for i in self.buildings:
            for key, value in production[i].items():
                self.production[key] += value

        self.production["energy"] -= self.parent.get_sum_up_to_n(self.building_slot_upgrade_energy_consumption, self.building_slot_upgrades+1)
        self.production_water = self.production["water"]
        self.production_energy = self.production["energy"]
        self.production_food = self.production["food"]
        self.production_minerals = self.production["minerals"]
        self.production_technology = self.production["technology"]
        self.production_city = self.production["city"]

        self.calculate_population()

        # is everything in plus, show thumpsup green,otherwise red, set smiley to sad if no food production
        vl = []
        for key, value in self.production.items():
            if value < 0:
                vl.append(value)
        if len(vl) > 0:
            self.thumpsup_button.setImage(pygame.transform.flip(pygame.transform.scale(
                images[pictures_path]["icons"][
                    "thumps_upred.png"], self.thumpsup_button_size), True, True))
        else:
            self.thumpsup_button.setImage(pygame.transform.flip(pygame.transform.scale(
                images[pictures_path]["icons"][
                    "thumps_up.png"], self.thumpsup_button_size), True, False))

        if self.production["food"] > 0:
            self.smiley_button.setImage(images[pictures_path]["icons"]["smile.png"])
        else:
            self.smiley_button.setImage(images[pictures_path]["icons"]["sad.png"])

    def calculate_population(self):
        """ calculates population"""
        if self.production["food"] > 0:
            self.population_grow = source.utils.config.population_grow_factor * self.production["food"]

    def set_info_text(self):
        """
        sets the text used for the info_panel
        """
        if self.parent.build_menu_visible: return
        self.parent.info_panel.visible = True

        if self.explored:
            text = self.info_text
            self.parent.info_panel.set_planet_image(self.image)
        else:
            text = "unknown planet" + ":\n\n"
            text += "resources: ???\n"
            text += "energy: ???\n"

        self.parent.info_panel.set_text(text)
        self.parent.info_panel.set_planet_image(self.image)

    def execute(self, kwargs):
        """ this executes the code when clicked on the button """
        if self.parent.build_menu_visible: return
        self.set_info_text()
        self.parent.set_selected_planet(self)

    def on_hover_release_callback(self, x, y):
        """
        :param x:
        :param y:
        :return: True if hover is left, False if on Hover
        """
        if self.contains(x, y):
            self.on_hover = True
            self.on_hover_release = False
        else:
            self.on_hover_release = True

        if self.on_hover and self.on_hover_release:
            self.on_hover = False
            return True

        return False

    def reset_tooltip(self):
        """
        resets the tooltip on_hover_release_callback
        """
        if not self._hidden:
            x, y = Mouse.getMousePos()
            if self.on_hover_release_callback(x, y):
                source.utils.Globals.tooltip_text = ""

    def listen(self, events):
        """ Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        self.reset_tooltip()
        self.move(events)
        self.set_screen_position()

        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):  # checks if mouse over ??
                if mouseState == MouseState.RIGHT_CLICK:
                    self.parent.set_selected_planet(self)

                if mouseState == MouseState.RELEASE and self.clicked:
                    self.clicked = False
                    self.onRelease(*self.onReleaseParams)

                elif mouseState == MouseState.CLICK:
                    self.clicked = True
                    self.onClick(*self.onClickParams)
                    self.parent.set_selected_planet(self)

                elif mouseState == MouseState.DRAG and self.clicked:
                    pass

                elif mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                    self.show_hover_image()

                    if self.tooltip != "":
                        source.utils.Globals.tooltip_text = self.tooltip
            else:
                self.clicked = False

    def show_hover_image(self):
        panzoom = self.parent.pan_zoom_handler
        pygame.draw.circle(self.win,colors.frame_color, self.center, self.getWidth()/2/panzoom.zoom, int(6*panzoom.zoom))

    def move(self, events):
        """
        calls the move function from the Button Class
        :param events:
        """
        super().move(events, self)

    def update(self):
        """
        updates the planet...a lot of stuff, have look on the code, its self explaining
        """
        self.set_screen_position()
        if self.name == "Sun":
            self.disable()
            if not self.explored:
                self.parent.fog_of_war.draw_fog_of_war(self)
                self.explored = True

            # hide if some ui is blocking it
            if self.parent.event_panel._hidden:
                if not self.parent.build_menu_visible:
                    self.show()
            return

        # update orbit angle
        if source.utils.Globals.enable_zoom:
            self.enable_orbit = False
        else:
            self.enable_orbit = True


        if source.utils.Globals.enable_orbit:
            self.enable_orbit = True
        else:
            self.enable_orbit = False

        if self.type == "sun":
            self.enable_orbit = False


        # limit positions
        limit_positions(self)

        # disable buttons if not selected
        if self.parent.selected_planet:
            if self.parent.selected_planet.name != self.name:
                self.hide_building_buttons()
            elif self.debug:
                self.draw_dict()

        # disable on build menu open
        self.update_game_variables()
        if self.parent.build_menu_visible:
            self.disable()
            return

        # tooltip and info text
        if self.explored:
            self.enable()
            self.parent.fog_of_war.draw_fog_of_war(self)

            if not self.name == "Sun":
                self.tooltip = "right click to build something useful!"
                self.text.set_alpha(255)

            # only the first time after exploring
            if not self.just_explored:
                self.setImage(self.image_raw)
                self.set_info_text()
                self.get_explored()

                # set this variable to only set info text on first time
                self.just_explored = True
        else:
            self.disable()

        self.set_population_limit()

    def get_explored(self):
        """
        called only once when the planet gets explored
        shows buttons ect
        """
        sounds.play_sound(sounds.happy, channel=4)
        self.planet_button_array.enable()
        for i in self.planet_button_array.getButtons():
            i.show()

        self.show_overview_button()
        self.parent.set_selected_planet(self)
        self.parent.explored_planets.append(self)
