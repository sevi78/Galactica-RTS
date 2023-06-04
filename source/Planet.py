import time

import pygame
from pygame import Vector2
from pygame_widgets.mouse import Mouse, MouseState

import source.Globals
import source.config
from source.AppHelper import limit_positions
from source.Button import Button, ButtonArray, ImageButton
from source.Globals import pictures_path
from source.Levels import level_dict
from source.Sounds import sounds
from source.config import production


class PlanetConfig:
    def __init__(self,**kwargs):

        self.name = kwargs.get("name")
        self.x = source.config.planet_positions[self.name][0]  # x
        self.y = source.config.planet_positions[self.name][1]  # y
        self.info_text = kwargs.get("info_text")
        self.population_grow = 0.0
        self.alien_population = 0
        self.buildings_max = 10
        self.building_slot_amount = 3
        self.specials = None
        self.type = source.texts.planet_texts[self.name].split("\n")[3].split(": ")[1]
        self.possible_resources = kwargs.get("possible_resources")
        self.image_name_small = level_dict[1][self.name]["image_name"]
        self.image_name_big = self.name + "_150x150.png"

        # print ("line:" , source.texts.planet_texts[self.name].split("\n"))
        #
        # print ("PlanetConfig", self.__dict__)

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
        :return:
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
        :return:
        """
        for i in self.overview_buttons:
            if self.explored:
                if not self.name == "Sun":
                    i.show()
            else:
                i.hide()

    def set_building_button_tooltip(self,i ):
        """
        creates tooltops for the buttons
        :param i:
        :return:
        """
        return_list = []
        price_list = []
        production_list =[]

        # prices
        text = ""
        for building in self.parent.buildings[i.name]:
            if building[0] == "a":
                text = "to build an " + building + " you need: "
            else:
                text = "to build a " + building + " you need: "

            for key, value in source.config.prices[building].items():
                if value > 0:
                    text += key + ": " + str(value) + ", "
            text = text[:-2]

            price_list.append(text)

        # production
        text = ""
        for building in self.parent.buildings[i.name]:
            # population
            if building in self.population_buildings:
                text = ". a " + building + " increases the planets population limit by " + str(self.population_buildings_values[building]) + "  "

            elif building[0] == "a":
                text = " . an " + building + " will produce: "
            else:
                text = " . a " + building + " will produce: "

            for key, value in source.config.production[building].items():
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

    def create_building_slots(self):
        #print ("create_building_slots!")
        """
        creates the ui elements for the planet:
        buildong icons, overview icons, buttons ect
        :return:
        """
        self.building_buttons = {}
        self.building_buttons_list = []
        self.overview_buttons = []
        slot_image_size = 25
        x = self._x
        y = self._y - self.getHeight()/2

        # # open build menu
        # self.button_build_menu_open = Button(self.win, x-slot_image_size,y,slot_image_size, slot_image_size,isSubWidget=False,
        #                                     image= source.Globals.images[pictures_path]["icons"]["build.png"],
        #                                     onClick=lambda: self.parent.open_build_menu()  )
        # self.button_build_menu_open.hide()

        #resource icons
        images = [pygame.transform.scale(source.Globals.images[pictures_path]["resources"][i + "_25x25.png"],(slot_image_size,slot_image_size))
                  for i in self.possible_resources]

        # ["not set", "not set", "not set","not set", "not set","not set"]
        self.building_slots = ButtonArray(self.win,
                                          x= x,
                                          y= y,
                                          width=len(self.possible_resources)*slot_image_size,
                                          height=slot_image_size+1,
                                          shape =(len(self.possible_resources),1),border=1,bottomBorder=0,rightBorder=0,leftBorder=0,topBorder=0,
                                          images=images,
                                          borderThickness=2,inactiveBorderColours=[source.Globals.colors.frame_color for i in range(6) ],

                                          tooltips=self.possible_resources,
                                          onClicks=(
                                          lambda: self.show_building_buttons(self.possible_resources[0]),
                                          lambda: self.show_building_buttons(self.possible_resources[1]),
                                          lambda: self.show_building_buttons(self.possible_resources[2]),
                                          lambda: self.show_building_buttons(self.possible_resources[3]),
                                          lambda: self.show_building_buttons(self.possible_resources[4]),
                                          lambda: self.show_building_buttons(self.possible_resources[5])
                                              ),
                                          parents=[self, self, self, self,self, self],
                                          ui_parents=[self, self, self, self,self, self],
                                          names= self.possible_resources,
                                          layers= [9,9,9,9,9,9],
                                          inactiveColours=[source.Globals.colors.background_color for i in range(6) ],
                                          borderColours=[source.Globals.colors.frame_color for i in range(6) ])#[4,4,4,4,4,4])#[1,1,1,1,1,1]


        # building buttons
        for i in self.building_slots.getButtons():
            images = [source.Globals.images[pictures_path]["buildings"][self.parent.buildings[i.name][0] + "_25x25.png"],
                      source.Globals.images[pictures_path]["buildings"][self.parent.buildings[i.name][1] + "_25x25.png"],
                      source.Globals.images[pictures_path]["buildings"][self.parent.buildings[i.name][2] + "_25x25.png"]]

            scaled_images = [pygame.transform.scale(image,(slot_image_size,slot_image_size)) for image in images]
            info_texts = [source.config.create_info_panel_building_text()[self.parent.buildings[i.name][0]],
                          source.config.create_info_panel_building_text()[self.parent.buildings[i.name][1]],
                          source.config.create_info_panel_building_text()[self.parent.buildings[i.name][2]]]

            # ["not set", "not set", "not set"]
            building_buttons = ButtonArray( self.win,
                                            x=i.getX(),
                                            y=y-slot_image_size-slot_image_size-i.getHeight(),
                                            width=slot_image_size+1,
                                            height=3*slot_image_size,
                                            shape =(1,3),
                                            border=1,bottomBorder=0,rightBorder=0,leftBorder=0,topBorder=0,
                                            images= scaled_images,
                                            borderThickness=0,
                                            texts= [self.parent.buildings[i.name][0], self.parent.buildings[i.name][1], self.parent.buildings[i.name][2]],
                                            tooltips=self.set_building_button_tooltip(i),

                                            parents=[self, self, self],
                                            ui_parents=[self, self, self],
                                            names= self.parent.buildings[i.name],
                                            textColours= [(0,0,0), (0,0,0), (0,0,0)],
                                            fontSizes= [0,0,0],
                                            info_texts= info_texts,
                                            layers=[9,9,9,9,9,9]#[4,4,4,4,4,4] #[1, 1, 1, 1, 1, 1]
                                            )

            # hide initially
            building_buttons.hide()
            self.building_slots.hide()

            # register
            self.building_buttons[i.name] = building_buttons
            self.building_buttons_list.append(building_buttons)

        # thumpsup button
        self.thumpsup_button_size = (20,20)
        self.thumpsup_button = ImageButton(self.win,
            x=self._x - slot_image_size ,
            y=self.building_slots.getY(),
            width=self.thumpsup_button_size[0],
            height=self.thumpsup_button_size[1],
            isSubWidget=False,
            onClick=lambda: print("no function"),
            transparent=True,
            image_hover_surface_alpha=255,
            parent=self.parent,
            ui_parent=self,
            tooltip="indicates whether the production is in plus ",
            image=pygame.transform.flip(pygame.transform.scale(source.Globals.images[pictures_path]["icons"]["thumps_up.png"],self.thumpsup_button_size),True,False),
            layer= 9)

        self.overview_buttons.append(self.thumpsup_button)

        # smiley
        self.smiley_button_size = (24, 24)

        self.smiley_button = ImageButton(self.win,
            x=self._x - slot_image_size * 2,
            y=self.building_slots.getY(),
            width=self.smiley_button_size[0],
            height=self.smiley_button_size[1],
            isSubWidget=False,
            onClick=lambda: print("no function"),
            transparent=True,
            image_hover_surface_alpha=255,
            parent=self.parent,
            ui_parent =self,
            tooltip="indicates the satisfaction of the population", image=source.Globals.images[pictures_path]["icons"]["smile.png"],
            layer=9
            )
        self.smiley_button.hide()
        self.thumpsup_button.hide()
        self.overview_buttons.append(self.smiley_button)



class Planet(Button, PlanetButtons):
    """ this is the planet class, inherited from:
    from pygame_widgets.button import Button
    """
    def __init__(self, win, x, y, width, height,isSubWidget, **kwargs):
        # inherit the base class
        Button.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        PlanetButtons.__init__(self)


        # setup variables
        self.fog_of_war_radius = self.getWidth() * 1.5
        self.layer = kwargs.get("layer", 1)
        self.name = kwargs.get("name")
        self.parent = kwargs.get("parent")
        self.planet_image = kwargs.get("image")
        self.image = kwargs.get("image")
        self.imageRect = self.image.get_rect()
        self.hover_image = pygame.transform.scale(kwargs.get("hover_image"), (self.getWidth(), self.getHeight()))
        self.hover_image.set_alpha(200)

        self.property = "planet"
        self.moveable = kwargs.get("moveable", False)
        self.orbit_angle = 0
        self.orbit_distance = 0
        self.orbit_object = kwargs.get("orbit_object", None)
        self.enable_orbit = False
        self.offset = Vector2(200, 0)
        self.orbit_speed = 0.002

        self.win = win
        self.x = source.config.planet_positions[self.name][0]#x
        self.y = source.config.planet_positions[self.name][1]#y

        self.size_x = width
        self.size_y = height
        self.start_time = time.time()
        self.wait = kwargs.get("wait", 1.0)

        self.pos = Vector2(self.getX(), self.getY())
        self.selected = False
        self.center = (self.getX() + self.getWidth() / 2, self.getY() + self.getHeight() / 2)
        # self.rect = self.imageRect
        self.inactiveColour = kwargs.get("inactiveColour", (0, 0, 0))
        self.hoverColour = kwargs.get("hoverColour", (150, 0, 0))
        self.pressedColour = kwargs.get("pressedColour", (0, 200, 20))
        self.radius = 5
        self.onClick = lambda: self.execute( kwargs)
        self.text.set_alpha(0)
        self.button_build_menu_open = None
        self.on_hover = False
        self.on_hover_release = False

        # setup Game variables
        self.info_text = kwargs.get("info_text")
        self.resources = {"energy":0, "food":0, "minerals":0, "water":0}
        self.explored = False
        self.just_explored = False
        self.buildings = []
        self.buildings_max = 10
        self.population = 0.0
        self.population_limit = 0.0
        self.population_grow = 0.0
        self.alien_population = 0
        self.building_slot_amount = 3
        self.building_cue = 0
        self.building_slots = None
        self.specials = None
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

        #population buildings
        self.population_buildings = ["town", "city", "metropole"]
        self.population_buildings_values = {"town": 1000, "city": 10000, "metropole": 100000}

        # create building slots
        self.building_buttons_energy = []
        self.building_buttons_water = []
        self.building_buttons_food = []
        self.building_buttons_minerals = []

        self.building_buttons = {"energy":self.building_buttons_energy,
                                 "food":self.building_buttons_food,
                                 "minerals":self.building_buttons_minerals,
                                 "water":self.building_buttons_water}
        self.building_buttons_list =self.building_buttons_energy + self.building_buttons_food +\
                                    self.building_buttons_minerals + self.building_buttons_water

        self.create_building_slots()

        # register the button
        self.parent.game_objects.append(self)
        self.parent.planets.append(self)
        #self.hide()

        self.planet_config = PlanetConfig(**kwargs)

    def set_orbit_object(self, obj):
        self.orbit_object = obj
        self.orbit_distance = source.AppHelper.get_distance(self.pos, obj.pos)
        self.offset.x = self.orbit_object.getX() - self.getX()
        self.offset.y = self.orbit_object.getY() - self.getY()
        self.orbit_speed = (self.offset.x / self.orbit_distance) * 0.01

    def orbit(self):
        self.orbit_angle += self.orbit_speed
        orbit_point = self.orbit_object.imageRect.center - self.offset.rotate(self.orbit_angle)
        self._x = orbit_point[0]
        self._y = orbit_point[1]
        self.set_center()


    def orbit_(self):
        self.orbit_angle += self.orbit_speed
        orbit_point = self.orbit_object.imageRect.center + self.offset.rotate(-self.orbit_angle)
        self._x = orbit_point[0]
        self._y = orbit_point[1]
        self.set_center()

    def orbit__(self):
        self.orbit_angle -= self.orbit_speed
        orbit_center = self.orbit_object.imageRect.center
        orbit_point = self.offset.rotate(self.orbit_angle) + orbit_center
        self._x = orbit_point[0]
        self._y = orbit_point[1]
        self.set_center()

    def set_population_limit(self):
        """
        sets the population limit for the planet, based on city buildongs:
        "town":1000,  "city":10000, "metropole":100000
        :return:
        """

        self.population_limit = sum([self.population_buildings_values[i] for i in self.buildings if i in self.population_buildings])

    def update_game_variables(self):
        """
        updates the population
        :return:
        """
        # timed execute: wait = seconds
        if time.time() > self.start_time + self.wait:
            self.start_time = time.time()
            if self.population_limit > self.population:
                self.population += self.population_grow
            # print ("Planet.update_game_variables", self.population_grow,  self.population)

    def calculate_production(self):
        """
        calculates the production, sets the overview icons (smiley, thumpsup) for display the condition of the planet
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

        for i in self.buildings:
            for key, value in production[i].items():
                self.production[key] += value

        self.production_water = self.production["water"]
        self.production_energy = self.production["energy"]
        self.production_food = self.production["food"]
        self.production_minerals = self.production["minerals"]
        self.production_technology = self.production["technology"]
        self.production_city = self.production["city"]

        self.calculate_population()

        # is everything in plus, show thumbsup green,otherwise red, set smiley to sad if no food production
        vl = []
        for key, value in self.production.items():
            if value < 0:
                vl.append(value)
        if len(vl) > 0:
            self.thumpsup_button.setImage(pygame.transform.flip(pygame.transform.scale(source.Globals.images[pictures_path]["icons"]["thumps_upred.png"],self.thumpsup_button_size),True,True))
        else:
            self.thumpsup_button.setImage(pygame.transform.flip(pygame.transform.scale(source.Globals.images[pictures_path]["icons"]["thumps_up.png"],self.thumpsup_button_size),True,False))

        if self.production["food"] > 0:
            self.smiley_button.setImage(source.Globals.images[pictures_path]["icons"]["smile.png"])
        else:
            self.smiley_button.setImage(source.Globals.images[pictures_path]["icons"]["sad.png"])

    def calculate_population(self):
        """ calculates population"""
        if self.production["food"] > 0:
            self.population_grow = source.config.population_grow_factor * self.production["food"]

    def set_info_text(self):
        """
        sets the text used for the info_panel
        :return:
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

    def execute(self,  kwargs):
        """ this executes the code when clicked on the button """
        if self.parent.build_menu_visible: return
        self.set_info_text()
        #self.parent.selected_planet = self
        self.parent.set_selected_planet(self)

    def on_hover_release_callback(self,x,y):
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
        :return:
        """
        if not self._hidden:
            x, y = Mouse.getMousePos()
            if self.on_hover_release_callback(x,y):
                source.Globals.tooltip_text = ""

    def listen(self, events):
        """ Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        self.reset_tooltip()
        self.move(events)
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y): # checks if mouse over ??
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
                    self.win.blit(self.hover_image,(self._x, self._y))

                    if self.tooltip != "":
                        source.Globals.tooltip_text = self.tooltip

            else:

                self.clicked = False

    def move(self, events):
        """
        calls the move function from the Button Class
        :param events:
        :return:
        """
        super().move(events,self)

    def update(self): 
        """
        updates the planet...a lot of stuff, hav e look on the code, its self explaining
        """
        if self.name == "Sun":
            self.disable()
            if not self.explored:
                self.parent.fog_of_war.draw_fog_of_war(self)
                self.explored = True
            # hide if some ui is blockin it
            if self.parent.event_panel._hidden:
                if not self.parent.build_menu_visible:
                    self.show()
            return

        # update orbit angle
        if source.Globals.enable_zoom:
            self.enable_orbit = False
        else:
            self.enable_orbit = True

        if self.enable_orbit:
            self.orbit()
        # surface = pygame.surface.Surface([self.orbit_distance, self.orbit_distance])
        # pygame.draw.circle(surface, (140, 170, 100), (self.orbit_object.getX(), self.orbit_object.getY()),
        #     self.orbit_distance, 1)
        # self.win.blit(surface,(self.orbit_object.getX(), self.orbit_object.getY()))


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
            if not self.name == "Sun":
                self.tooltip = "right click to build something useful!"
                self.text.set_alpha(255)

            # only the first time after exploring
            if not self.just_explored:
                self.setImage(self.planet_image)
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
        :return:
        """
        sounds.play_sound(sounds.happy, channel=4)
        self.building_slots.enable()
        for i in self.building_slots.getButtons():
            #print (i)
            #i.enable()
            i.show()
        self.show_overview_button()
        self.parent.set_selected_planet(self)






