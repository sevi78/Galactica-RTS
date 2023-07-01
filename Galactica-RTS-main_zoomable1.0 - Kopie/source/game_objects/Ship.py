import math
import random

from pygame.math import Vector2
from pygame_widgets.mouse import Mouse, MouseState

import source.gui.WidgetHandler
import source.utils.Globals
from source import utils
from source.gui.Button import Moveable, ImageButton
from source.gui.ProgressBar import ProgressBar
from source.gui.WidgetHandler import WidgetBase, WidgetHandler
from source.utils import debug_positions, get_distance, colors, images
from source.utils.Globals import *
from source.utils.images import pictures_path
from source.utils.sounds import sounds


class ShipRanking:
    """
    all functions and variables needed to rank the ship
    params: experience
            rank
            ranks
            rank_images

    functions:
            set_experience
            set_rank
            draw_rank_image

    possible ranks:
            {0: "Cadet", 1: "Ensign", 2: "Lieutenant", 3: "Commander", 4: "Commodore", 5: "Captain", 6: "Vice Admiral", 7: "Admiral", 8: "Fleet Admiral"}

    """

    def __init__(self):
        self.property = "ship"
        # ranking
        self.experience = 0
        self.experience_factor = 3000
        self.rank = "Cadet"
        self.ranks = {0: "Cadet", 1: "Ensign", 2: "Lieutenant", 3: "Commander", 4: "Commodore", 5: "Captain", 6: "Vice Admiral", 7: "Admiral", 8: "Fleet Admiral"}

        # rank image
        self.rank_images = {
            "Cadet": images[pictures_path]["icons"]["badge1_30x30.png"],
            "Ensign": images[pictures_path]["icons"]["badge2_30x30.png"],
            "Lieutenant": images[pictures_path]["icons"]["badge3_30x30.png"],
            "Commander": images[pictures_path]["icons"]["badge4_48x30.png"],
            "Commodore": images[pictures_path]["icons"]["badge5_48x30.png"],
            "Captain": images[pictures_path]["icons"]["badge6_48x30.png"],
            "Vice Admiral": images[pictures_path]["icons"]["badge7_43x30.png"],
            "Admiral": images[pictures_path]["icons"]["badge8_43x30.png"],
            "Fleet Admiral": images[pictures_path]["icons"]["badge9_44x30.png"]
            }

        # resize rank images
        for key, image in self.rank_images.items():
            self.rank_images[key] = pygame.transform.scale(image, (image.get_width() / 2, image.get_height() / 2))

    def set_experience(self, value):
        self.experience += value
        self.set_rank()

    def set_rank(self):
        rank_value = int(self.experience / self.experience_factor)
        if rank_value < 0:
            rank_value = 0
        elif rank_value > 8:
            rank_value = 8
        prev_rank = self.rank
        self.rank = self.ranks[rank_value]
        prev_key = next((key for key, value in self.ranks.items() if value == prev_rank), None)
        curr_key = next((key for key, value in self.ranks.items() if value == self.rank), None)
        if curr_key > prev_key:
            self.parent.event_text = "Congratulations !!! Rank increased from {} to {} !!!".format(prev_rank, self.rank)
            sounds.play_sound(sounds.rank_up)
        elif curr_key < prev_key:
            self.parent.event_text = "Shame on you !!! Rank decreased from {} to {} !!!".format(prev_rank, self.rank)
            sounds.play_sound(sounds.rank_down)

    def draw_rank_image(self):
        if not utils.Globals.app.build_menu_visible:
            image = self.rank_images[self.rank]
            # self.win.blit(image, (
            # self.getX() + self.getWidth() / 2 - image.get_width() / 2 / self.get_zoom(),
            # self.getY() + self.rank_image_y / self.get_zoom()))

            self.win.blit(image, (self.center[0] + self.getWidth()/2/ self.get_zoom(),
                                  self.center[1] - self.getHeight()/2/ self.get_zoom()))


class ShipMoving:
    """
    holds the fuctions and variables to move the ship:
    params:
            desired_orbit_radius
            offset
            orbit_angle (used for the orbit position)
            target (target to track or move to)
            moving
            orbiting
            orbit_speed
            orbit_object
            offset ( distance to orbit object)
            orbit_point ( the point to get for orbiting)

    functions:
            set_orbit_object (obj=any Planet, mouseposition, any Ship)
            orbit
            show_connections (draws lines between target and ship)
            move_to_connection
            set_energy_reloader
            set_progressbar_position (updates the progressbar position)
            low_energy_warning
            track_to
            set_position
    """

    def __init__(self):
        self.desired_orbit_radius = 100
        self.offset = None
        self.orbit_angle = 0.0
        self.target = None
        self.moving = False
        self.orbiting = False
        self.orbit_speed = 0.5
        self.orbit_object = None
        self.offset = Vector2(100, 0)
        self.orbit_point = None
        self.target_point = None
        self.zoomable = True

    def show_connections(self):
        if self.target:
            if hasattr(self.target, "x"):
                pygame.draw.line(surface=self.win,
                    start_pos=self.center,
                    end_pos=self.target.center,
                    color=colors.frame_color,
                    width=5)

    def move_to_connection(self):
        print ("move_to_connection")
        self.moving = True
        # if stopped for any reason, no travel
        if self.move_stop > 0:
            self.moving = False
            self.set_experience(-1)
            return

        # low energy warning
        #self.low_energy_warning()

        # if everyting fine, undock and travel!(reset energy loader)
        # if not self.energy <= 1:
        #     self.set_energy_reloader(None)



        #rotate image to target

        self.track_to(self.target)

        self.play_travel_sound()

        self.reach_goal(get_distance((self.getX(), self.getY()), (self.validate_target())), self.target)

        if self.target:
            self.calculate_travel_cost(get_distance((self.getX(), self.getY()), (self.validate_target())))

        self.things_to_be_done_while_traveling()

        return True

    def validate_target(self):
        if type(self.target) == tuple:
            x, y = self.target
        else:
            x, y = self.target.getX(), self.target.getY()
        return x, y

    def play_travel_sound(self):
        # plays sound
        if not self.hum_playing:
            sounds.play_sound(self.hum, channel=self.sound_channel, loops=1000, fade_ms=500)
            self.hum_playing = True

    def reach_goal(self, distance, target):
        # if goal reached (planet)
        if hasattr(self.target, "x"):
            if distance <= target.getWidth():
                if hasattr(self.target, "property"):
                    if self.target.property == "planet":
                        self.target.explored = True

                        # set event_text
                        self.parent.event_text = "WELL DONE! your ship has just reached a habitable planet! : " + self.target.name

                        # self.parent.draw()
                        self.parent.fog_of_war.draw_fog_of_war(self.target)

                        # unload_cargo goods
                        self.unload_cargo()

                        # reset selection/target
                        self.set_energy_reloader(self.target)
                        #self.set_orbit_object(self.target)
                        #self.enable_orbit = True
                        #self.orbit_distance = 1#get_distance((self.getX(), self.getY()), (target.getX(), target.getY()))
                        #self.offset.x = 1
                        #self.orbit_distance = get_distance((self.x, self.y), (target.x, target.y)) - self.offset.x
                        #self.orbit_speed = 10
                        #
                        #

                    if self.target.property == "item":
                        self.target.get_collected()
                else:
                    self.target = None
                    self.select(False)

                sounds.stop_sound(self.sound_channel)

                self.hum_playing = False

                self.moving = False

        elif hasattr(self.target, "crew"):
            if distance <= target.getWidth():
                # set event_text
                self.parent.event_text = "your ship has just reached a another ship: " + self.target.name + "reloading ship: " + self.name + "from : " + self.target.name

                # reset selection/target
                self.set_energy_reloader(self.target)
                self.target = None
                self.select(False)

                # whats this for ?!???
                self.rect = self.imageRect
                sounds.stop_sound(self.sound_channel)
                self.hum_playing = False
                self.moving = False

        else:
            if distance <= 5:
                self.target = None
                self.select(False)
                sounds.stop_sound(self.sound_channel)
                self.hum_playing = False

                # whats this for ?!???
                self.rect = self.imageRect
                self.moving = False

    def things_to_be_done_while_traveling(self):
        # set progress bar position
        self.set_progressbar_position()

        # draw fog of war
        self.parent.fog_of_war.draw_fog_of_war(self)

        # develop planet if distance is near enough
        self.develop_planet()

        # get experience
        self.set_experience(1)

    def calculate_travel_cost(self, distance):
        # calculate travelcosts
        self.energy -= distance * self.energy_use * source.utils.Globals.time_factor * source.utils.Globals.game_speed
        self.energy = int(self.energy)

    def set_energy_reloader(self, obj):
        self.energy_reloader = obj

    def set_progressbar_position(self):

        # set progress bar position
        self.progress_bar.setX(self.getX() )
        self.progress_bar.setY(self.getY() + self.getHeight() /self.get_zoom())

        self.progress_bar.setWidth(self.progress_bar.parent.getWidth()/self.get_zoom())

    def low_energy_warning(self):
        return
        """
        bloody chatbot fuction, if energy is running out
        :return:
        """
        # low energy warning
        if self.energy < self.energy_warning_level:
            self.parent.event_text = "LOW ENERGY WARNING!!! your ship is running out of energy! find a planet to land soon!!"

        if self.energy <= 0:
            self.parent.event_text = "DAMMIT!!! your ship has run out of energy! you all gonna die !!!"
            self.move_stop += 1

        # if ship energy is empty
        if self.energy <= 0 and self.move_stop > 1000:
            self.parent.event_text = "NO ENERGY DUDE! you cant move with this ship! "
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 2000:
            self.parent.event_text = "..mhhh--- there might be a solution -- let me think about it a few seconds.."
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 3000:
            self.parent.event_text = "the board engineer and i, have worked hard on a solution to this problem:"
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 4000:
            self.parent.event_text = "how about this: we sacrifice john the cook, i mean do we really need him?" \
                                     " put him into the plasma reactor of our spaceship and get some energy out of him !"
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 5000:
            self.parent.event_text = "type 'yes' or 'no' if you want to burn the last cook from earth for surviving"
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 6000:
            self.parent.event_text = "haha!! that was just a joke! funny istn it ??"
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 7000:
            self.parent.event_text = "i mean, we will definitely cook the cook in the plasma engine, but I will decide for you :)"
            self.crew -= 1
            self.energy = 500
            self.move_stop = 0

        if self.energy > 0:
            self.move_stop = 0
        # print (self.move_stop)

    def track_to(self, target):
        """
        rotated the image to the target
        :param target: Planet, Ship or mouse position
        :return:
        """
        #   0 - image is looking to the right
        #  90 - image is looking up
        # 180 - image is looking to the left
        # 270 - image is looking down

        correction_angle = 90

        if hasattr(target, "x"):
            mx, my = target.getX(), target.getY()
        elif not self.target:
            mx, my = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        elif hasattr(target, "crew"):
            mx, my = target.getX(), target.getY()
        else:
            mx, my = target[0], target[1]

        dx, dy = mx - self.imageRect.centerx, my - self.imageRect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - correction_angle

        self.image_rot = pygame.transform.rotate(self.image, angle)
        self.image_rect_rot = self.image_rot.get_rect(center=self.center)
        self.imageRect = self.image_rect_rot

    def set_image_position(self):
        self.set_center()
        self.image_rect_rot = self.image_rot.get_rect(center=self.center)
        self.image_rect_rot.x = self._x
        self.image_rect_rot.y = self._y
        self.imageRect = self.image_rect_rot


class ShipButtons:
    """
    all UI elements of the ship, WIP
    """
    def __init__(self):
        self.visible = False
        self.speed_up_button = ImageButton(utils.Globals.win, self.getX(), self.getY() + self.getHeight(), 32, 32,
            isSubWidget=False, image=images[pictures_path]["icons"]["speed_up.png"],
            onClick=lambda: print("Ok"))
        self.radius_button = ImageButton(utils.Globals.win, self.getX() + self.getWidth(), self.getY() + self.getHeight(),
            32, 32, isSubWidget=False, image=images[pictures_path]["icons"]["radius.png"],
            onClick=lambda: print("Ok"))

    def reposition_buttons(self):
        self.spacing = 15
        self.speed_up_button.setX(self.getX() + self.getWidth() + self.spacing)
        self.speed_up_button.setY(self.getY() + self.getHeight())
        self.radius_button.setX(self.getX() + self.getWidth() + self.spacing)
        self.radius_button.setY(self.getY() + self.getHeight() - self.spacing * 3)

    def hide_buttons(self):
        self.speed_up_button.hide()
        self.radius_button.hide()

    def show_buttons(self):
        return
        self.speed_up_button.show()
        self.radius_button.show()


class ShipParams:
    """
    holds variables and functions for the ship
    """
    def __init__(self, **kwargs):

        self.reload_max_distance = 300
        self.debug = True
        self.name = kwargs.get("name")
        self.parent = kwargs.get("parent")
        self.layer = kwargs.get("layer", 3)

        # setup Game variables
        self.food = kwargs.get("food", 0)
        self.food_max = 0
        self.minerals = kwargs.get("minerals", 0)
        self.minerals_max = 0
        self.water = kwargs.get("water", 0)
        self.water_max = 0
        self.population = kwargs.get("population", 0)
        self.population_max = 0
        self.technology = kwargs.get("technology", 0)
        self.technology_max = 0

        self.resources = {"minerals": self.minerals,
                          "food": self.food,
                          "population": self.population,
                          "water": self.water,
                          "technology": self.technology
                          }

        self.speed = 0.1
        self.energy_max = 10000
        self.energy = 10000
        self.energy_reloader = None
        self.move_stop = 0
        self.crew = 7
        self.crew_members = ["john the cook", "jim the board engineer", "stella the nurse", "sam the souvenir dealer",
                             "jean-jaques the artist", "Nguyen thon ma, the captain", "dr. Hoffmann the chemist"]

        # fog of war
        self.fog_of_war_radius = 100
        self.parent.fog_of_war.draw_fog_of_war(self)

        # orbit
        self.offset = Vector2(100, 0)
        self.angle = 0

        # energy progress bar
        self.progress_bar = ProgressBar(win=self.win,
            x=self.getX(),
            y=self.getY() + self.getHeight() + self.getHeight() / 5,
            width=self.getWidth(),
            height=5,
            progress=lambda: 1 / self.energy_max * self.energy,
            curved=True,
            completedColour=colors.frame_color,
            layer=self.layer,
            parent=self
            )

        # upgrade
        self.upgrade_factor = 1.5

    def on_hover_release_callback(self, x, y):
        if self.contains(x, y):
            self.on_hover = True
            self.on_hover_release = False
        else:
            self.on_hover_release = True

        if self.on_hover and self.on_hover_release:
            self.on_hover = False

            return True

        return False

    def set_resources(self):
        self.resources = {"minerals": self.minerals,
                          "food": self.food,
                          "population": self.population,
                          "water": self.water,
                          "technology": self.technology
                          }

    def set_info_text(self):

        text = self.name + ":\n\n"
        text += "experience: " + str(self.experience) + "\n"
        text += "rank: " + self.rank + "\n\n"
        text += "resources loaded: " + "\n\n"
        text += "water: " + str(self.water) + "/" + str(self.water_max) + "\n"
        text += "energy: " + str(self.energy) + "/" + str(self.energy_max) + "\n"
        text += "food: " + str(self.food) + "/" + str(self.food_max) + "\n"
        text += "minerals: " + str(self.minerals) + "/" + str(self.minerals_max) + "\n"
        text += "technology: " + str(self.technology) + "/" + str(self.technology_max) + "\n\n"
        text += "speed: " + str(self.speed) + "\n"
        text += "scanner range: " + str(self.fog_of_war_radius) + "\n"
        text += "crew: " + str(self.crew) + "\n"

        if self.debug:
            text += "\n\ndebug:\n"
            text += "\ntarget: " + str(self.target) + "\n"
            text += "selected: " + str(self.selected) + "\n"
            text += "reloader: " + str(self.energy_reloader) + "\n"
            text += "move_stop: " + str(self.move_stop) + "\n"
            text += "moving: " + str(self.moving)
            text += "position, x,y:" + str(int(self.getX())) + "/" + str(int(self.getY()))


            # text += str(dir(self))

        self.parent.info_panel.set_text(text)
        self.parent.info_panel.set_planet_image(self.image)

    def set_tooltip(self):
        text = "selected: " + str(self.selected)
        self.tooltip = self.name + ": " + " speed: " + str(self.speed) + "e, scanner range: " + str(self.fog_of_war_radius) + text

    def reset_tooltip(self):
        if not self._hidden:
            x, y = Mouse.getMousePos()
            if self.on_hover_release_callback(x, y):
                utils.Globals.tooltip_text = ""

    def submit_tooltip(self):
        if self.tooltip:
            if self.tooltip != "":
                utils.Globals.tooltip_text = self.tooltip

    def develop_planet(self):
        for i in WidgetHandler.layers[3]:
            if "Planet" in str(i):
                if i.name == "Sun": return
                if int(self.get_distance_to(i)) <= i.fog_of_war_radius:
                    if not i.explored:
                        self.set_experience(1000)
                        self.parent.event_text = f"WELL DONE! your {self.name} has just reached a habitable planet! : " + i.name
                        i.show()
                        self.parent.set_selected_planet(i)
                        self.parent.fog_of_war.draw_fog_of_war(i)
                        self.set_info_text()
                        i.explored = True

    def get_distance_to(self, obj):
        x = self.getX()
        y = self.getY()

        if hasattr(obj, "x"):
            try:
                x1 = obj.getX()
                y1 = obj.getY()
            except AttributeError:
                x1 = obj[0]
                y1 = obj[1]
        else:
            x1 = obj[0]
            y1 = obj[1]

        distance = math.dist((x, y), (x1, y1))

        return distance

    def flickering(self):
        # make flickering relaod stream :))
        r0 = random.randint(-4, 5)
        r = random.randint(-3, 4)
        r1 = random.randint(0, 17)
        r2 = random.randint(0, 9)

        startpos = (self.imageRect.center[0] + r, self.imageRect.center[1] + r)
        endpos = (self.energy_reloader.imageRect.center[0] + r0, self.energy_reloader.imageRect.center[1] + r0)

        if r0 == 0:
            return

        if r == 3:
            pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
                color=pygame.color.THECOLORS["yellow"], width=r2)

        if r == 7:
            pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
                color=pygame.color.THECOLORS["red"], width=r1)

        if r == 2:
            pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
                color=pygame.color.THECOLORS["white"], width=r * 2)

        # pygame.mixer.Channel(2).play (sounds.electricity2)
        # sounds.play_sound(sounds.electricity2, channel=self.sound_channel)
        self.parent.event_text = "reloading spaceship: --- needs a lot of energy!"

    def reload_ship(self):
        if self.energy_reloader:
            dist = self.get_distance_to(self.energy_reloader)

            if dist > self.reload_max_distance:
                return

            # if reloader is a planet
            if hasattr(self.energy_reloader, "production"):
                if self.energy_reloader.production["energy"] > 0:
                    if self.parent.player.energy - self.energy_reload_rate * self.energy_reloader.production["energy"] > 0:
                        if self.energy < self.energy_max:
                            self.energy += self.energy_reload_rate * self.energy_reloader.production["energy"] * source.utils.Globals.game_speed
                            self.parent.player.energy -= self.energy_reload_rate * self.energy_reloader.production["energy"] * source.utils.Globals.game_speed
                            self.flickering()
                        else:
                            self.parent.event_text = "Ship reloaded sucessfully!!!"
                            sounds.stop_sound(self.sound_channel)

                if self.energy_reloader.type == "sun":
                    if self.energy < self.energy_max:
                        self.energy += self.energy_reload_rate   * source.utils.Globals.game_speed
                        self.flickering()

            # if relaoder is a ship
            elif hasattr(self.energy_reloader, "crew"):
                if self.energy_reloader.energy > 0:
                    if self.energy_reloader.energy - self.energy_reload_rate * source.utils.Globals.game_speed > 0:
                        if self.energy < self.energy_max:
                            self.energy += self.energy_reload_rate
                            self.energy_reloader.energy -= self.energy_reload_rate * source.utils.Globals.game_speed
                            self.flickering()
                        else:
                            self.parent.event_text = "Ship reloaded sucessfully!!!"
                            sounds.stop_sound(self.sound_channel)
        else:
            sounds.stop_sound(self.sound_channel)

    def upgrade(self, key):
        setattr(self, key, getattr(self, key) * self.upgrade_factor)

    def unload_cargo(self):
        text = ""
        for key, value in self.resources.items():
            if value > 0:
                text += key + ": " + str(value)
                setattr(self.parent.player, key, getattr(self.parent.player, key) + value)
                self.resources[key] = 0
                setattr(self, key, 0)

                self.parent.event_text = "unloading ship: " + text
                sounds.play_sound(sounds.unload_ship)


class Ship(WidgetBase, ShipParams, ShipMoving, Moveable, ShipRanking, ShipButtons):
    """ this is the Ship class"""
    def __init__(self, win, x, y, width, height, isSubWidget=False, *args, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        ShipParams.__init__(self, **kwargs)
        ShipMoving.__init__(self)
        Moveable.__init__(self, x, y, width, height, kwargs)
        ShipRanking.__init__(self)
        ShipButtons.__init__(self)

        # display
        self.layer = kwargs.get("layer", 3)
        self.image_initial = kwargs.get("image")
        self.image = pygame.transform.scale(self.image_initial, (self.getWidth(), self.getHeight()))
        self.imageRect = self.image.get_rect()
        self.imageRect.left = self.getX()
        self.imageRect.top = self.getY()
        self.center = None
        self.set_center()

        # no energy image
        self.noenergy_image = images[pictures_path]["resources"]["noenergy_25x25.png"]

        # this is used for rotating, we will blitt mostly this.
        # TODO: use image instead of rot image and get source from image initial
        self.image_rot = pygame.transform.rotate(self.image, 90)
        self.image_rect_rot = self.image_rot.get_rect(center=self.center)

        # sound
        self.hum_playing = False

        # functionality
        self.on_hover = False
        self.on_hover_release = False
        self.selected = False
        self.target = None

        # register
        self.parent.ships.append(self)

    def set_center(self):

        self.center = (self.getX() + self.getWidth() / 2/self.get_zoom(), self.getY() + self.getHeight() / 2/self.get_zoom())

    def select(self, value):
        self.selected = value
        if value:
            sounds.play_sound("click", channel=7)

    def get_hit_object(self):
        for obj in self.parent.planets:
            if obj.imageRect.collidepoint(pygame.mouse.get_pos()):
                return obj

        for obj in self.parent.ships:
            if obj.imageRect.collidepoint(pygame.mouse.get_pos()):
                return obj

        for obj in self.parent.collectables:
            if obj.imageRect.collidepoint(pygame.mouse.get_pos()):
                return obj

        return None

    def listen(self, events):
        self.reset_tooltip()

        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                if mouseState == MouseState.RIGHT_CLICK:
                    if self.parent.ship == self:
                        if self.selected:
                            self.select(False)
                        else:
                            self.select(True)

                if mouseState == MouseState.RELEASE and self.clicked:
                    self.clicked = False

                elif mouseState == MouseState.CLICK:
                    self.clicked = True
                    self.select(True)
                    self.parent.ship = self

                elif mouseState == MouseState.DRAG and self.clicked:
                    pass

                elif mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                    self.submit_tooltip()
            else:
                self.clicked = False

                if mouseState == MouseState.CLICK:
                    self.select(False)
                    if self.parent.ship == self:
                        self.parent.ship = None

                if mouseState == MouseState.RIGHT_CLICK:
                    #if self.parent.ship == self:
                    if self.selected:

                        self.set_target()
                        if self.get_hit_object():
                            self.set_energy_reloader(self.get_hit_object())

    def set_target(self):
        target = self.get_hit_object()
        if target == self:
            return

        if target:
            self.target = target
            self.set_energy_reloader(target)

            # this resets the orbit angle to make shure start point is always the same
            self.angle = 0
        else:
            self.target = pygame.mouse.get_pos()
            self.set_energy_reloader(None)

        self.select(False)

    # draw functions
    def draw(self):
        self.set_screen_position()
        self.set_image_position()
        self.set_progressbar_position()
        # if self._hidden:
        #     return
        self.draw_image_rot()
        self.draw_rank_image()

        if self.selected:
            self.show_selection()
            self.draw_scope()
            self.set_info_text()

        # travel
        if self.target:
            if self.energy > 0:
                self.move_to_connection()
                self.show_connections()

        if self.energy_reloader:
            # reload ship
            self.reload_ship()

            # orbit around the planet
            #self.orbit(obj= self)
            self.orbiting = True
        else:
            self.orbiting = False

        # move stopp reset
        if self.energy > 0:
            self.move_stop = 0

        # move stopp
        if self.energy <= 0:
            self.move_stop += 1

            sounds.stop_sound(self.sound_channel)
            self.draw_noenergy_image()
            self.set_experience(-1)

        self.low_energy_warning()

        # self.update_position()
        debug_positions(x=self.x, y=self.y, color=colors.frame_color, size=10, text="self.x, self.y: ")
        debug_positions(x=self._x, y=self._y, color="red", size=12, text="self._x, self._y: ")

    def draw_image_rot(self):
        if not utils.Globals.app.build_menu_visible:
            self.win.blit(self.image_rot, self.image_rect_rot)

    def draw_scope(self):
        """
        draws line to mouse position and draws the scope
        """

        # draw line from selected object to mouse cursor
        if self.selected:
            self.set_center()
            pygame.draw.line(surface=self.win, start_pos=self.center, end_pos=pygame.mouse.get_pos(), color=colors.frame_color)

            # scope
            pos = pygame.mouse.get_pos()
            size_x = 30
            size_y = 30
            arrow = pygame.draw.arc(self.win, colors.frame_color, (
            (pos[0] - size_x / 2, pos[1] - size_y / 2), (size_x, size_y)), 2, 10, 2)

            arrow = pygame.draw.arc(self.win, colors.frame_color, (
            (pos[0] - size_x, pos[1] - size_y), (size_x * 2, size_y * 2)), 2, 10, 2)

            # horizontal line
            factor = size_x / 12
            x = pos[0] - size_x * factor / 2
            y = pos[1]
            x1 = x + size_x * factor
            y1 = y
            pygame.draw.line(surface=self.win, start_pos=(x, y), end_pos=(
            x1, y1), color=colors.frame_color)

            # vertical line
            x = pos[0]
            y = pos[1] - size_x * factor / 2
            x1 = x
            y1 = y + size_x * factor
            pygame.draw.line(surface=self.win, start_pos=(x, y), end_pos=(
            x1, y1), color=colors.frame_color)

    def show_selection(self):
        self.set_center()
        pygame.draw.circle(self.win,colors.frame_color, (self._x + self.getWidth()/2/self.get_zoom(), self._y + self.getHeight()/2/self.get_zoom()), self.getWidth()/2/self.get_zoom(), int(6*self.get_zoom()))

    def draw_noenergy_image(self):
        if not self._disabled:
            self.win.blit(self.noenergy_image, (
            self.getX() + self.noenergy_image_x, self.getY() + self.noenergy_image_y))

    def update(self):
        self.reposition_buttons()
        if self.selected:
            self.show_buttons()
        else:
            self.hide_buttons()
