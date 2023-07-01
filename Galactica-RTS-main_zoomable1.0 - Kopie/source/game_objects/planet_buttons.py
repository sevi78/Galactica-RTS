import os
import pygame

import source
from source.gui import ButtonArray, ImageButton
from source.utils import load_file, images, colors, pictures_path


class PlanetConfig:

    def __init__(self, **kwargs):

        self.name = kwargs.get("name")
        self.database_path = "levels" + os.sep + "level1" + os.sep + "planets" + os.sep + self.name + ".json"
        self.x = load_file(self.database_path)["x"]  # source.config.planet_positions[self.name][0]  # x
        self.y = load_file(self.database_path)["y"]
        self.info_text = kwargs.get("info_text")
        self.population_grow = 0.0
        self.alien_population = 0
        self.buildings_max = 10
        self.building_slot_amount = 3
        self.specials = []
        self.type = load_file(self.database_path)["type"]#source.game_objects.texts.planet_texts[self.name].split("\n")[3].split(": ")[1]
        self.possible_resources = kwargs.get("possible_resources")
        self.image_name_small = load_file(self.database_path)["image_name_small"]#level_dict[1][self.name]["image_name"]
        self.image_name_big = self.name + "_150x150.png"
        self.orbit_planet = "Sun"
        self.orbit_speed = 0.002


class PlanetButtons(PlanetConfig):
    """
    base class of Planet. stores the buttons and some variables.
    holds the functions for the buttons, create ect
    """

    def __init__(self, **kwargs):
        self.overview_buttons = []

    def hide_building_buttons(self):
        for buttonarray in self.building_buttons_list:
            buttonarray.hide()
            for button in buttonarray.getButtons():
                button.hide()

    def show_building_buttons(self, resource):
        """
        shows the buildong button only if planet is explored
        :param resource:
        """

        if self.building_buttons[resource].isVisible():
            self.building_buttons[resource].hide()
            for button in self.building_buttons[resource].getButtons():
                button.hide()
        else:
            self.building_buttons[resource].show()
            for button in self.building_buttons[resource].getButtons():
                button.show()

    def show_overview_button(self):
        """
        shows the overview buttons if planet is explored
        """
        for i in self.overview_buttons:
            if self.explored:
                if not self.name == "Sun":
                    i.show()
            else:
                i.hide()

    def set_building_button_tooltip(self, i):
        """
        creates tooltops for the buttons
        :param i:
        """
        return_list = []
        price_list = []
        production_list = []

        # prices
        text = ""
        for building in self.parent.buildings[i.name]:
            if building[0] == "a":
                text = "to build an " + building + " you need: "
            else:
                text = "to build a " + building + " you need: "

            for key, value in source.utils.config.prices[building].items():
                if value > 0:
                    text += key + ": " + str(value) + ", "
            text = text[:-2]

            price_list.append(text)

        # production
        text = ""
        for building in self.parent.buildings[i.name]:
            # population
            if building in self.population_buildings:
                text = ". a " + building + " increases the planets population limit by " + str(
                    self.population_buildings_values[building]) + "  "

            elif building[0] == "a":
                text = " . an " + building + " will produce: "
            else:
                text = " . a " + building + " will produce: "

            for key, value in source.utils.config.production[building].items():
                if value > 0:
                    text += key + ": " + str(value) + ", "
                #
                # elif value < 0:
                #     text += "but it will also cost you " + key + ": " +  str(value) + " everytime it produces something!, "
            text = text[:-2]

            production_list.append(text)

        for i in range(len(price_list)):
            return_list.append(price_list[i] + production_list[i])

        return return_list

    def create_planet_button_array(self):
        """
        creates the ui elements for the planet:
        building icons, overview icons, buttons ect
        :return:
        """
        self.building_buttons = {}
        self.building_buttons_list = []
        self.overview_buttons = []
        slot_image_size = 25
        x = self._x
        y = self._y - self.getHeight() / 2

        # # open build menu
        # self.button_build_menu_open = Button(self.win, x-slot_image_size,y,slot_image_size, slot_image_size,isSubWidget=False,
        #                                     image= images[pictures_path]["icons"]["build.png"],
        #                                     onClick=lambda: self.parent.open_build_menu()  )
        # self.button_build_menu_open.hide()

        # resource icons
        images_scaled = [pygame.transform.scale(
            images[pictures_path]["resources"][i + "_25x25.png"], (slot_image_size, slot_image_size))
                  for i in self.possible_resources]

        self.planet_button_array = ButtonArray(self.win,
            x=x,
            y=y,
            width=len(self.possible_resources) * slot_image_size,
            height=slot_image_size + 1,
            shape=(len(self.possible_resources), 1), border=1, bottomBorder=0, rightBorder=0, leftBorder=0, topBorder=0,
            images=images_scaled,
            borderThickness=2, inactiveBorderColours=[colors.frame_color for i in range(6)],

            tooltips=self.possible_resources,
            onClicks=(
                lambda: self.show_building_buttons(self.possible_resources[0]),
                lambda: self.show_building_buttons(self.possible_resources[1]),
                lambda: self.show_building_buttons(self.possible_resources[2]),
                lambda: self.show_building_buttons(self.possible_resources[3]),
                lambda: self.show_building_buttons(self.possible_resources[4]),
                lambda: self.show_building_buttons(self.possible_resources[5])
                ),
            parents=[self, self, self, self, self, self],
            ui_parents=[self, self, self, self, self, self],
            names=self.possible_resources,
            layers=[9, 9, 9, 9, 9, 9],
            inactiveColours=[colors.background_color for i in range(6)],
            borderColours=[colors.frame_color for i in range(6)])

        # building buttons
        for i in self.planet_button_array.getButtons():
            images_scaled = [
                images[pictures_path]["buildings"][self.parent.buildings[i.name][0] + "_25x25.png"],
                images[pictures_path]["buildings"][self.parent.buildings[i.name][1] + "_25x25.png"],
                images[pictures_path]["buildings"][self.parent.buildings[i.name][2] + "_25x25.png"]]

            scaled_images = [pygame.transform.scale(image, (slot_image_size, slot_image_size)) for image in images_scaled]
            info_texts = [source.utils.config.create_info_panel_building_text()[self.parent.buildings[i.name][0]],
                          source.utils.config.create_info_panel_building_text()[self.parent.buildings[i.name][1]],
                          source.utils.config.create_info_panel_building_text()[self.parent.buildings[i.name][2]]]

            building_buttons = ButtonArray(self.win,
                x=i.getX(),
                y=y - slot_image_size - slot_image_size - i.getHeight(),
                width=slot_image_size + 1,
                height=3 * slot_image_size,
                shape=(1, 3),
                border=1, bottomBorder=0, rightBorder=0, leftBorder=0, topBorder=0,
                images=scaled_images,
                borderThickness=0,
                texts=[self.parent.buildings[i.name][0], self.parent.buildings[i.name][1],
                       self.parent.buildings[i.name][2]],
                tooltips=self.set_building_button_tooltip(i),

                parents=[self, self, self],
                ui_parents=[self, self, self],
                names=self.parent.buildings[i.name],
                textColours=[(0, 0, 0), (0, 0, 0), (0, 0, 0)],
                fontSizes=[0, 0, 0],
                info_texts=info_texts,
                layers=[9, 9, 9, 9, 9, 9]
                )

            # hide initially
            building_buttons.hide()
            self.planet_button_array.hide()

            # register
            self.building_buttons[i.name] = building_buttons
            self.building_buttons_list.append(building_buttons)

        # thumpsup button
        self.thumpsup_button_size = (20, 20)
        self.thumpsup_button = ImageButton(self.win,
            x=self._x - slot_image_size,
            y=self.planet_button_array.getY(),
            width=self.thumpsup_button_size[0],
            height=self.thumpsup_button_size[1],
            isSubWidget=False,
            onClick=lambda: print("no function"),
            transparent=True,
            image_hover_surface_alpha=255,
            parent=self.parent,
            ui_parent=self,
            tooltip="indicates whether the production is in plus ",
            image=pygame.transform.flip(pygame.transform.scale(images[pictures_path]["icons"][
                "thumps_up.png"], self.thumpsup_button_size), True, False),
            layer=9)

        self.overview_buttons.append(self.thumpsup_button)

        # smiley
        self.smiley_button_size = (24, 24)
        self.smiley_button = ImageButton(self.win,
            x=self._x - slot_image_size * 2,
            y=self.planet_button_array.getY(),
            width=self.smiley_button_size[0],
            height=self.smiley_button_size[1],
            isSubWidget=False,
            onClick=lambda: print("no function"),
            transparent=True,
            image_hover_surface_alpha=255,
            parent=self.parent,
            ui_parent=self,
            tooltip="indicates the satisfaction of the population", image=images[pictures_path]["icons"][
                "smile.png"],
            layer=9
            )

        self.smiley_button.hide()
        self.thumpsup_button.hide()
        self.overview_buttons.append(self.smiley_button)