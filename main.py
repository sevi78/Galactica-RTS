import time

from pygame_widgets.util import drawText


import source
import source.Globals
import source.Images
import source.SaveLoad
import source.Settings
import source.WidgetHandler
import source.config
from source.AppHelper import AppHelper
from source.BuildingWidget import BuildingWidget
from source.Button import Button
from source.Globals import WIDTH, HEIGHT
from source.Sounds import sounds
from source.UIBuilder import UIBuilder
from source.__init__ import update
from source.Globals import *


#
# from modulefinder import ModuleFinder
# finder = ModuleFinder()
# finder.run_script("Mains.py")
# for name, mod in finder.modules.items():
#     print(name)
# from TextHandler import drawText


#
# global menu
# menu = pygame_menu.Menu("test",200,300,)


class GameLogic:
    def build(self, building):
        """
        this builds the buildings on the planet: first check for prices ect, then build a building_widget
        that overgives the values to the planet if ready
        :param building: string
        :return: nothing
        """
        planet = self.selected_planet
        # only build if selected planet is set
        if not planet: return

        # check for minimum population
        if building in self.buildings_list:
            if source.config.build_population_minimum[building] > planet.population:
                self.event_text = "you must reach a population of minimum " + str(
                    source.config.build_population_minimum[building]) + " people to build a " + building + "!"

                sounds.play_sound("bleep", channel=7)
                return


        # build building widget, first py the bill
        # pay the bill

        if planet.building_cue >= planet.building_slot_amount:
            self.event_text = "you have reached the maximum(" + str(planet.building_slot_amount) + ") of buildings that can be build at the same time on " + planet.name + "!"
            sounds.play_sound("bleep", channel=7)
            return
        if len(planet.buildings) + planet.building_cue >= planet.buildings_max:
            self.event_text = "you have reached the maximum(" + str(planet.buildings_max) + ") of buildings that can be build on " + planet.name + "!"
            sounds.play_sound("bleep", channel=7)
            return

        self.build_payment(building)

        # predefine variables used to build building widget to make shure it is only created once
        widget_key = None
        widget_value = None
        widget_name = None

        # check for prices
        if building in self.buildings_list:
            for key, value in self.prices[building].items():
                if (getattr(self.player, key) - value) > 0:

                    widget_key = key
                    widget_value = value
                    widget_name = building
                else:
                    return

        # create building_widget ( progressbar)
        if widget_key:

            widget_width = self.building_panel.getWidth()
            widget_height = 35
            spacing = 5

            # get the position and size
            win = pygame.display.get_surface()
            height = win.get_height()
            y = height - spacing - widget_height - widget_height * len(self.building_widget_list)

            sounds.play_sound(sounds.bleep2, channel=7)

            print(planet.building_slot_amount, planet.building_cue)

            building_widget = BuildingWidget(win=self.win,
                x=self.building_panel._x,
                y=y,
                width=widget_width,
                height=widget_height,
                name=widget_name,
                fontsize=18,
                progress_time=5,
                parent=self,
                key=widget_key,
                value=widget_value,
                planet=planet,
                tooltip="building widdget", layer=4
                )
            # add building widget to building cue to make shure it can be build only if building_cue is < building_slots_amount
            planet.building_cue += 1

    def build_payment(self, building):
        """
        pays the bills if something is build ;)
        :param building: str
        :return:
        """
        # only build if has selected planet
        if not self.selected_planet: return

        # if "building" is a building and not called from another button(hack)
        if building in self.buildings_list:
            # check for prices
            for key, value in self.prices[building].items():
                # if price is bigger than zero
                if (getattr(self.player, key) - value) > 0:
                    setattr(self.player, key, getattr(self.player, key) - value)

    def add_object(self):
        x = 200
        y = 100
        size = 30
        spacing = 10
        for key, value  in source.Globals.images[source.Globals.pictures_path]["celestial objects"].items():

            button = Button(self.win, x,y,30,30,False, image=value)
            y += size + spacing


class App(AppHelper, UIBuilder, GameLogic):
    def __init__(self, width, height):
        UIBuilder.__init__(self, width, height)
        # set app-icon
        pygame.display.set_icon(source.Globals.images[source.Globals.pictures_path]["planets"]["Zeta Bentauri_60x60.png"])

        # start timer
        self.timer_start = time.time()

    def update(self, events):
        """
        updates all game Elements except pygame_widgets and calls functions that need events
        :param events:
        :return:
        """
        self.events = events

        for event in events:
            # only resize background on window resize
            if event.type == pygame.WINDOWRESIZED :
                pass
                #self.bg = pygame.transform.scale(self.bg, (self.win.get_width(), self.win.get_height()))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    if self.build_menu_visible:
                        self.close_build_menu()
                    else:
                        self.open_build_menu()
                if event.key == 97:# a
                    self.add_object()


        # set fps
        self.clock.tick(source.Globals.frames_per_second)
        pygame.display.set_caption(source.Globals.root + "   " + str(f"FPS: {self.clock.get_fps()}") )

        # necessary functions, maybe could put these outside somehow
        self.quit_game(events)
        #self.clear_widgets(events)
        self.ui_helper.update()

        # update objects
        self.update_icons(events)

        for i in self.ships:
            i.update()

        self.player.update()
        self.event_panel.update()

        # event text
        event_text_height =120
        self.event_text_font = pygame.font.SysFont(None, 25)
        prefix = "GPT-1357: "
        self.event_display_text = prefix + self.event_text
        drawText(self.win, self.event_display_text,source.Globals.colors.frame_color,
                 (self.ui_helper.left, self.ui_helper.anchor_bottom, self.ui_helper.width, event_text_height), self.event_text_font, "center")

        # cheat
        self.cheat(events)

        # set global population
        self.player.population = int(sum([i.population for i in self.planets]))


        #self.background.draw()

    def loop(self):

        """
        the game loop: blits the background,fog of war.
        calls self.update,  updates pygame_widgets and pygame.display
        :return:
        """
        # game loop
        while self.run == 1:


                #self.zoom_win.loop()
            #self.building_editor.draw()
            # settings
            #self.settings.mainloop(self.win, main_background,fps_limit =source.Globals.frames_per_second)
            events = pygame.event.get()


            # draw background, fog of war
            if hasattr(self,"background_image"):
                self.background_image.draw()


            self.update_game_objects(events)
            if enable_zoom:
                self.pan_zoom_handler.listen(events)

            #self.box_selection.listen(events, self.win)

            update(events)
            # navigate
            if navigation:
                self.navigation.listen(events)


            if not source.Globals.game_paused:
                self.update(events)

            self.set_screen_size((1400,900), events)
            self.tooltip_instance.update(events)

            # self.main_menu.disable()
            # self.main_menu.mainloop(self.win, None)

            #self.console()
            #self.EditorTest()
            #self.drag(events)
            # control()
            pygame.display.update()

import pygame

app = App(WIDTH, HEIGHT)


