import json
import os
import sys
from threading import Thread

import pygame

import source

from source import utils
from source.utils import Globals
from source.utils.config import production, planet_positions, ship_prices, prices


class UIHelper:
    def __init__(self, parent):
        self.parent = parent
        self.win = pygame.display.get_surface()
        self.width = self.win.get_width()
        self.height = self.win.get_height()

        self.right = 0
        self.left = 0
        self.top = 0
        self.bottom = 0

        self.anchor_right = 0
        self.anchor_left = 0
        self.anchor_top = 0
        self.anchor_bottom = 0

        self.spacing = 10

    def set_anchor_right(self, value):
        self.anchor_right = self.width - value

    def set_anchor_bottom(self, value):
        self.anchor_bottom = self.height - value

    def set_spacing(self, spacing):
        self.spacing = spacing

    def center_pos(self, width, height):
        """
        gets center of the screen
        :param width:
        :param height:
        :return: center of the screen
        """
        win = pygame.display.get_surface()
        win_width = win.get_width()
        win_height = win.get_height()

        x = win_width / 2 - width / 2
        y = win_height / 2 - height / 2
        pos = (x, y)
        return pos

    def update(self):
        """
        updates positions for dynamic UI
        :return:
        """
        # print("UIHelper:")
        self.win = pygame.display.get_surface()
        self.width = self.win.get_width()
        self.height = self.win.get_height()

        self.set_anchor_right(self.parent.building_panel.getWidth())
        self.set_anchor_bottom(30)

        # print (self.width, self.height)
        # print ("UIHelper: anchor_right:  ", self.anchor_right)

    def hms(self, seconds):  # no use
        """
        time converter
        :param seconds:
        :return: datetime format
        """
        h = seconds // 3600
        m = seconds % 3600 // 60
        s = seconds % 3600 % 60
        return '{:02d}:{:02d}:{:02d}'.format(h, m, s)


class AppHelper:
    """ this class is only to make App more readable, must be inheritet to 'App' """

    def __init__(self):
        self.population_limit = None
        self.ctrl_pressed = False
        self.s_pressed = False

    def quit_game(self, events):
        """
        :param events:
        quit the game with quit icon or esc
        """
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

    def set_screen_size(self, size, events):
        """
        set the screen site using 's'
        :param size:
        :param events:
        """
        x = 100
        y = 100

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
                    pygame.display.set_mode(size, pygame.RESIZABLE)

    def set_planet_name(self):
        """
        sets the planet name if explored,  or ??? of not
        :return: planetname
        """
        if self.selected_planet:
            if self.selected_planet.explored:
                planetname = self.selected_planet.name + ":"
            else:
                planetname = "???"
        else:
            planetname = "select planet"

        return planetname

    def open_build_menu(self):
        if not self.selected_planet:
            return

        self.build_menu_visible = True

        # disable all object below
        for i in self.build_menu_widgets:
            i.show()
            try:
                for button in i.getButtons():
                    button.show()
            except:
                pass

        for i in self.game_objects:
            i.disable()
        for i in self.planets:
            i.disable()

        for i in self.ships:
            i.disable()

        # disable button is not possible to build it
        for key, value in self.build_menu_widgets_buildings.items():
            for button in self.build_menu_widgets_buildings[key]:
                if not button.property in self.selected_planet.possible_resources:
                    # button.disable()
                    button.hide()

                else:
                    # button.enable()
                    button.show()

    def close_build_menu(self):
        self.build_menu_visible = False

        if self.build_menu_widgets[0].isVisible():

            # to_hide = [1, 3]
            # for i in WidgetHandler.WidgetHandler.getWidgets():
            #     if i.layer in to_hide:
            #         i.show()

            for i in self.build_menu_widgets:
                i.hide()
                try:
                    for button in i.getButtons():
                        button.hide()
                except:
                    pass

            for i in self.game_objects:
                i.enable()

            for i in self.planets:
                i.enable()

            for i in self.ships:
                i.enable()

    def set_selected_planet(self, planet):
        if planet:
            self.selected_planet = planet
            self.info_panel.update(self.events)

    def update_icons(self, events):
        for icon in self.icons:
            if hasattr(icon, "update"):
                icon.update(events)

    # noinspection PyMissingOrEmptyDocstring
    def update_game_objects(self, events):
        for game_object in self.game_objects:
            game_object.update()

    def calculate_global_production(self):
        """
        calculates the production of all planets, sets values to player
        :return:
        """
        self.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "technology": 0,
            "city": 0
            }

        self.population_limit = 0
        for planet in self.planets:
            # set population limits
            self.population_limit += planet.population_limit

            # set production values
            for i in planet.buildings:
                for key, value in production[i].items():
                    self.production[key] += value

        # subtract the building_slot_upgrades ( they cost 1 energy)
        for planet in self.planets:
            self.production["energy"] -= self.get_sum_up_to_n(planet.building_slot_upgrade_energy_consumption, planet.building_slot_upgrades+1)

        self.player.population_limit = self.population_limit
        self.player.production = self.production

        self.production_water = self.production["water"]
        self.production_energy = self.production["energy"]
        self.production_food = self.production["food"]
        self.production_minerals = self.production["minerals"]

        # self.player.population = population



    def cheat(self, events):
        """cheat you bloody cheater :) """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == 99:  # C
                    self.player.energy += 1000
                    self.player.food += 1000
                    self.player.minerals += 1000
                    self.player.water += 1000
                    self.player.technology += 10000

                    if self.ship:
                        self.ship.energy = 10000

                    self.player.population += 250
                    for i in self.planets:
                        i.population += 250

                    # for i in WidgetHandler.WidgetHandler.getWidgets():
                    #     if "Planet" in str(i):
                    #         i.hide()
                    #         print (get_distance(self.ship.pos, (i.getX(), i.getY())))
                    #     # self.get_planet_positions()
                    # for p in self.planets:
                    #     p.explored = True

    def draw_fog_of_war(self, obj, **kwargs):
        """
        draws the fog of war circle based on the fog of war raduis of the obj
        :param obj:
        :param kwargs:
        :return:
        """
        self.fog_of_war.draw_fog_of_war(obj)

        # x, y = kwargs.get("x", obj.getX() + obj.getWidth()/2), kwargs.get("y", obj.getY() + obj.getHeight()/2)
        # radius = kwargs.get("radius", obj.fog_of_war_radius)
        #
        # if hasattr(self, "fog_of_war"):
        #     pygame.draw.circle(surface=self.fog_of_war, color=(60, 60, 60), center=(
        #      x, y), radius=radius, width=0)

    def store_planet_positions(self, events):
        # gets values from save file(settings.json)
        level = source.utils.Globals.app.level
        dirpath = os.path.dirname(os.path.realpath(__file__))
        database_path = os.path.split(dirpath)[0].split("source")[0] + "database" + os.sep
        pictures_path = os.path.split(dirpath)[0].split("source")[0] + "pictures" + os.sep
        level_path = database_path + "levels" + os.sep + "level" + str(level) + os.sep

        # check events for l_ctr +s for saving
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.s_pressed = True
                if event.key == pygame.K_LCTRL:
                    self.ctrl_pressed = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    self.s_pressed = False
                if event.key == pygame.K_LCTRL:
                    self.ctrl_pressed = False

            if self.ctrl_pressed and self.s_pressed:
                # save each file
                for planet in self.planets:
                    # get values from file and adjust
                    with open(os.path.join(level_path + "planets" + os.sep + planet.name + ".json"), 'r+') as file:
                        planet_settings = json.load(file)
                        planet_settings["x"] = planet.getX()
                        planet_settings["y"] = planet.getY()

                    # write back to file
                    with open(os.path.join(level_path + "planets" + os.sep + planet.name + ".json"), 'w') as file:
                        json.dump(planet_settings, file)
                        print(planet_settings)

    def get_planet_positions(self):
        """
        sets planet positions into dict, will be used for Level Editor
        :return:
        """
        for i in self.planets:
            planet_positions[i.name] = (i.getX(), i.getY() )
            #planet_positions[i.name] = (i.getX() - self.navigation.scene_x, i.getY() - self.navigation.scene_y)

        return planet_positions

    def get_sum_up_to_n(self, dict, n):
        sum = 0
        for key, value in dict.items():
            if key < n:
                sum += value

        return sum





def check_function_execution(func):


    func_thread = Thread(target=func)

    return func_thread.is_alive()


def set_event_text(self,new_text): #doesnt work :(
    if new_text != self.parent.event_text:
        self.parent.event_text = new_text


def check_if_enough_resources_to_build(thing_to_build):
    price_dict = None
    build_type = None
    check = True
    text = f"not enough resources to build a {thing_to_build}! you are missing: "

    # get the corresponding price dict
    if thing_to_build in prices.keys():
        build_type = "building"
        price_dict = prices

    elif thing_to_build in ship_prices.keys():
        build_type = "ship"
        price_dict = ship_prices
    else:
        print(f"wrong input for check_if_enough_resources_to_build:, no key for {thing_to_build}  in any price dict")
        return False

    # check for prices
    for key, value in price_dict[thing_to_build].items():
        if not getattr(utils.Globals.app.player, key) - value >= 0:
            text += f"{getattr(utils.Globals.app.player, key) - value} {key}, "
            check = False

    if not check:
        text = text[:-2] + "!"
        Globals.app.event_text = text

    return check


