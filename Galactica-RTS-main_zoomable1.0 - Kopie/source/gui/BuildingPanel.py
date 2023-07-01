import time

import pygame
from pygame_widgets.util import drawText

import source
from source import utils
from source.editors import PlanetEditor, BuildingEditor
#from source.game_objects.Planet import PlanetButtons
from source.gui.Button import Button, ImageButton, ButtonArray
from source.gui.Slider import Slider
from source.gui.WidgetHandler import WidgetBase
from source.gui.space_harbor import SpaceHarbor
from source.interaction.Navigation import Navigation
from source.utils import colors, sounds, images
from source.utils.Globals import pictures_path






class PlanetButtons():
    """
    base class of Planet. stores the buttons and some variables.
    holds the functions for the buttons, create ect
    """

    def __init__(self,x,y,parent, **kwargs):
        self.overview_buttons = []
        self.x = x
        self.y = y
        self.parent = parent
        self.win = self.parent.win
        self.population_buildings = ["town", "city", "metropole"]
        self.population_buildings_values = {"town": 1000, "city": 10000, "metropole": 100000}


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
        if not self.parent.parent.selected_planet:
            return

        for i in self.overview_buttons:
            if self.parent.parent.selected_planet.explored:

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
        self.possible_resources = [ "water", "energy", "food", "minerals", "technology",  "city"]
        slot_image_size = 25
        x = self.x
        y = self.y +300


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
            #ui_parents=[self, self, self, self, self, self],
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
                #ui_parents=[self, self, self],
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
            x=self.x - slot_image_size,
            y=self.planet_button_array.getY(),
            width=self.thumpsup_button_size[0],
            height=self.thumpsup_button_size[1],
            isSubWidget=False,
            onClick=lambda: print("no function"),
            transparent=True,
            image_hover_surface_alpha=255,
            parent=self.parent,
            #ui_parent=self,
            tooltip="indicates whether the production is in plus ",
            image=pygame.transform.flip(pygame.transform.scale(images[pictures_path]["icons"][
                "thumps_up.png"], self.thumpsup_button_size), True, False),
            layer=9)

        self.overview_buttons.append(self.thumpsup_button)

        # smiley
        self.smiley_button_size = (24, 24)
        self.smiley_button = ImageButton(self.win,
            x=self.x - slot_image_size * 2,
            y=self.planet_button_array.getY(),
            width=self.smiley_button_size[0],
            height=self.smiley_button_size[1],
            isSubWidget=False,
            onClick=lambda: print("no function"),
            transparent=True,
            image_hover_surface_alpha=255,
            parent=self.parent,
            #ui_parent=self,
            tooltip="indicates the satisfaction of the population", image=images[pictures_path]["icons"][
                "smile.png"],
            layer=9
            )

        self.smiley_button.hide()
        self.thumpsup_button.hide()
        self.overview_buttons.append(self.smiley_button)
class BuildingSlot:
    """ this handles the building slot up/down grades and the tooltips
    this code is absolutely terrible, but it works :)
    """
    def __init__(self):
        self.minus_button_image = {}
        self.plus_button_image = {}
        self.tooltip = ""
        self.plus_just_hovered = False
        self.minus_just_hovered = False

    def set_building_slot_tooltip_plus(self, events):
        # if not planet selected, do nothing
        if not self.parent.selected_planet:
            return

        planet = self.parent.selected_planet
        upgrades = planet.building_slot_upgrades
        consumption = planet.building_slot_upgrade_energy_consumption
        prices = planet.building_slot_upgrade_prices
        max = len(planet.building_slot_upgrade_energy_consumption)-2

        # check for mouse collision with image
        for button_name, image_rect in self.plus_button_image.items():
            if button_name == "plus_icon":

                if image_rect.collidepoint(pygame.mouse.get_pos()):
                    self.hover = True
                    if not self.plus_just_hovered:
                        self.plus_just_hovered = True
                else:
                    self.hover = False

        # on hover set tooltip
        if self.hover:
            # if not max upgrade reached
            if upgrades <= max:
                    self.tooltip = f"Upgrade from {planet.building_slot_amount} building slots to " \
                                                  f"{planet.building_slot_amount + 1}? this will cost you " \
                                                  f"{prices[upgrades]}" \
                                                  f" technology! it will reduce the energy production by" \
                                                  f" {consumption[upgrades+1]}"
            else:
                self.tooltip = f"you have reached the maximum {max} of possible building slot upgrades !"

        self.submit_tooltip()

    def set_building_slot_tooltip_minus(self, events):
        # if not planet selected, do nothing
        if not self.parent.selected_planet:
            return

        planet = self.parent.selected_planet
        upgrades = planet.building_slot_upgrades
        consumption = planet.building_slot_upgrade_energy_consumption
        min = 0
        self.tooltip = ""

        # check for mouse collision with image
        for button_name, image_rect in self.minus_button_image.items():
            if button_name == "minus_icon":

                if image_rect.collidepoint(pygame.mouse.get_pos()):
                    self.hover = True
                    if not self.minus_just_hovered:
                        self.minus_just_hovered = True
                else:
                    self.hover = False

        # on hover set tooltip
        if self.hover:
            # if not max upgrade reached
            if planet.building_slot_amount >= min +1:
                    self.tooltip = f"Downgrade from {planet.building_slot_amount} building slots to " \
                                                  f"{planet.building_slot_amount - 1}? this will not give anything back,  " \
                                                  f" but it will increase the energy production by" \
                                                  f" {consumption[upgrades]}"
            else:
                self.tooltip = f"you have reached the minimum{min} of possible building slot downgrades !"

        self.submit_tooltip()

    def reset_building_slot_tooltip(self):
        if not self.parent.selected_planet:
            return

        if not self.plus_button_image["plus_icon"].collidepoint(pygame.mouse.get_pos()):
            if self.plus_just_hovered:
                utils.Globals.tooltip_text = ""
                self.plus_just_hovered = False

        if not self.minus_button_image["minus_icon"].collidepoint(pygame.mouse.get_pos()):
            if self.minus_just_hovered:
                utils.Globals.tooltip_text = ""
                self.minus_just_hovered = False

    def submit_tooltip(self):
        if self.tooltip != "":
            if self.tooltip != utils.Globals.tooltip_text:
                utils.Globals.tooltip_text = self.tooltip

    def upgrade_building_slots(self, events):
        planet = self.parent.selected_planet
        do_upgrade = False

        # check if not max is reached
        if planet.building_slot_upgrades <= len(planet.building_slot_upgrade_prices)-2:
            # now get the next price
            price = planet.building_slot_upgrade_prices[planet.building_slot_upgrades]

            # on hover and click, do upgrade
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button_name, image_rect in self.plus_button_image.items():
                        if button_name == "plus_icon":
                            if image_rect.collidepoint(pygame.mouse.get_pos()):
                                do_upgrade = True

        # max upgrades reached, exit function
        else:
            self.parent.event_text = f"maximum {planet.building_slot_upgrades} building slots reached!"
            return

        # if do_upgrade, set values
        if not do_upgrade:
            return

        # if enough technology
        if self.parent.player.technology - price > 0:
            self.parent.event_text = f"Upgraded from {planet.building_slot_amount} building slots to {planet.building_slot_amount + 1}!"
            # if not max reached
            if planet.building_slot_upgrades < len(planet.building_slot_upgrade_prices.items()):
                planet.building_slot_amount += 1
                planet.building_slot_upgrades += 1
                self.parent.player.technology -= price
        else:
            self.parent.event_text = f"not enough technology to upgrade building slot ! you have {self.parent.player.technology}, but you will need {price}"

        # finally calculate new productions
        planet.calculate_production()
        self.parent.calculate_global_production()

    def downgrade_building_slots(self, events):
        planet = self.parent.selected_planet
        do_downgrade = False

        # check if not min is reached
        if planet.building_slot_upgrades >= 0:
            # on hover and click, do upgrade
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button_name, image_rect in self.minus_button_image.items():
                        if button_name == "minus_icon":
                            if image_rect.collidepoint(pygame.mouse.get_pos()):
                                do_downgrade = True

        # min upgrades reached, exit function
        else:
            self.parent.event_text = f"minimum {0} building slots reached!"
            return

        # if do_upgrade, set values
        if not do_downgrade:
            return

        self.parent.event_text = f"Downgraded from {planet.building_slot_amount} building slots to {planet.building_slot_amount - 1}!"

        # if not min reached
        if planet.building_slot_amount > 0:
            planet.building_slot_amount -= 1
            if planet.building_slot_upgrades > 0:
                planet.building_slot_upgrades -= 1

        # finally calculate new productions
        planet.calculate_production()
        self.parent.calculate_global_production()


class BuildingPanel(WidgetBase, BuildingSlot):
    """
    displays the planets buildings, population , production
    """

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        BuildingSlot.__init__(self)


        self.planet_building_text = None
        self.planet_text = None
        self.hover = False

        self.singleton_buildings_images = {}

        self.singleton_buildings = []
        self.buildings = ["mine"]
        self.layer = kwargs.get("layer", 9)
        self.parent = kwargs.get("parent")
        self.frame_color = colors.frame_color
        self.clockslider_height = 7
        self.time_factor = 1
        self.year = 77812
        self.bg_color = pygame.colordict.THECOLORS["black"]
        self.font = pygame.font.SysFont(None, 18)
        self.resource_image_size = (15, 15)
        self.x = 0
        self.y = 0
        self.startTime = time.time()

        # construct surface
        self.surface = pygame.surface.Surface((width, height))
        self.surface.fill(self.bg_color)
        self.surface.set_alpha(19)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.x = x
        self.surface_rect.y = y
        self.size_x = kwargs.get("size_x")
        self.size_y = kwargs.get("size_y")
        self.spacing = kwargs.get("spacing")
        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, 1)

        # construct planet_surface
        self.planet_surface_size_y = 600
        self.planet_surface = pygame.surface.Surface((width, self.planet_surface_size_y))
        self.planet_surface.fill(self.bg_color)
        self.planet_surface.set_alpha(0)
        self.planet_surface_rect = self.planet_surface.get_rect()
        self.planet_surface_rect.x = x
        self.planet_surface_rect.y = y + self.surface.get_height()
        self.planet_surface_frame = pygame.draw.rect(self.win, self.frame_color, self.planet_surface_rect, 1)

        # planet image
        self.planet_image = None

        # construct slider_____
        self.spacing_x = 35
        self.clock_slider = Slider(win=self.win,
            x=self.surface_rect.x + self.spacing_x + self.spacing_x,
            y=self.surface_rect.y + int(self.spacing / 2),
            width=self.surface_rect.width - self.spacing - self.spacing_x * 2,
            height=self.clockslider_height,
            min=1, max=100, step=1, handleColour=pygame.color.THECOLORS["blue"], layer=self.layer)

        self.clock_slider.colour = self.frame_color
        self.clock_slider.setValue(utils.Globals.game_speed)

        # construct texts
        self.time_warp_text = self.font.render(str(self.clock_slider.getValue()) + "x", True, self.frame_color)
        self.year_text = self.parent.ui_helper.hms(self.year)

        # construct icon_______________________________________________________________________________________________
        self.create_icons()

        # space harbor
        self.space_harbor = SpaceHarbor(self.win, self.x, self.y, self.getWidth(), 90, isSubWidget= False, parent = self, layer=9)

        # building buttons
        # buildings,resources
        # all possible buildings and resources
        self.resources = ["water", "energy", "food", "minerals", "technology", "city"]
        self.water_buildings = ["spring", "water treatment", "terra former"]
        self.energy_buildings = ["solar panel", "wind mill", "power plant"]
        self.food_buildings = ["farm", "ranch", "agriculture complex"]
        self.mineral_buildings = ["mine", "open pit", "mineral complex"]
        self.technology_buildings = ["university", "space harbor", "particle accelerator"]
        self.city_buildings = ["town", "city", "metropole"]
        self.population_buildings = ["town", "city", "metropole"]

        self.buildings = {"water": self.water_buildings,
                          "energy": self.energy_buildings,
                          "food": self.food_buildings,
                          "minerals": self.mineral_buildings,
                          "technology": self.technology_buildings,
                          "city": self.city_buildings
                          }

        self.buildings_list = self.water_buildings + self.energy_buildings + self.food_buildings + \
                              self.mineral_buildings + self.technology_buildings + self.city_buildings

        #todo fix this
        # self.planet_buttons = PlanetButtons(x, y +200, self)
        # self.planet_buttons.create_planet_button_array()

    def create_icons(self):
        self.image = images[pictures_path]["icons"]["clock.png"]
        self.image_size = self.image.get_size()
        self.clock_icon = Button(win=self.win,
            x=self.surface_rect.x + (self.spacing / 2),
            y=self.surface_rect.y + (self.spacing / 2),
            width=self.image_size[0],
            height=self.image_size[1],
            isSubWidget=False,
            image=self.image,
            tooltip="this is the time, don't waste it !",
            frame_color=self.frame_color,
            transparent=True,
            onClick=lambda: self.clock_slider.setValue(1),
            parent=self.parent, layer=self.layer
            )
        self.parent.icons.append(self.clock_icon)
        self.arrow_size = 15
        self.minus_arrow_button = Button(win=self.win,
            x=self.clock_icon.getX() + self.spacing * 2,
            y=self.clock_slider.getY() - self.clock_slider.getHeight() - 2,
            width=self.image_size[0],
            height=self.image_size[1],
            isSubWidget=False,
            image=pygame.transform.scale(
                images[pictures_path]["icons"]["arrow-left.png"], (self.arrow_size, self.arrow_size)),
            tooltip="decrease time",
            frame_color=self.frame_color,
            transparent=True,
            onClick=lambda: self.set_clockslider_value(-1),
            parent=self.parent, layer=self.layer
            )
        self.plus_arrow_button = Button(win=self.win,
            x=self.clock_icon.getX() + self.spacing * 2 + self.arrow_size,
            y=self.clock_slider.getY() - self.clock_slider.getHeight() - 2,
            width=self.image_size[0],
            height=self.image_size[1],
            isSubWidget=False,
            image=pygame.transform.scale(
                images[pictures_path]["icons"]["arrow-right.png"], (self.arrow_size, self.arrow_size)),
            tooltip="increase time",
            frame_color=self.frame_color,
            transparent=True,
            onClick=lambda: self.set_clockslider_value(+1),
            parent=self.parent, layer=self.layer
            )
        # planet selection buttons
        self.planet_minus_arrow_button = Button(win=self.win,
            x=self.getX() + self.spacing * 2,
            y=self.getY() + 40,
            width=self.image_size[0],
            height=self.image_size[1],
            isSubWidget=False,
            image=pygame.transform.scale(
                images[pictures_path]["icons"]["arrow-left.png"], (self.arrow_size, self.arrow_size)),
            tooltip="select planet",
            frame_color=self.frame_color,
            transparent=True,
            onClick=lambda: self.set_planet_selection(-1),
            parent=self.parent, layer=self.layer
            )
        self.planet_plus_arrow_button = Button(win=self.win,
            x=self.getX() + self.getWidth() - self.spacing * 2 - self.arrow_size,
            y=self.getY() + 40,
            width=self.image_size[0],
            height=self.image_size[1],
            isSubWidget=False,
            image=pygame.transform.scale(
                images[pictures_path]["icons"]["arrow-right.png"], (self.arrow_size, self.arrow_size)),
            tooltip="select planet",
            frame_color=self.frame_color,
            transparent=True,
            onClick=lambda: self.set_planet_selection(-1),
            parent=self.parent, layer=self.layer
            )
        # settings icon
        self.settings_icon = ImageButton(win=self.win,
            x=self.getX() - 25,
            y=self.clock_slider.getY(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(images[pictures_path]["icons"]["settings_40x40.png"], (25, 25)),
            tooltip="settings: WARNING! Closes Game if clicked, work in progress...",
            frame_color=colors.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: utils.Settings.main(surface=self.win))
        # ships
        # ship icon
        self.spacehunter_icon = ImageButton(win=self.win,
            x=self.settings_icon.getX() - 25,
            y=self.clock_slider.getY(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                images[pictures_path]["ships"]["spacehunter_30x30.png"], (25, 25)),
            tooltip="navigate to this ship, not working yet",
            frame_color=colors.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: Navigation.navigate_to(self.parent.navigation, "spacehunter"))
        self.info_icon = ImageButton(win=self.win,
            x=self.spacehunter_icon.getX() - 25,
            y=self.clock_slider.getY(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(images[pictures_path]["icons"]["info_30x30.png"], (25, 25)),
            tooltip="information about game controls",
            frame_color=colors.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: self.set_info_text())
        self.planet_editor_icon = ImageButton(win=self.win,
            x=self.info_icon.getX() - 50,
            y=self.clock_slider.getY(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                images[pictures_path]["planets"]["Zeta Bentauri_60x60.png"], (25, 25)),
            tooltip="open planet editor",
            frame_color=colors.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: PlanetEditor.main(surface=self.win))
        self.building_editor_icon = ImageButton(win=self.win,
            x=self.planet_editor_icon.getX() - 50,
            y=self.clock_slider.getY(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                images[pictures_path]["icons"]["building_icon.png"], (25, 25)),
            tooltip="open building editor",
            frame_color=colors.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: BuildingEditor.main(surface=self.win))
        self.orbit_icon = ImageButton(win=self.win,
            x=self.building_editor_icon.getX() - 50,
            y=self.clock_slider.getY(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                images[pictures_path]["icons"]["orbit_icon.png"], (25, 25)),
            tooltip="show orbit",
            frame_color=colors.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: self.set_global_variable("show_orbit", True))
        self.grid_icon = ImageButton(win=self.win,
            x=self.building_editor_icon.getX() - 50,
            y=self.clock_slider.getY(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                images[pictures_path]["icons"]["grid_icon.png"], (25, 25)),
            tooltip="show grid",
            frame_color=colors.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: self.set_global_variable("show_grid", True))

    def set_global_variable(self, key, value):
        if getattr(utils.Globals, key):
            setattr(utils.Globals, key, False)
        else:
            setattr(utils.Globals, key, True)

    def set_info_text(self):
        utils.Globals.app.info_panel.text = "Ship: rightclick to move to a planet, or reload the ship. \n\n ctrl and mouse click to navigate \n\n" \
                                             "numbers 1-9 to make layers visible or not \n\nb to open build menu"

    def set_clockslider_value(self, value):
        if value < 0:
            if self.clock_slider.min + 1 < self.clock_slider.getValue() - value:
                self.clock_slider.setValue(self.clock_slider.getValue() + value)
        elif value > 0:
            if self.clock_slider.max + 1 > self.clock_slider.getValue() + value:
                self.clock_slider.setValue(self.clock_slider.getValue() + value)

    def set_planet_selection(self, value):
        # if empty list: do nothing
        my_list = self.parent.explored_planets
        if not my_list:
            return

        # move list items forward
        if value == 1:
            first_item = my_list.pop(0)
            my_list.append(first_item)

        # move list items backward
        else:
            last_item = my_list.pop()
            my_list.insert(0, last_item)

        #set new selected planet
        self.parent.set_selected_planet(my_list[0])

    def show_planet_selection_buttons(self):
        if len(self.parent.explored_planets) > 1:
            self.planet_minus_arrow_button.show()
            self.planet_plus_arrow_button.show()
        else:
            self.planet_plus_arrow_button.hide()
            self.planet_minus_arrow_button.hide()

        # self.planet_buttons.show_overview_button()
        # for i in self.planet_buttons.possible_resources:
        #     self.planet_buttons.show_building_buttons(i)
    def listen(self, events):
        # DESTROY BUILDINGS
        # check for mouse collision with image
        for building_name, image_rect in self.singleton_buildings_images.items():
            if image_rect.collidepoint(pygame.mouse.get_pos()):
                utils.Globals.tooltip_text = f"Are you sure you want to destroy this {building_name}? You will probably not get anything back."
                # check for mouse click and destroy building
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.destroy_building(building_name)
            else:
                if utils.Globals.tooltip_text == f"Are you sure you want to destroy this {building_name}? You will probably not get anything back.":
                    utils.Globals.tooltip_text = ""

        # building slot upgrade and tooltip
        if self.parent.selected_planet:
            self.set_building_slot_tooltip_plus(events)
            self.set_building_slot_tooltip_minus(events)
            self.upgrade_building_slots(events)
            self.downgrade_building_slots(events)

        self.reset_building_slot_tooltip()

    def set_planet_building_display(self):
        """ sets text to the planet building texts based on buildings"""
        buildings = "None"
        if self.parent.selected_planet:
            buildings = ""
            for i in self.parent.selected_planet.buildings:
                buildings += i + ", "

            self.planet_buttons.show_building_buttons()

        return buildings

    def set_planet_production_display(self):
        """ sets text to the planet building texts based on production"""
        text = "None"
        if self.parent.selected_planet:
            text += ""

        return text

    def reposition(self):
        win = pygame.display.get_surface()
        width = win.get_width()

        # reposition
        self.surface_rect.x = width - self.surface.get_width()
        self.clock_icon._x = self.surface_rect.x + (self.spacing / 2)
        self.clock_slider._x = self.surface_rect.x + self.spacing_x + self.spacing_x
        self.planet_surface_rect.x = self.surface_rect.x
        self.minus_arrow_button._x = self.clock_icon.getX() + self.spacing * 2 + 3
        self.plus_arrow_button._x = self.clock_icon.getX() + self.spacing * 2 + self.arrow_size + 3
        self.planet_minus_arrow_button._x = self.surface_rect.x + self.spacing
        self.planet_plus_arrow_button._x = self.surface_rect.x + self.getWidth() - self.spacing * 2 - self.arrow_size
        self.settings_icon._x = self.clock_icon.getX() - self.spacing - self.settings_icon.getWidth()
        self.spacehunter_icon._x = self.settings_icon._x - self.spacing - self.settings_icon.getWidth()
        self.info_icon._x = self.spacehunter_icon._x - self.spacing - self.settings_icon.getWidth()
        self.planet_editor_icon._x = self.info_icon._x - self.spacing - self.settings_icon.getWidth()
        self.building_editor_icon._x = self.planet_editor_icon._x - self.spacing - self.settings_icon.getWidth()
        self.orbit_icon._x = self.building_editor_icon._x - self.spacing - self.settings_icon.getWidth()
        self.grid_icon._x = self.orbit_icon._x - self.spacing - self.settings_icon.getWidth()

    def destroy_building(self, b):
        print("destroy_building", b)
        self.parent.selected_planet.buildings.remove(b)
        self.parent.selected_planet.calculate_production()
        self.parent.selected_planet.calculate_population()
        self.parent.event_text = f"you destroyed one {b}! You will not get anything back from it! ... what a waste ..."
        sounds.play_sound(sounds.destroy_building)

    def update_time(self):
        self.year += 0.01 * self.time_factor * source.utils.Globals.game_speed
        utils.Globals.time_factor = self.time_factor

    def draw(self):
        """
        draws the ui elements
        """
        self.reposition()
        self.show_planet_selection_buttons()

        # TIME__________________________________________________________________________________________________________
        # draw surface and frame
        # self.win.blit(self.surface,self.surface_rect)
        self.update_time()

        # frame
        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, 1)
        self.win.blit(self.surface, self.surface_frame)

        # clock
        self.time_warp_text = self.font.render(str(self.clock_slider.getValue()) + "x", True, self.frame_color)
        self.win.blit(self.time_warp_text,
            (self.surface_rect.x + self.spacing_x, self.clock_icon._y + self.clock_icon.imageRect.height / 2))

        self.year_text = self.font.render("year: " + str(round(self.year, 2)), True, self.frame_color)
        self.win.blit(self.year_text, (self.surface_rect.x + self.spacing_x + self.spacing_x,self.clock_icon._y +
                                       self.clock_icon.getHeight() - self.year_text.get_height()))
        self.time_factor = self.clock_slider.getValue()

        # PLANET Image _________________________________________________________________________________________________
        # draw planet_surface and frame
        # self.win.blit(self.planet_surface, self.planet_surface_rect)
        self.planet_surface_frame = pygame.draw.rect(self.win, self.frame_color, self.planet_surface_rect, 1)
        self.win.blit(self.planet_surface, self.planet_surface_frame)

        # UI____________________________________________________________________________________________________________
        x = self.planet_surface_rect.x
        self.y = self.planet_surface_rect.y + self.spacing

        # planet text
        self.planet_text = drawText(self.win, self.parent.set_planet_name(), colors.frame_color,
            (x, self.y, self.getWidth(), self.planet_surface.get_height()), self.font, "center")

        x = self.planet_surface_rect.x + self.spacing
        self.y += self.spacing * 2

        if self.parent.selected_planet:
            # draw population text
            # population
            drawText(self.win, "population: " + str(int(self.parent.selected_planet.population)) + "/" + str(int(self.parent.selected_planet.population_limit)), self.frame_color, (
                x + self.spacing_x, self.y, self.getWidth(), 20), self.font, "left")
            image = images[pictures_path]["resources"]["city_25x25.png"]
            self.win.blit(image, (x, self.y))
            self.y += self.spacing * 3

            # draw background planet icon
            name = self.parent.selected_planet.name
            pic = name + "_150x150.png"

            if pic in images[pictures_path]["planets"].keys():
                self.planet_image = images[pictures_path]["planets"][pic]
            else:
                self.planet_image = pygame.transform.scale(self.parent.selected_planet.image.copy(), (150, 150))

            self.planet_image.set_alpha(128)
            self.win.blit(self.planet_image, self.planet_surface_rect.midtop)

            ############################################################################################################
            # buildings
            # __________________________________________________________________________________________________________

            # buildings:
            drawText(self.win, "buildings:  " + str(len(self.parent.selected_planet.buildings)) + "/" + str(int(self.parent.selected_planet.buildings_max)), self.frame_color, (
                x + self.spacing_x, self.y, self.getWidth(), 20), self.font, "left")
            self.y += self.spacing * 3

            # building slots:
            drawText(self.win, "building slots:  " + str(self.parent.selected_planet.building_slot_amount) + "/" + str(self.parent.selected_planet.building_slot_max_amount-1), self.frame_color, (
                x + self.spacing_x, self.y, self.getWidth(), 20), self.font, "left")

            # plus icon
            plus_image = pygame.transform.scale(images[pictures_path]["icons"]["plus_icon.png"], self.resource_image_size)

            # get rect for storage
            plus_image_rect = plus_image.get_rect()
            plus_image_rect.x = x
            plus_image_rect.y = self.y
            self.plus_button_image["plus_icon"] = plus_image_rect
            self.win.blit(plus_image, (x, self.y))

            self.y += self.spacing * 2

            # minus icon
            minus_image = pygame.transform.scale(
                images[pictures_path]["icons"]["minus_icon.png"], self.resource_image_size)
            # get rect for storage
            minus_image_rect = minus_image.get_rect()
            minus_image_rect.x = x
            minus_image_rect.y = self.y
            self.minus_button_image["minus_icon"] = minus_image_rect
            self.win.blit(minus_image, (x, self.y))

            self.y += self.spacing * 3

            # draw an image for every type of building built, plus a counter text
            self.singleton_buildings = []
            for sb in self.parent.selected_planet.buildings:
                if not sb in self.singleton_buildings:
                    self.singleton_buildings.append(sb)

            self.singleton_buildings_images = {}

            y = 0
            for b in self.singleton_buildings:
                # because of the dynamic creation of this panel, we cannot use a button, this would lead to memory leaks
                # and performance problems - so we just blit an image and get its rect as button surface

                image = pygame.transform.scale(images[pictures_path]["buildings"][b + "_25x25.png"],
                    self.resource_image_size)

                # get rect for storage
                image_rect = image.get_rect()
                image_rect.x = x
                image_rect.y = self.y + y

                # store it
                self.singleton_buildings_images[b] = image_rect

                # blit it
                self.win.blit(image, image_rect)

                # building count
                value = self.parent.selected_planet.buildings.count(b)
                text = self.font.render(b + ": " + str(value) + "x", True, self.frame_color)
                self.win.blit(text, (x + self.spacing_x, self.y + y))

                y += self.spacing * 2

            self.y += y + self.spacing

            # PRODUCTION________________________________________________________________________________________________
            # production label
            self.planet_building_text = drawText(self.win, "production: ", colors.frame_color, (
                self.planet_surface_rect.x,
                self.y, self.getWidth(),
                self.planet_surface.get_height()), self.font, "center")

            # production images and texts
            x = self.planet_surface_rect.x + self.spacing
            # self.y = self.planet_surface_rect.y + self.spacing * 15
            self.y += self.spacing * 3

            resources = self.parent.resources

            for r in resources:
                image = pygame.transform.scale(
                    images[pictures_path]["resources"][r + "_25x25.png"], self.resource_image_size)
                self.win.blit(image, (x, self.y))
                value = getattr(self.parent.selected_planet, "production_" + r)
                text = self.font.render(r + ": " + str(value), True, self.frame_color)
                self.win.blit(text, (x + self.spacing_x, self.y))

                self.y += self.spacing * 2

            self.y += self.spacing * 2

            # GLOBAL PRODUCTION_________________________________________________________________________________________
            # global production label
            self.planet_building_text = drawText(self.win, "global production: ", colors.frame_color, (
                self.planet_surface_rect.x,
                self.y, self.getWidth(),
                self.planet_surface.get_height()), self.font, "center")

            self.y += self.spacing * 3

            for r in resources:
                image = pygame.transform.scale(
                    images[pictures_path]["resources"][r + "_25x25.png"], self.resource_image_size)
                self.win.blit(image, (x, self.y))
                value = self.parent.player.production[r]
                text = self.font.render(r + ": " + str(value), True, self.frame_color)
                self.win.blit(text, (x + self.spacing_x, self.y))

                self.y += self.spacing * 2

        # adjust frame size_y
        self.planet_surface_rect.__setattr__("height", self.y - self.spacing * 3)
