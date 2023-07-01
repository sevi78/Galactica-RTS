import time

import pygame

import source.utils.Globals
from source.gui.Button import Button
from source.gui.ProgressBar import ProgressBar
from source.gui.WidgetHandler import WidgetBase
from source.utils import colors, images
from source.utils.Globals import pictures_path
from source.utils.config import building_production_time
from source.utils.sounds import sounds


class BuildingWidget(WidgetBase):
    def __init__(self, win, x, y, width, height, name, parent, planet, key, value, **kwargs):
        super().__init__(win, x, y, width, height, **kwargs)
        self.layer = kwargs.get("layer")
        self.text = name + ":"
        self.name = name
        self.parent = parent
        self.planet = planet
        self.key = key
        self.value = value
        self.immediately_build_cost = 0
        self.tooltip = kwargs.get("tooltip", "no tooltip set yet!")

        # get the position and size
        self.win = pygame.display.get_surface()
        height = win.get_height()
        self.dynamic_x = self.parent.ui_helper.anchor_right
        self.cue_id = len(self.parent.building_widget_list)
        self.spacing = 5
        self.dynamic_y = height - self.spacing - self.getHeight() - self.getHeight() * self.cue_id

        self.font = pygame.font.SysFont(kwargs.get("fontname", None), kwargs.get("fontsize", 15))
        self.fontsize = kwargs.get("fontsize", 15)
        self.spacing = kwargs.get("spacing", 15)
        self.image = images[pictures_path]["buildings"][self.name + "_25x25.png"]


        # button
        self.button = Button(self.win,
            x=self.dynamic_x + self.getHeight() / 2,
            y=self.dynamic_y,
            width=self.getHeight(),
            height=self.getHeight(),
            image=self.image,
            onClick=lambda: self.function("do nothing"),
            transparent=True,
            image_hover_surface_alpha=255,
            parent=parent,
            tooltip=self.tooltip, layer=self.layer)

        # text
        self.text_render = self.font.render(self.text, True, colors.frame_color, self.fontsize)

        # progress bar
        self.progress_bar_width = kwargs.get("progress_bar_width", 100)
        self.progress_bar_height = kwargs.get("progress_bar_height", 10)
        self.startTime = time.time()
        self.progress_time = building_production_time[self.name]  # kwargs.get("progress_time", 100)

        self.progress_bar = ProgressBar(win=self.win,
            x=self.dynamic_x + self.button.getWidth(),
            y=self.button._y + self.progress_bar_height / 2,
            width=self.progress_bar_width,
            height=self.progress_bar_height,
            progress=lambda: (time.time() - self.startTime) / self.progress_time,
            curved=True,
            completedColour=colors.frame_color, layer=self.layer
            )

        # register
        self.parent.building_widget_list.append(self)

    def set_building_to_planet(self):
        """
        overgive the values stores for the planet: wich building to append, sets population limit, calculates production
        and calls calculate_global_production()
        and plays some nice sound :)
        :return:
        """
        ships = ["spaceship", "cargoloader", "spacehunter"]
        sounds.play_sound("success", channel=7)
        # remove self from planets building cue:
        self.planet.building_cue -= 1

        # if it is a ship, no calculation has to be done, return
        if self.name in ships:
            self.parent.create_ship(self.name + "_30x30.png", self.planet.getX() + self.planet.getWidth(), self.planet.getY())
            self.parent.navigation.set_moveables()
            return

        # append to planets building list
        self.planet.buildings.append(self.name)

        # set new value to planets production
        setattr(self.planet, self.name, getattr(self.planet, "production_" + self.key) - self.value)
        setattr(self.parent.player, self.name, getattr(self.parent.player, self.key) - self.value)

        self.planet.set_population_limit()
        self.planet.calculate_production()
        self.parent.calculate_global_production()

    def draw(self):
        """
        reposition the elements dynamically, draw elements, and finally deletes itself
        """

        # reposition
        widget_height = self.getHeight()
        self.dynamic_x = self.parent.ui_helper.anchor_right
        spacing = 5

        # get the position and size
        win = pygame.display.get_surface()
        height = win.get_height()
        y = height - spacing - widget_height - widget_height * self.cue_id

        # button
        self.button.image_hover_surface.set_alpha(0)
        self.button.setX(self.parent.ui_helper.anchor_right)
        self.button._y = y

        # progress_bar
        self.progress_bar.setWidth(self.parent.building_panel.getWidth() - self.button.getWidth() - 15)
        self.progress_bar.setX(self.dynamic_x + self.button.getWidth() + 5)
        self.progress_bar.setY(y + self.button.getHeight() / 2)

        # draw widgets text
        self.text = self.name + ": " + str(int(self.progress_bar.percent * 100)) + "%/ " + str(self.parent.ui_helper.hms(self.progress_time))
        self.text_render = self.font.render(self.text, True, colors.frame_color, self.fontsize)
        self.win.blit(self.text_render, (self.dynamic_x + self.button.getWidth(), self.button._y + 2))

        # move down if place is free
        for i in range(len(self.parent.building_widget_list)):
            if self.parent.building_widget_list[i] == self:
                self.cue_id = self.parent.building_widget_list.index(self.parent.building_widget_list[i])

        # if progress is finished, set building to planet
        if self.progress_bar.percent == 1:
            self.set_building_to_planet()

            # finally delete it and its references
            self.delete()

    def delete(self):
        self.parent.building_widget_list.remove(self)
        self.__del__()
        self.progress_bar.__del__()
        self.button.__del__()

    def listen(self, events):
        for event in events:
            if self.button.imageRect.collidepoint(pygame.mouse.get_pos()):
                self.immediately_build_cost = int((1 - self.progress_bar.percent) * building_production_time[self.name])
                self.set_tooltip()

    def function(self, arg):
        source.utils.Globals.tooltip_text = ""
        self.build_immediately()
        self.set_building_to_planet()
        self.delete()

    def set_tooltip(self):
        self.button.tooltip = f"are you sure to build this {self.name} immediately? this will cost you {self.immediately_build_cost} technology units?"

    def build_immediately(self):
        self.parent.player.technology -= self.immediately_build_cost
