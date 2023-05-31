import math
import os
import sys

import pygame

from source.config import production, planet_positions


class Inspector:# doesnt work :(
    def memory(self):
        # Getting all memory using os.popen()
        total_memory, used_memory, free_memory = map(
            int, os.popen('free -t -m').readlines()[-1].split()[1:])

        usage = "RAM memory % used: " +  str(round((used_memory / total_memory) * 100, 2)) + "used_memory: " + str(used_memory)

        return usage


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
        self.anchor_right  = self.width - value

    def set_anchor_bottom(self, value):
        self.anchor_bottom  = self.height - value

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

        x = win_width/2 - width/2
        y = win_height/2 - height/2
        pos = (x,y)
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

    def hms(self, seconds):#no use
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

    def quit_game(self, events):
        """
        :param events:
        :return:
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
        :return:
        """
        x = 100
        y = 100
        import os

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
                    pygame.display.set_mode(size, pygame.RESIZABLE)

    def clear_widgets(self, events):
        #print ("clear_widgets: not implemented")
        return
        # kaputt
        """ deletes all WidgetHandler.WidgetHandler.getWidgets(), (Buttons from 'Button' class """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == 8:  # pygame.K_DELETE:
                    print("clear widgets", event.key)

                    # get all widgets
                    widgets =WidgetHandler.WidgetHandler.getWidgets()

                    # why the f..k we need to repeat the delete process???
                    while len(widgets) > 0:
                        # remove them
                        for widget in widgets:
                            # print (widget)
                            WidgetHandler.WidgetHandler.removeWidget(widget)

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
            self.building_panel.update()

    def update_icons(self, events):
        for icon in self.icons:
            if hasattr(icon, "update"):
                icon.update(events)

    def update_game_objects(self, events):
        for game_object in self.game_objects:
            game_object.update()

    def calculate_global_production(self):
        """
        calculates thesource.Globals production of all planets, sets values to player
        :return:
        """
        self.production = {
            "energy": 0,
            "food": 0,
            "minerals": 0,
            "water": 0,
            "technology":0,
            "city":0
            }

        self.population_limit = 0
        for planet in self.planets:
            # set population limits
            self.population_limit += planet.population_limit

            for i in planet.buildings:
                for key, value in production[i].items():
                    self.production[key] += value

        self.player.population_limit = self.population_limit
        self.player.production = self.production

        self.production_water = self.production["water"]
        self.production_energy = self.production["energy"]
        self.production_food = self.production["food"]
        self.production_minerals = self.production["minerals"]

        # self.player.population = population

    def get_planet_positions(self):
        """
        sets planet positions into dict, will be used for Level Editor
        :return:
        """
        for i in self.planets:

            planet_positions[i.name] = (i.getX(), i.getY())

    def cheat(self, events):
        """cheat you bloody cheater :) """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == 99:# C
                    self.player.energy += 1000
                    self.player.food += 1000
                    self.player.minerals += 1000
                    self.player.water += 1000
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
                    for p in self.planets:
                         p.explored = True

    def draw_fog_of_war(self,obj,**kwargs):
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

def get_distance(pos_a, pos_b):
    """
    returns the distance betweeen two positions
    :param pos_a:
    :param pos_b:
    :return: distance
    """
    x = pos_a[0]
    y = pos_a[1]
    x1 = pos_b[0]
    y1 = pos_b[1]

    dist_x = (x1 - x)
    dist_y = (y1 - y)
    distance = math.dist((x, y), (x1, y1))

    return distance

def limit_positions(obj):
    win = pygame.display.get_surface()
    test = 100
    zero = 0
    win_width = win.get_width()
    win_height = win.get_height()
    x = obj.getX()
    y = obj.getY()
    #
    # if obj.type == "star" and not obj._hidden and x in range(-10, 10):
    #     print ("x, y, obj.getWidth(), obj._hidden", x, y, obj.getWidth(), obj._hidden)
    if not hasattr(obj, "crew"):
        if x <= zero or x >= win_width :
            obj.hide()
        elif y <= zero or y >= win_height:
            obj.hide()
        else:
            obj.show()

def orbit(obj):
    return
    # Add the rotated offset vector to the pos vector to get the rect.center.
    obj.rect.center = obj.pos + obj.offset.rotate(obj.orbit_angle)
    orbit_point = obj.orbit_object.imageRect.center + self.offset.rotate(self.angle)

    self.imageRect.center = orbit_point

    def update(obj):
        obj.orbit_angle -= 2
        # Add the rotated offset vector to the pos vector to get the rect.center.
        obj.rect.center = obj.pos + obj.offset.rotate(obj.orbit_angle)


    # print (self.imageRect.center)



    # print (self.imageRect.center)
    # self.setX(self.imageRect.left)
    # self.setY(self.imageRect.top)
    #
    # # orbit_point = (self.imageRect.left,self.imageRect.top)
    #
    # if self.get_distance_to(orbit_point) >= 1:
    #     self.move_to(orbit_point)
    #     self.orbiting = False
    # else:
    #     self.orbiting = True
    #
    # if self.orbiting:
    # self.setX(self.imageRect.left)
    # self.setY(self.imageRect.top)
    # self.orbiting = True

    # set progress bar position





