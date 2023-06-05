import random
from os.path import isfile, join

import source.Globals
import source.Images
from source.Globals import *

from source.AppHelper import UIHelper
from source.BackgroundImage import BackgroundImage
from source.BuildingPanel import BuildingPanel
from source.Button import Button, ButtonArray
from source.CollectableItem import CollectableItem
from source.EventPanel import EventPanel
from source.FogOfWar import FogOfWar
from source.Globals import moveable, WIDTH, HEIGHT, pictures_path
from source.Icon import Icon
from source.InfoPanel import InfoPanel
from source.Levels import level_dict
from source.Navigation import Navigation
from source.Planet import Planet
from source.Player import Player
from source.Ship import Ship
from source.Ships import *
from source.ToolTip import ToolTip
from source.UniverseBackground import Universe
from source.config import planet_positions, prices, production
from source.texts import planet_texts
from source.paning_and_zooming import PanZoomHandler


class SceneParams:
    def __init__(self):
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

        # buildings,resources
        # all possible buildings and resources
        self.resources = ["water", "energy", "food", "minerals", "technology", "city"]
        self.water_buildings = ["spring", "water treatment", "terra former"]
        self.energy_buildings = ["solar panel", "wind mill", "power plant"]
        self.food_buildings = ["farm", "ranch", "agriculture complex"]
        self.mineral_buildings = ["mine", "open pit", "mineral complex"]
        self.technology_buildings = ["university", "space harbor", "particle accelerator"]
        self.city_buildings = ["town", "city", "metropole"]

        self.buildings = {"water": self.water_buildings,
                          "energy": self.energy_buildings,
                          "food": self.food_buildings,
                          "minerals": self.mineral_buildings,
                          "technology": self.technology_buildings,
                          "city": self.city_buildings
                          }

        self.buildings_list = self.water_buildings + self.energy_buildings + self.food_buildings + \
                              self.mineral_buildings + self.technology_buildings + self.city_buildings

        self.building_widget_list = []

        # prices/production
        self.prices = prices
        self.production = production


class SceneBuilder(SceneParams):
    def __init__(self, width, height):
        """
        creates all scene elemts like ships and planets, background , fog of war
        :param width:
        :param height:
        """

        SceneParams.__init__(self)
        # UI Helper
        self.ui_helper = UIHelper(self)
        self.level = 1
        self.game_objects = []
        self.planets = []
        self.collectables = []

        # background
        self.create_background()

        # fog of war
        self.create_fog_of_war()

        # planets
        self.planet_buttons = []
        self.create_planets(self.level)
        self.create_artefacts()

        # ship
        self.ships = []
        win = pygame.display.get_surface()
        win_width = win.get_width()
        win_height = win.get_height()
        center_x = win_width / 2
        center_y = win_height / 2
        spacing = 100

        self.ship = None
        self.create_ship("spaceship_30x30.png", center_x, center_y + 300)
        self.create_ship("cargoloader_30x30.png", center_x - spacing, center_y + 300)
        self.create_ship("spacehunter_30x30.png", center_x + spacing, center_y + 300)

    def create_fog_of_war(self):
        self.fog_of_war = FogOfWar(source.Globals.win, 0, 0, source.Globals.scene_width, source.Globals.scene_height, False, layer=2)

    def create_background(self):
        self.background_image = BackgroundImage(source.Globals.win,
            x=0,
            y=0,
            width=WIDTH,
            height=HEIGHT,
            isSubWidget=False,
            image=source.Images.images[pictures_path]["textures"]["bg.png"].convert(),
            layer=0, property="background")

        self.universe = Universe(source.Globals.win, 0, 0, source.Globals.scene_width, source.Globals.scene_height, isSubWidget=False, layer=3)

    def create_ship(self, name, x, y):
        """ creates a ship from the image name like: schiff1_30x30"""
        size_x, size_y = map(int, name.split("_")[1].split(".")[0].split("x"))
        name = name.split("_")[0]
        class_ = name[0].upper() + name[1:]

        if class_ == "Spaceship":
            ship = Spaceship(source.Globals.win, x=x, y=y, width=size_x, height=size_y,
                image=source.Globals.images[pictures_path]["ships"][name + "_30x30.png"],

                textColour=source.Globals.colors.frame_color,
                moveable=False,
                wait=1.0,
                name=name,
                parent=self,
                ui_parent=None,  # self.background,
                tooltip="this is your spaceship: " + name,
                textVAlign="over_the_top",
                selection_image=source.Globals.images[pictures_path]["icons"]["selection_150x150.png"],
                layer=8)

            self.ships.append(ship)

        if class_ == "Spacehunter":
            ship = Spacehunter(source.Globals.win, x=x, y=y, width=size_x, height=size_y,
                image=source.Globals.images[pictures_path]["ships"][name + "_30x30.png"],

                textColour=source.Globals.colors.frame_color,
                moveable=False,
                wait=1.0,
                name=name,
                parent=self,
                ui_parent=None,  # self.background,
                tooltip="this is your spaceship: " + name,
                textVAlign="over_the_top",
                selection_image=source.Globals.images[pictures_path]["icons"]["selection_150x150.png"],
                layer=8)

            self.ships.append(ship)

        if class_ == "Cargoloader":
            ship = Cargoloader(source.Globals.win, x=x, y=y, width=size_x + 20, height=size_y + 20,
                image=source.Globals.images[pictures_path]["ships"][name + "_30x30.png"],

                textColour=source.Globals.colors.frame_color,
                moveable=False,
                wait=1.0,
                name=name,
                parent=self,
                ui_parent=None,  # self.background,
                tooltip="this is your spaceship: " + name,
                textVAlign="over_the_top",
                selection_image=source.Globals.images[pictures_path]["icons"]["selection_150x150.png"],
                layer=8)

            self.ships.append(ship)

    def create_planets_old(self, level):
        """
        creates the ppanets based on the level from Lovels (level_dict)
        :param level:
        :return:
        """
        for planetname, planetparams in level_dict[level].items():
            # print (planetname,planetparams)
            width = int(planetparams["image_name"].split("_")[1].split("x")[0])
            height = int(planetparams["image_name"].split("_")[1].split("x")[1].split(".png")[0])

            # dirty hack to fix the position
            planetparams["x"] = planet_positions[planetname][0]
            planetparams["y"] = planet_positions[planetname][1]
            planetparams["position"] = planet_positions[planetname]

            planet_button = Planet(win=source.Globals.win,
                x=int(planetparams["x"]),
                y=int(planetparams["y"]),
                width=width,
                height=height,
                isSubWidget=False,
                image=source.Globals.images[pictures_path]["planets"][planetparams["image_name"]],
                transparent=True,

                info_text=planet_texts[planetparams["name"]],
                text=planetparams["name"],
                textColour=source.Globals.colors.frame_color,
                property="planet",
                name=planetparams["name"],
                parent=self,
                tooltip="send your ship to explore the planet!",
                possible_resources=planetparams["possible_resources"],
                moveable=moveable,
                hover_image=source.Globals.images[pictures_path]["icons"]["selection_150x150.png"],
                textVAlign="below_the_bottom",
                layer=3)
            self.planet_buttons.append(planet_button)

        # set orbit_object
        sun = [i for i in self.planets if i.name == "Sun"][0]
        for i in self.planets:
            if not i == sun:
                i.set_orbit_object(sun)

    def create_planets(self, level):
        """
        creates the ppanets based on the level from Lovels (level_dict)
        :param level:
        :return:
        """
        dirpath = os.path.dirname(os.path.realpath(__file__))
        database_path = os.path.split(dirpath)[0] + os.sep + "database" + os.sep
        level_path = database_path + "levels" + os.sep + "level" + str(level) + os.sep + "planets" + os.sep
        file_names = [f for f in os.listdir(level_path) if isfile(join(level_path, f))]

        for file_name in file_names:
            # planet dict
            planet = source.SaveLoad.load_file("levels" + os.sep + "level" + str(level) + os.sep + "planets" + os.sep + file_name)

            # get width and height from image
            width = int(planet["image_name_small"].split("_")[1].split("x")[0])
            height = int(planet["image_name_small"].split("_")[1].split("x")[1].split(".png")[0])

            planet_button = Planet(win=source.Globals.win,
                x=int(planet["x"]),
                y=int(planet["y"]),
                width=width,
                height=height,
                isSubWidget=False,
                image=source.Globals.images[pictures_path]["planets"][planet["image_name_small"]],
                transparent=True,
                info_text=planet["info_text"],
                text=planet["name"],
                textColour=source.Globals.colors.frame_color,
                property="planet",
                name=planet["name"],
                parent=self,
                tooltip="send your ship to explore the planet!",
                possible_resources=eval(str(planet["possible_resources"]).replace("'", '"')),
                moveable=moveable,
                hover_image=source.Globals.images[pictures_path]["icons"]["selection_150x150.png"],
                textVAlign="below_the_bottom",
                layer=3)

            self.planet_buttons.append(planet_button)

        # set orbit_object
        sun = [i for i in self.planets if i.name == "Sun"][0]
        for i in self.planets:
            if not i == sun:
                i.set_orbit_object(sun)

    def create_artefacts(self):  # self not working yet
        w = WIDTH
        h = HEIGHT
        buffer = 100
        image = source.Globals.images[pictures_path]["artefacts"]["artefact1_60x31.png"]
        artefact = CollectableItem(source.Globals.win,
            random.randint(buffer, WIDTH - buffer), random.randint(buffer, HEIGHT - buffer), 50, 50,
            isSubWidget=False,
            image=image,
            layer=4,
            transparent=True,
            tooltip="...maybe an alien artefact ? ...we don't now what it is ! it might be dangerous --- but maybe useful !?",
            moveable=True,

            energy=100,
            minerals=1000,
            parent=self, )


class UIBuilder(SceneBuilder):
    """this creates all UI Elements:
    use SceneBuilder for Scene Elements like ships planets ect

    it also starts the game loop"""

    def __init__(self, width, height):
        # self.main_menu = main()

        SceneBuilder.__init__(self, width, height)

        self.pan_zoom_handler = PanZoomHandler(
            source.Globals.win, source.Globals.WIDTH, source.Globals.HEIGHT, source.Globals.scene_width,
            source.Globals.scene_height, parent=self)

        # self.building_editor = BuildingEditor()
        self.clock = pygame.time.Clock()
        self.navigation = Navigation(source.Globals.win, 0, 0, width, height, isSubWidget=False, scene_width=source.Globals.scene_width, scene_height=source.Globals.scene_height,
            parent=self, layer=10)
        self.ui_helper = UIHelper(self)
        self.win = source.Globals.win
        # self.box_selection = SelectionRect(self.win, pygame.mouse.get_pos())

        # set args
        self.width = width
        self.height = height
        self.icons = []
        self.selected_planet = None
        self.build_menu_visible = False
        self.build_menu_widgets = []
        self.build_menu_widgets_buildings = {"energy": [],
                                             "food": [],
                                             "minerals": [],
                                             "water": [],
                                             "city": [],
                                             "technology": []
                                             }

        # event text
        self.event_text_font = pygame.font.SysFont(None, 30)
        prefix = "GPT-1357: "
        self.event_text = "hi, i am George Peter Theodor the 1357th, or short: GPT-1357." \
                          "i am an artificial intelligence to help mankind out of their mess...maybe the only intelligent beeing " \
                          "on this ship. my advice: find a new world for the last dudes from earth!"
        self.event_display_text = prefix + self.event_text

        # player
        self.create_player()

        # building_panel
        self.create_building_panel()

        # tooltip
        self.create_tooltip()

        # Info_panel
        self.info_panel = InfoPanel(self.win, x=0, y=10, width=200, height=300, isSubWidget=False, parent=self, layer=9)

        # icons
        self.create_icons()

        # build menu
        self.build_menu = None
        self.create_build_menu()
        self.close_build_menu()

        # navigation

        # event panel
        self.create_event_panel()

        # make self global, maybe we need that
        source.Globals.app = self

        # drag
        # self.dragables = self.planets + self.ships
        # self.dragables.append(self.bg)
        # self.dragables.append(self.fog_of_war)
        # settings window
        # Settings.main()
        #
        # self.settings = Settings.main_menu
        # self.settings.disable()

        # run game loop
        self.run = 1
        self.loop()

    def create_player(self):
        self.player = Player(name="zork",
            color=pygame.Color('red'),
            energy=1000,
            food=1000,
            minerals=1000,
            water=1000,
            technology=1000,
            city=0,
            clock=0
            )

    def create_event_panel(self):
        self.event_panel = EventPanel(win=self.win, x=300, y=200, width=900, height=600, center=True, parent=self, layer=9)

    def create_tooltip(self):
        # tooltip
        self.tooltip_instance = ToolTip(surface=self.win,
            x=100,
            y=100,
            width=100,
            height=100,
            color=pygame.colordict.THECOLORS["black"],
            text_color=pygame.colordict.THECOLORS["darkslategray1"],
            isSubWidget=False, parent=self, layer=4)

    def create_building_panel(self):
        # building_panel
        size_x = 250
        size_y = 35
        spacing = 10
        self.building_panel = BuildingPanel(self.win,
            x=self.width - size_x,
            y=spacing,
            width=size_x - spacing,
            height=size_y,
            isSubWidget=False,
            size_x=size_x,
            size_y=size_y,
            spacing=spacing,
            parent=self,
            layer=9)

    def draw(self):
        # background
        # self.bg = pygame.transform.scale(self.bg, (self.ui_helper.width, self.ui_helper.height))
        pass

    def create_icons(self):
        """
        creates the icons used for displaying the resources on top of the screen
        :return:
        """
        start_x = 250
        spacing = 150
        pos_x = start_x
        pos_y = 15

        water_icon = Icon(win=self.win,
            x=pos_x,
            y=pos_y,
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=source.Globals.images[pictures_path]["resources"]["water_25x25.png"],
            key="water",
            tooltip="water is good to drink and for washing aswell",
            frame_color=source.Globals.colors.frame_color,
            moveable=False,
            include_text=True,
            layer=9)
        pos_x += spacing

        energy_icon = Icon(win=self.win,
            x=pos_x,
            y=pos_y,
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=source.Globals.images[pictures_path]["resources"]["energy_25x25.png"],
            key="energy",
            tooltip="energy is needed for almost everything",
            frame_color=source.Globals.colors.frame_color,
            moveable=False,
            include_text=True, layer=9)
        pos_x += spacing

        food_icon = Icon(win=self.win,
            x=pos_x,
            y=pos_y,
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=source.Globals.images[pictures_path]["resources"]["food_25x25.png"],
            key="food",
            tooltip="this is food, you want to eat!!! Don't you?!??",
            frame_color=source.Globals.colors.frame_color,
            moveable=False,
            include_text=True, layer=9)
        pos_x += spacing

        minerals_icon = Icon(win=self.win,
            x=pos_x,
            y=pos_y,
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=source.Globals.images[pictures_path]["resources"]["minerals_25x25.png"],
            key="minerals",
            tooltip="some of the minerals look really nice in the sun!",
            frame_color=source.Globals.colors.frame_color,
            moveable=False,
            include_text=True, layer=9)

        pos_x += spacing

        technology_icon = Icon(win=self.win,
            x=pos_x,
            y=pos_y,
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=source.Globals.images[pictures_path]["resources"]["technology_25x25.png"],
            key="technology",
            tooltip="technology is bad! but we need some things to build and evolve technology",
            frame_color=source.Globals.colors.frame_color,
            moveable=False,
            include_text=True, layer=9)

        pos_x += spacing

        city_icon = Icon(win=self.win,
            x=pos_x,
            y=pos_y,
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=source.Globals.images[pictures_path]["resources"]["city_25x25.png"],
            key="city",
            tooltip="population; produce food and water to make it grow!",
            frame_color=source.Globals.colors.frame_color,
            moveable=False,
            include_text=True, layer=9)

        pos_x = self.width - 130

    def create_build_menu(self):
        """
        this monster creates the buildmenu; an overview over all buildable things
        :return:
        """
        # width (relative dynamic: use colon_size_x to adjust
        x = 0
        colon_size_x = 466
        start_x = 0 - colon_size_x / 2

        # height (dynamic)
        build_menu_height = 702  # 732-30 muss durch 3 teilbar sein
        start_y = 60
        y = 0
        row_size_y = 30

        # font sizes
        price_font_size = 20

        # text colors
        price_color_cost = pygame.color.THECOLORS["orange"]
        price_color_win = pygame.color.THECOLORS["green"]

        # image sizes
        price_image_size = (16, 16)

        # colons
        colons = ["resource", "building", "price", "production"]

        # first row(titles)
        for colon in colons:
            if colon == "resource":
                button = Button(win=self.win, x=int(x + start_x + colon_size_x / 2), y=start_y,
                    width=int(colon_size_x / 2),
                    height=row_size_y, text=colon + ": ", border_thickness=1, layer=9)
            elif colon == "building":
                button = Button(win=self.win, x=int(x + start_x + colon_size_x), y=start_y, width=int(colon_size_x / 2),
                    height=row_size_y, text=colon + ": ", border_thickness=1, layer=9)
            elif colon == "price":
                button = Button(win=self.win, x=int(x + start_x + colon_size_x + colon_size_x / 2), y=start_y,
                    width=colon_size_x, height=row_size_y, text=colon + ": ", border_thickness=1, layer=9)
            elif colon == "production":
                button = Button(win=self.win, x=int(x + start_x + colon_size_x + colon_size_x / 2 + colon_size_x),
                    y=start_y,
                    width=colon_size_x, height=row_size_y, text=colon + ": ", border_thickness=1, layer=9)

            button.disable()
            self.build_menu_widgets.append(button)

        # next row
        y += start_y + row_size_y
        y_hold = y
        x = start_x
        row_size_y = build_menu_height / 6  # this might be wrong

        # resource icons (first colon)
        for r in self.resources:
            colon_name = Button(win=self.win, x=x + colon_size_x / 2, y=y, width=colon_size_x / 2,
                height=int(row_size_y),
                text=r + ": ",
                image=pygame.transform.scale(source.Globals.images[pictures_path]["resources"][r + "_25x25.png"],
                    (50, 50)),
                borderThickness=1, imageHAlign="left", textHAlign="right", layer=9)

            y += row_size_y
            colon_name.disable()
            self.build_menu_widgets.append(colon_name)

        # hold y for later use, remove "resource", no need anymore, only building, price and production is needed
        y = y_hold
        x += colon_size_x
        colons.remove("resource")

        # dynamic creation of all widgets (resource, building, price, production) with arrays for every row
        ry = 0
        for r in self.resources:
            for colon in colons:
                if colon == "building":
                    # print ("build_menu_ ", r, self.buildings[r][0])
                    buildings_array = ButtonArray(win=self.win, x=x, y=y + ry,
                        width=colon_size_x / 2,
                        height=int(row_size_y),
                        shape=(1, 3),
                        border=1,
                        texts=self.buildings[r],
                        images=[source.Globals.images[pictures_path]["buildings"][
                                    self.buildings[r][0] + "_25x25.png"],
                                source.Globals.images[pictures_path]["buildings"][
                                    self.buildings[r][1] + "_25x25.png"],
                                source.Globals.images[pictures_path]["buildings"][
                                    self.buildings[r][2] + "_25x25.png"]],

                        textHAligns=("right", "right", "right"),
                        imageHAligns=("left", "left", "left"),
                        bottomBorder=0,
                        names=[self.buildings[r][0], self.buildings[r][1],
                               self.buildings[r][2]],
                        tooltips=["not set", "not set", "not set"],
                        parents=[self, self, self],
                        propertys=[r, r, r],
                        layers=[9, 9, 9])
                    # onClicks=[lambda: self.build(self.buildings[r][0]),
                    #           lambda: self.build(self.buildings[r][1]),
                    #           lambda: self.build(self.buildings[r][2])])
                    self.build_menu_widgets.append(buildings_array)

                    for button in buildings_array.getButtons():
                        self.build_menu_widgets_buildings[r].append(button)

                if colon == "price":
                    # set the colors based on the values: orange for negative values, green for positive values
                    price_colors = [0, 0, 0, 0]
                    for i in self.buildings[r]:
                        if self.prices[i]["water"] > 0:
                            price_colors[0] = price_color_cost
                        if self.prices[i]["energy"] > 0:
                            price_colors[1] = price_color_cost
                        if self.prices[i]["food"] > 0:
                            price_colors[2] = price_color_cost
                        if self.prices[i]["minerals"] > 0:
                            price_colors[3] = price_color_cost

                        price_array = ButtonArray(win=self.win, x=x + colon_size_x - colon_size_x / 2, y=y + ry,
                            width=colon_size_x,
                            height=int(row_size_y / 3),
                            shape=(4, 1), border=1,
                            texts=[str(self.prices[i]["water"]),
                                   str(self.prices[i]["energy"]),
                                   str(self.prices[i]["food"]),
                                   str(self.prices[i]["minerals"])],
                            fontSizes=[price_font_size, price_font_size, price_font_size,
                                       price_font_size],

                            images=[pygame.transform.scale(
                                source.Globals.images[pictures_path]["resources"]["water" + "_25x25.png"],
                                price_image_size),
                                pygame.transform.scale(
                                    source.Globals.images[pictures_path]["resources"][
                                        "energy" + "_25x25.png"], price_image_size),
                                pygame.transform.scale(
                                    source.Globals.images[pictures_path]["resources"][
                                        "food" + "_25x25.png"], price_image_size),
                                pygame.transform.scale(
                                    source.Globals.images[pictures_path]["resources"][
                                        "minerals" + "_25x25.png"], price_image_size)],

                            onClicks=(lambda: print(1), lambda: print(2), lambda: print(3),
                                      lambda: print(4)),

                            imageHAligns=("left", "left", "left", "left"),
                            textColours=price_colors,
                            layers=[9, 9, 9, 9])

                        self.build_menu_widgets.append(price_array)
                        for pb in price_array.getButtons():  pb.disable()
                        y += row_size_y / 3
                    y -= row_size_y

                if colon == "production":
                    price_colors = [0, 0, 0, 0]
                    for i in self.buildings[r]:
                        if self.production[i]["water"] > 0:
                            price_colors[0] = price_color_win
                        if self.production[i]["energy"] > 0:
                            price_colors[1] = price_color_win
                        if self.production[i]["food"] > 0:
                            price_colors[2] = price_color_win
                        if self.production[i]["minerals"] > 0:
                            price_colors[3] = price_color_win

                        if self.production[i]["water"] < 0:
                            price_colors[0] = price_color_cost
                        if self.production[i]["energy"] < 0:
                            price_colors[1] = price_color_cost
                        if self.production[i]["food"] < 0:
                            price_colors[2] = price_color_cost
                        if self.production[i]["minerals"] < 0:
                            price_colors[3] = price_color_cost

                        production_array = ButtonArray(win=self.win,
                            x=x + colon_size_x + colon_size_x - colon_size_x / 2, y=y + ry,
                            width=colon_size_x,
                            height=int(row_size_y / 3),
                            shape=(4, 1), border=1,
                            texts=[str(self.production[i]["water"]),
                                   str(self.production[i]["energy"]),
                                   str(self.production[i]["food"]),
                                   str(self.production[i]["minerals"])],
                            fontSizes=[price_font_size, price_font_size, price_font_size,
                                       price_font_size],

                            images=[pygame.transform.scale(
                                source.Globals.images[pictures_path]["resources"][
                                    "water" + "_25x25.png"], price_image_size),
                                pygame.transform.scale(
                                    source.Globals.images[pictures_path]["resources"][
                                        "energy" + "_25x25.png"], price_image_size),
                                pygame.transform.scale(
                                    source.Globals.images[pictures_path]["resources"][
                                        "food" + "_25x25.png"], price_image_size),
                                pygame.transform.scale(
                                    source.Globals.images[pictures_path]["resources"][
                                        "minerals" + "_25x25.png"], price_image_size)],
                            onClicks=(lambda: print(1), lambda: print(2), lambda: print(3),
                                      lambda: print(4)),

                            imageHAligns=("left", "left", "left", "left"),
                            textColours=price_colors,
                            layers=[9, 9, 9, 9]
                            )

                        self.build_menu_widgets.append(production_array)
                        for i in production_array.getButtons():  i.disable()
                        y += row_size_y / 3

                    # reset y for next colon
                    y -= row_size_y

            # set ry (resource position y ) for next resource
            ry += row_size_y
