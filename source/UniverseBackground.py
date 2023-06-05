import math
import random

import pygame
from pygame import gfxdraw
from pygame_menu._types import Any, NumberInstance, NumberType

import source.Globals
from source.AppHelper import limit_positions
from source.Button import Moveable
from source.Globals import pictures_path
from source.WidgetHandler import WidgetBase


class CelestialObject(WidgetBase, Moveable):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        Moveable.__init__(self, x, y, width, height, kwargs)

        self.rotation = random.randint(-3, 3)
        self.layer = kwargs.get("layer", 3)
        self.type = kwargs.get("type", "star")
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = kwargs.get("image", None)
        self.image_raw = self.image
        self.rotateable = ["galaxy", "nebulae", "asteroid", "comet"]
        if self.image:
            if self.type in self.rotateable:
                self.image = pygame.transform.rotate(self.image_raw, random.randint(-369, 360))
            self.image_rect = self.image.get_rect()
            self.image_rect.x = x
            self.image_rect.y = y

        self.parent = kwargs.get("parent")
        self.ui_parent = kwargs.get("ui_parent")

        # append to list
        # setattr(self.parent, getattr(self.parent, self.type), self)
        getattr(self.parent, self.type).append(self)
        # self.parent.stars.append(self)

    def listen(self, events):
        pass

    def get_counter_attribute(self, key: str, incr: Any = 0, default: Any = 0) -> NumberType:
        """
        Get counter attribute.

        :param key: Key of the attribute
        :param incr: Increase value
        :param default: Default vale to start with, by default it's zero
        :return: New increase value
        """
        if not isinstance(incr, NumberInstance):
            incr = float(incr)
        if not isinstance(default, NumberInstance):
            if isinstance(incr, float):
                default = float(default)
            else:
                try:
                    default = int(default)
                except ValueError:
                    default = float(default)
        if not self.has_attribute(key):
            self.set_attribute(key, default + incr)
            return default + incr
        new = self.get_attribute(key) + incr
        self.set_attribute(key, new)
        return new

    def draw(self):
        if not self._hidden:
            if self.image:
                # if self.type == "asteroid":
                #     image = pygame.transform.rotate(self.image,self.rotation )
                #     self.image = image

                self.image_rect.x = self.getX() - self.image.get_size()[0] / 2
                self.image_rect.y = self.getY() - self.image.get_size()[1] / 2

                self.win.blit(self.image, self.image_rect)

            elif self.type == "pulsating_star":
                t = pygame.time.Clock().get_time() * 0.001
                s = 2 * math.pi * random.random()
                x, y = self.getX(), self.getY()

                flicker = s
                c = int(127 * max(0.5, 1 + math.cos(t + flicker)))
                try:
                    gfxdraw.pixel(self.win, x, y, (c, c, c))
                except TypeError:
                    print(TypeError)
            else:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                # pygame.draw.circle(self.win, color, (self._x + self._width , self._y), self.width)
                pygame.draw.lines(self.win, color, True, [(self._x + 1, self._y), (self._x + 1, self._y)])

    def rescale(self):
        return
        if self._width <= 1 or self._height <= 1:
            return
        else:
            if self.image:
                self.image = pygame.transform.scale(self.image_raw, (self._width, self._height))
            else:
                return
                self.width = self._width


class Universe(WidgetBase, Moveable):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        Moveable.__init__(self, x, y, width, height, kwargs)
        self.parent = kwargs.get("parent")
        self.layer = kwargs.get("layer", 0)
        self.amount = int(math.sqrt(math.sqrt(width)) * source.Globals.settings["universe_density"])

        # define borders
        self.left_end = 0  # -self.getWidth()
        self.right_end = self.getWidth()
        self.top_end = 0  # -self.getHeight()
        self.bottom_end = self.getHeight()

        # images
        self.star_images = {
            0: source.Globals.images[pictures_path]["stars"]["star_30x30.png"],
            1: source.Globals.images[pictures_path]["stars"]["star_50x50.png"],
            2: source.Globals.images[pictures_path]["stars"]["star1_50x50.png"],
            3: source.Globals.images[pictures_path]["stars"]["star2_100x100.png"]
            }

        self.asteroid_images = {
            0: source.Globals.images[pictures_path]["celestial objects"]["asteroid_40x33.png"],
            }

        self.comet_images = {
            0: source.Globals.images[pictures_path]["celestial objects"]["comet_90x38.png"]
            }

        self.nebulae_images = {
            0: source.Globals.images[pictures_path]["celestial objects"]["nebulae_300x300.png"]
            }

        self.galaxy_images = {
            0: source.Globals.images[pictures_path]["celestial objects"]["galaxy_.png"],
            1: source.Globals.images[pictures_path]["celestial objects"]["galaxy3_small.png"]
            }

        # drawing lists
        self.star = []
        self.pulsating_star = []
        self.asteroid = []
        self.nebulae = []
        self.galaxy = []
        self.comet = []
        self.universe = []

        # create universe
        self.create_universe()

    def create_pulsating_star(self) -> None:
        """
        Add a new star to the simulation.
        """
        self.stars.append([
            random.randrange(1, self.menu.get_width()),  # x position
            random.randrange(1, self.menu.get_height()),  # y position
            2 * math.pi * random.random()  # initial flickering
            ])

    def create_stars(self):
        # star images
        for i in range(int(self.amount / 20)):
            x = random.randint(self.left_end, self.right_end)
            y = random.randint(self.top_end, self.bottom_end)

            select = random.randint(0, len(self.star_images.keys()) - 1)
            image = pygame.transform.scale(self.star_images[select], (15, 15))
            w = image.get_rect().width
            h = image.get_rect().height
            star = CelestialObject(self.win, x, y, w, h, image=image, layer=self.layer, parent=self, type="star")

        # flickering stars
        for i in range(int(self.amount / 3)):
            x = random.randint(self.left_end, self.right_end)
            y = random.randint(self.top_end, self.bottom_end)
            w = random.randint(1, 10)
            star = CelestialObject(self.win, x, y, w, w, layer=self.layer, parent=self, type="star")

        # # puslatoing stars
        # for i in range(int(self.amount / 3)):
        #     x = random.randint(self.left_end, self.right_end)
        #     y = random.randint(self.top_end, self.bottom_end)
        #     w = 1
        #     star = CelestialObject(self.win, x, y, w, w, layer=self.layer, parent=self, type="pulsating_star")

    def create_galaxys(self):
        for i in range(int(self.amount / 300)):
            select = random.randint(0, len(self.galaxy_images.keys()) - 1)
            image = self.galaxy_images[select]
            w = image.get_rect().width
            h = image.get_rect().height
            x = random.randint(self.left_end, self.right_end)
            y = random.randint(self.top_end, self.bottom_end)

            galaxy = CelestialObject(self.win, x, y, w, h, image=image, layer=self.layer, parent=self, type="galaxy")

    def create_nebulaes(self):
        for i in range(int(self.amount / 250)):
            select = random.randint(0, len(self.nebulae_images.keys()) - 1)
            image = self.nebulae_images[select]
            w = image.get_rect().width
            h = image.get_rect().height
            x = random.randint(self.left_end, self.right_end)
            y = random.randint(self.top_end, self.bottom_end)

            nebulae = CelestialObject(self.win, x, y, w, h, image=image, layer=self.layer, parent=self, type="nebulae")

    def create_asteroids(self):
        for i in range(int(self.amount / 50)):
            select = random.randint(0, len(self.asteroid_images.keys()) - 1)
            image = self.asteroid_images[select]
            w = image.get_rect().width
            h = image.get_rect().height
            x = random.randint(self.left_end, self.right_end)
            y = random.randint(self.top_end, self.bottom_end)

            asteroid = CelestialObject(self.win, x, y, w, h, image=image, layer=self.layer, parent=self, type="asteroid")

    def create_comets(self):
        for i in range(int(self.amount / 350)):
            select = random.randint(0, len(self.comet_images.keys()) - 1)
            image = self.comet_images[select]
            w = image.get_rect().width
            h = image.get_rect().height
            x = random.randint(self.left_end, self.right_end)
            y = random.randint(self.top_end, self.bottom_end)

            comet = CelestialObject(self.win, x, y, w, h, image=image, layer=self.layer, parent=self, type="comet")

    def create_universe(self):

        self.create_stars()

        self.create_galaxys()
        self.create_nebulaes()
        self.create_comets()
        self.create_asteroids()

        self.universe = self.star + self.pulsating_star + self.galaxy + self.nebulae + self.comet + self.asteroid
        # self.universe = self.pulsating_star
        # print("Scene Objects: ", len(self.universe))

    def draw(self):
        for celestial_object in self.universe:
            limit_positions(celestial_object)
            celestial_object.draw()

    def listen(self, events):
        return
        # resize = 10
        # for event in events:
        #     if event.type == pygame.MOUSEWHEEL:
        #         if event.y == -1 or event.y == 1:
        #             for celestial_object in self.universe:
        #                 celestial_object.setWidth(celestial_object.getWidth() + event.y * resize)
        #                 celestial_object.setHeight(celestial_object.getHeight() + event.y * resize)
        #                 celestial_object.rescale()
        #                 #print (celestial_object.getWidth, celestial_object.getHeight())

#
# pygame.init()
# width, height = 1920,1080
# win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
# bg =  Background(width, height, win)
# bg.create_stars(int(width/15))
# run = True
#
# while run:
#     for e in pygame.event.get():
#         if e.type == pygame.QUIT:
#             run = False
#
#     bg.draw()
#     pygame.display.update()
#
#
# pygame.quit()
# sys.exit()
