import math
import random

import pygame
from pygame.math import Vector2
from pygame_widgets.mouse import Mouse, MouseState

import source.Globals
from source.Globals import *
import source.WidgetHandler
from source.Button import Moveable, ImageButton
from source.Images import pictures_path
from source.ProgressBar import ProgressBar
from source.Sounds import sounds
from source.WidgetHandler import WidgetBase


class ShipRanking:
    """
    all functions and variables needed to ranke the ship
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

        # ranking
        self.experience = 0
        self.experience_factor = 3000
        self.rank = "Cadet"
        self.ranks = {0: "Cadet", 1: "Ensign", 2: "Lieutenant", 3: "Commander", 4: "Commodore", 5: "Captain", 6: "Vice Admiral", 7: "Admiral", 8: "Fleet Admiral"}

        # rank image
        self.rank_images = {
            "Cadet": source.Globals.images[pictures_path]["icons"]["badge1_30x30.png"],
            "Ensign": source.Globals.images[pictures_path]["icons"]["badge2_30x30.png"],
            "Lieutenant": source.Globals.images[pictures_path]["icons"]["badge3_30x30.png"],
            "Commander": source.Globals.images[pictures_path]["icons"]["badge4_48x30.png"],
            "Commodore": source.Globals.images[pictures_path]["icons"]["badge5_48x30.png"],
            "Captain": source.Globals.images[pictures_path]["icons"]["badge6_48x30.png"],
            "Vice Admiral": source.Globals.images[pictures_path]["icons"]["badge7_43x30.png"],
            "Admiral": source.Globals.images[pictures_path]["icons"]["badge8_43x30.png"],
            "Fleet Admiral": source.Globals.images[pictures_path]["icons"]["badge9_44x30.png"]
            }
        # resize rank images
        for key, image in self.rank_images.items():
            self.rank_images[key] = pygame.transform.scale(image, (image.get_width() / 2, image.get_height() / 2))

    def set_experience(self, value):
        self.experience += value
        self.set_rank()
        #print ("self.experience", self.experience)

    def set_rank(self):
        rank_value = int(self.experience/self.experience_factor)
        if rank_value < 0:
            rank_value = 0
        elif rank_value > 8:
            rank_value = 8

        self.rank = self.ranks[rank_value]

    def draw_rank_image(self):
        if not source.Globals.app.build_menu_visible:
            image = self.rank_images[self.rank]
            self.win.blit(image, (self.getX() + self.getWidth()/2 - image.get_width()/2, self.getY() + self.rank_image_y))


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

    def set_orbit_object(self, obj):
        self.orbit_object = obj
        self.orbit_distance = source.AppHelper.get_distance(self.pos, obj.pos)
        self.offset.x = self.orbit_object.getX() - self.getX()
        self.offset.y = self.orbit_object.getY() - self.getY()
        self.orbit_speed = self.offset.x / self.orbit_distance * 0.1

    def orbit(self):
        self.orbit_object = self.energy_reloader
        self.offset = Vector2(self.orbit_object.getWidth(), self.orbit_object.getHeight())
        target_point = self.orbit_object.imageRect.center + self.offset.rotate(self.orbit_angle)

        # Calculate distance between object and orbit point
        distance = math.sqrt((self._x - target_point[0]) ** 2 + (self._y - target_point[1]) ** 2)

        if distance > self.desired_orbit_radius * 0.01:
            if self.energy > 0:
                # Move towards the orbit point
                direction = Vector2(target_point[0] - self._x, target_point[1] - self._y)
                direction.normalize_ip()
                direction *= self.orbit_speed
                self._x += direction.x
                self._y += direction.y
        else:
            # Calculate new orbit point
            self.orbit_angle -= self.orbit_speed
            self.orbit_point = self.orbit_object.imageRect.center + self.offset.rotate(self.orbit_angle)
            self._x = self.orbit_point[0]
            self._y = self.orbit_point[1]

        self.set_center()
        # self.x = self._x
        # self.y = self._y

    def show_connections(self):
        if self.target:
            if hasattr(self.target, "x"):
                pygame.draw.line(surface=self.win,
                                 start_pos=self.center,
                                 end_pos=self.target.center,
                                 color =source.Globals.colors.frame_color,
                                 width=5)

    def move_to_connection(self):
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

        # set target and calc new position
        self.set_center()

        target = self.target


        if hasattr(target, "x"):
            x1 = target.imageRect.center[0]
            y1 = target.imageRect.center[1]

        elif hasattr(target, "crew"):
                x1 = target.imageRect.center[0]
                y1 = target.imageRect.center[1]
        else:
            x1 = self.target[0]
            y1 = self.target[1]

        x = self.getX()
        y = self.getY()

        dist_x = (x1-x)
        dist_y = (y1-y)
        distance  = math.dist((x,y), (x1,y1))

        try:
            new_x = x + (self.speed * dist_x)/distance*source.Globals.time_factor
            new_y = y + (self.speed * dist_y)/distance*source.Globals.time_factor
        except ZeroDivisionError:
            return

        # set new position
        self.setX(new_x)
        self.setY(new_y)

        # rotate image to target
        self.track_to(target)

        # plays sound
        if not self.hum_playing:
            sounds.play_sound(self.hum, channel=self.sound_channel,loops=1000, fade_ms= 500)
            #pygame.mixer.Sound.play(self.hum)
            self.hum_playing = True

        # if goal reached (planet)
        if hasattr(self.target, "x"):
            if distance <= target.getWidth():
                self.target.explored = True

                # set event_text
                self.parent.event_text = "WELL DONE! your ship has just reached a habitable planet! : " + self.target.name

                # self.parent.draw()
                self.parent.fog_of_war.draw_fog_of_war(self.target)

                # unload_cargo goods
                self.unload_cargo()

                # reset selection/target
                self.set_energy_reloader(self.target)
                self.target = None
                self.select(False)

                # whats this for ?!???
                self.rect = self.imageRect
                sounds.stop_sound(self.sound_channel)
                #pygame.mixer.Sound.stop(self.hum)
                self.hum_playing = False
                #sounds.stop_sound(self.sound_channel)





        elif hasattr(self.target,"crew"):
            if distance <= target.getWidth():
                # set event_text
                self.parent.event_text = "your ship has just reached a another ship: " + self.target.name + "reloading ship: " +self.name + "from : " + self.target.name

                # reset selection/target
                self.set_energy_reloader(self.target)
                self.target = None
                self.select(False)

                # whats this for ?!???
                self.rect = self.imageRect
                sounds.stop_sound(self.sound_channel)
                #pygame.mixer.Sound.stop(self.hum)
                self.hum_playing = False
                #sounds.stop_sound(self.sound_channel)
                self.moving = False


        else:
            if distance <= 5:
                self.target = None
                self.select(False)
                sounds.stop_sound(self.sound_channel)
                #pygame.mixer.Sound.stop(self.hum)
                self.hum_playing = False
                #sounds.stop_sound(self.sound_channel)

                # whats this for ?!???
                self.rect = self.imageRect
                self.moving = False

        # calculate travelcosts
        self.energy -= distance*self.energy_use * source.Globals.time_factor
        self.energy = int(self.energy)
        #self.set_info_text()

        # set progress bar position
        self.set_progressbar_position()

        # self.parent.draw()
        self.parent.fog_of_war.draw_fog_of_war(self)

        # draw the image
        #self.win.blit(self.image_rot, self.image_rect_rot)

        # develop planet if distance is near enough
        self.develop_planet()

        # get experience
        self.set_experience(1)

        self.x = self._x
        self.y = self._y

        return True

    def set_energy_reloader(self, obj):
        #print ("setting energy reloader to  :", obj)
        self.energy_reloader = obj

    def set_progressbar_position(self):
        # set progress bar position
        self.progress_bar.setX(self.getX())
        self.progress_bar.setY(self.getY() + self.getHeight() + +self.getHeight()/5)

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


        if self.energy>0:
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

        self.image_rot  = pygame.transform.rotate(self.image, angle)
        self.image_rect_rot = self.image_rot.get_rect(center = self.center)
        self.imageRect = self.image_rect_rot

    def set_position(self):
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
        self.speed_up_button = ImageButton(source.Globals.win,self.getX(), self.getY() + self.getHeight(), 32,32,
            isSubWidget=False,image=source.Globals.images[pictures_path]["icons"]["speed_up.png"],
            onClick=lambda : print("Ok") )
        self.radius_button = ImageButton(source.Globals.win,self.getX() + self.getWidth(), self.getY() + self.getHeight(),
            32,32, isSubWidget=False, image=source.Globals.images[pictures_path]["icons"]["radius.png"],
            onClick=lambda : print("Ok"))

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
        self.speed_up_button.show()
        self.radius_button.show()


class ShipParams:
    """
    holds variables for the ship and functions aswell
    """
    def __init__(self, **kwargs):

        self.reload_max_distance = 100
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
                          "food":self.food,
                          "population":self.population,
                          "water":self.water,
                          "technology": self.technology}

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
                                        y=self.getY() + self.getHeight()+self.getHeight()/5,
                                        width=self.getWidth(),
                                        height=5,
                                        progress=lambda: 1 / self.energy_max * self.energy,
                                        curved=True,
                                        completedColour =source.Globals.colors.frame_color,
                                        layer = self.layer,
                                        parent = self
                                        )
        # upgrade
        self.upgrade_factor = 1.5

    def on_hover_release_callback(self,x,y):
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
        if not self._hidden:
            x, y = Mouse.getMousePos()
            if self.on_hover_release_callback(x,y):
                source.Globals.tooltip_text = ""

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
        text += "resources loaded: "  + "\n\n"
        text += "water: " + str(self.water) + "/" + str(self.water_max) + "\n"
        text += "energy: " + str(self.energy) + "/" + str(self.energy_max) + "\n"
        text += "food: " + str(self.food) + "/" + str(self.food_max) + "\n"
        text += "minerals: " + str(self.minerals) + "/" + str(self.minerals_max) + "\n"
        text += "technology: " + str(self.technology) + "/" + str(self.technology_max) + "\n\n"

        text += "speed: " + str(self.speed) + "\n"
        text += "scanner range: " + str(self.fog_of_war_radius) + "\n"
        text += "crew: "  + str(self.crew)  + "\n"

        if self.debug:
            text += "\n\ndebug:\n"
            text += "\ntarget: " + str(self.target ) + "\n"

            text += "selected: " + str(self.selected) + "\n"
            text += "reloader: " + str(self.energy_reloader) + "\n"
            text += "move_stop: " + str(self.move_stop) + "\n"
            text += "moving: " + str(self.moving)

            #text += str(dir(self))

        self.parent.info_panel.set_text(text)
        self.parent.info_panel.set_planet_image(self.image)

    def develop_planet(self):
        for i in source.WidgetHandler.WidgetHandler.layers[3]:
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

        if hasattr(obj,"x"):
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

        startpos = (self.imageRect.center[0] +r, self.imageRect.center[1] +r)
        endpos = (self.energy_reloader.imageRect.center[0] +r0,self.energy_reloader.imageRect.center[1] + r0)

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
                color=pygame.color.THECOLORS["white"], width=r*2)

        #pygame.mixer.Channel(2).play (source.Globals.sounds.electricity2)
        #sounds.play_sound(sounds.electricity2, channel=self.sound_channel)
        self.parent.event_text = "reloading spaceship: --- needs a lot of energy!"

    def reload_ship(self):

        if self.energy_reloader:
            if self.get_distance_to(self.energy_reloader) > self.reload_max_distance:
                return
            
            #print("reloading ship:", self.name)
            # if reloader is a planet
            if hasattr(self.energy_reloader, "production"):
                if self.energy_reloader.production["energy"] > 0:
                    if self.parent.player.energy - self.energy_reload_rate * self.energy_reloader.production["energy"] > 0:
                        if self.energy < self.energy_max:
                            self.energy += self.energy_reload_rate * self.energy_reloader.production["energy"]
                            self.parent.player.energy -= self.energy_reload_rate * self.energy_reloader.production["energy"]
                            self.flickering()
                        else:
                            self.parent.event_text = "Ship reloaded sucessfully!!!"

                            sounds.stop_sound(self.sound_channel)

            # if relaoder is a ship
            elif hasattr(self.energy_reloader, "crew"):
                if self.energy_reloader.energy > 0:
                    if self.energy_reloader.energy - self.energy_reload_rate > 0:
                        if self.energy < self.energy_max:
                            self.energy += self.energy_reload_rate
                            self.energy_reloader.energy -= self.energy_reload_rate
                            self.flickering()
                        else:
                            self.parent.event_text = "Ship reloaded sucessfully!!!"

                            sounds.stop_sound(self.sound_channel)
        else:

            sounds.stop_sound(self.sound_channel)

    def upgrade(self, key):
        setattr(self, key, getattr(self,key) * self.upgrade_factor)

    def unload_cargo(self):
        text = ""
        for key,value in self.resources.items():
            if value > 0:
                text += key + ": " + str(value)
                setattr(self.parent.player, key, getattr(self.parent.player,key) + value)
                self.resources[key] = 0
                setattr(self, key, 0 )

        self.parent.event_text = "unloading ship: " + text


class Ship(WidgetBase, ShipParams, ShipMoving, Moveable, ShipRanking, ShipButtons):
    """ this is the Ship class"""

    def __init__(self, win, x, y, width, height, isSubWidget=False, *args, **kwargs):
        WidgetBase.__init__(self,win, x, y, width, height, isSubWidget, **kwargs)
        ShipParams.__init__(self,**kwargs)
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

        # selection image
        self.selection_image = pygame.transform.scale(kwargs.get("selection_image"), (self.getWidth(), self.getHeight()))
        self.selection_image.set_alpha(200)

        # no energy image
        self.noenergy_image = source.Globals.images[pictures_path]["resources"]["noenergy_25x25.png"]

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

    def get_hit_object(self):
        for obj in self.parent.planets:
            if obj.imageRect.collidepoint(pygame.mouse.get_pos()):
                return obj

        for obj in self.parent.ships:
            if obj.imageRect.collidepoint(pygame.mouse.get_pos()):
                return obj
        return None

    def listen(self, events):
        self.reset_tooltip()

        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                # print("ship.listen:", mouseState)
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
                    if self.parent.ship == self:



                        self.set_target()
                        if self.get_hit_object():
                            self.set_energy_reloader(self.get_hit_object())

    def set_target(self):
        target = self.get_hit_object()
        if target == self:
            return
        if target:
            self.target = target
            self.energy_reloader = target

            # this resets the orbit angle to make shure start point is always the same
            self.angle = 0
        else:
            self.target = pygame.mouse.get_pos()
            self.set_energy_reloader(None)

        self.select(False)

    def set_tooltip(self):
        text = "selected: " + str(self.selected)
        self.tooltip = self.name + ": " + " speed: " + str(self.speed) + "e, scanner range: " + str(self.fog_of_war_radius) + text

    def submit_tooltip(self):
        if self.tooltip:
            if self.tooltip != "":
                source.Globals.tooltip_text = self.tooltip

    # draw functions
    def draw(self):

        self.set_position()
        self.set_progressbar_position()
        if self._hidden:
            return
        self.draw_image_rot()
        self.draw_rank_image()

        #print("ship state: ", self.rank)

        if self.selected:
            self.show_selection()
            self.draw_line()
            self.track_to(pygame.mouse.get_pos())
            self.set_info_text()

        # travel
        if self.target:
            if self.energy > 0:
                self.move_to_connection()
                self.show_connections()



        if self.energy_reloader:
            #self.draw_dict()
            # reload ship
            self.reload_ship()
            # orbit aroudn the planet

            self.orbit()
            pass



        # move stopp reset
        if self.energy > 0:
            self.move_stop = 0

        # move stopp
        if self.energy <= 0:
            self.move_stop += 1

            sounds.stop_sound(self.sound_channel)
            self.draw_noenergy_image()

        self.low_energy_warning()

        #self.update_position()

    def draw_image_rot(self):
        if not source.Globals.app.build_menu_visible:
            self.win.blit(self.image_rot, self.image_rect_rot)

    def draw_image__(self):
        self.win.blit(self.image, self.imageRect)

    def draw_line(self):
        """
        draws line to mouse position and draws the scope

        """
        # draw line from selected object to mouse cursor
        if self.selected:
            pygame.draw.line(surface=self.win, start_pos=self.center, end_pos=pygame.mouse.get_pos(), color =source.Globals.colors.frame_color)

            # scope
            pos = pygame.mouse.get_pos()
            size_x = 30
            size_y = 30
            arrow = pygame.draw.arc(self.win, source.Globals.colors.frame_color,((pos[0]-size_x/2,pos[1]-size_y/2),(size_x,size_y)),2,10,2)
            arrow = pygame.draw.arc(self.win, source.Globals.colors.frame_color,((pos[0] - size_x, pos[1] - size_y), (size_x*2, size_y*2)), 2, 10, 2)

            # horizontal line
            factor = size_x / 12
            x = pos[0]-size_x*factor/2
            y = pos[1]
            x1 = x+size_x * factor
            y1 = y
            pygame.draw.line(surface=self.win, start_pos=(x, y), end_pos=(x1, y1), color =source.Globals.colors.frame_color)

            # vertical line
            x = pos[0]
            y = pos[1] - size_x*factor/2
            x1 = x
            y1 = y + size_x * factor
            pygame.draw.line(surface=self.win, start_pos=(x,y), end_pos=(x1,y1), color =source.Globals.colors.frame_color)

    def set_center(self):
        self.center = (self.getX() + self.getWidth() / 2, self.getY() + self.getHeight() / 2)

    def debug(self): # not used
        print ("________________________________________________________")
        print ("self.move_to_connection():", self.move_to_connection())
        print("move_to_mouse_position(self):", self.move_to_mouse_position())
        print ("orbit", self.orbit)
        print ("self.selected", self.selected)

    def show_selection(self):
        self.win.blit(self.selection_image, (self.getX(), self.getY()))

    def select(self, value):
        self.selected = value
        if value:
            sounds.play_sound("click", channel=7)

    def update(self):
        self.reposition_buttons()
        if self.selected:
            self.show_buttons()
        else:
            self.hide_buttons()

    def draw_noenergy_image(self):
        if not self._disabled:
            self.win.blit(self.noenergy_image, (self.getX() + self.noenergy_image_x, self.getY() + self.noenergy_image_y))


class Spaceship(Ship):
    def __init__(self,win, x, y, width, height, isSubWidget=False, *args, **kwargs):
        Ship.__init__(self,win, x, y, width, height, isSubWidget=False, *args, **kwargs)
        self.hum = sounds.hum1
        self.sound_channel = 1

        # setup Game variables
        self.speed = 0.1
        self.energy_max = 10000
        self.energy = 10000
        self.energy_use = 0.0005
        self.energy_reload_rate = 1
        #self.move_stop = 0
        self.energy_warning_level = 500
        self.noenergy_image_x = 0
        self.noenergy_image_y = -self.getHeight()
        self.rank_image_x = 0
        self.rank_image_y = -self.getHeight()/1.5


        self.crew = 7
        self.crew_members = ["john the cook", "jim the board engineer", "stella the nurse", "sam the souvenir dealer",
                             "jean-jaques the artist", "Nguyen thon ma, the captain", "dr. Hoffmann the chemist"]


        # fog of war
        self.fog_of_war_radius = 100

        # tooltip
        self.set_tooltip()


class Cargoloader(Ship):
    def __init__(self,win, x, y, width, height, isSubWidget=False, *args, **kwargs):
        Ship.__init__(self,win, x, y, width, height, isSubWidget=False, *args, **kwargs)
        self.hum = sounds.hum2
        self.sound_channel = 2

        # setup Game variables
        self.speed = 0.02
        self.energy_max = 20000
        self.energy = 15000
        self.energy_use = 0.001
        self.energy_reload_rate = 0.5
        #self.move_stop = 0
        self.energy_warning_level = 500
        self.noenergy_image_x = 0
        self.noenergy_image_y = -self.getHeight()/2
        self.rank_image_x = 0
        self.rank_image_y = -self.getHeight()/2.4

        self.crew = 7
        self.crew_members = ["john the cook", "jim the board engineer", "stella the nurse", "sam the souvenir dealer",
                             "jean-jaques the artist", "Nguyen thon ma, the captain", "dr. Hoffmann the chemist"]

        # fog of war
        self.fog_of_war_radius = 50

        # tooltip
        self.set_tooltip()


class Spacehunter(Ship):
    def __init__(self,win, x, y, width, height, isSubWidget=False, *args, **kwargs):
        Ship.__init__(self,win, x, y, width, height, isSubWidget=False, *args, **kwargs)
        self.hum = sounds.hum3
        self.sound_channel = 3
        # setup Game variables
        self.speed = 0.2
        self.energy_max = 5000
        self.energy = 5000
        self.energy_use = 0.0015
        self.energy_reload_rate = 1.5
        self.energy_warning_level = 500
        self.noenergy_image_x = 0
        self.noenergy_image_y = -self.getHeight()
        self.rank_image_x = 0
        self.rank_image_y = -self.getHeight()/1.5

        self.crew = 7
        self.crew_members = ["john the cook", "jim the board engineer", "stella the nurse", "sam the souvenir dealer",
                             "jean-jaques the artist", "Nguyen thon ma, the captain", "dr. Hoffmann the chemist"]

        # fog of war
        self.fog_of_war_radius = 30

        # tooltip
        self.set_tooltip()

