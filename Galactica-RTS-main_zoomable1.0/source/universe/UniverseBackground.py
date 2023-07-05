import math
import random

import pygame
from pygame import gfxdraw

import source.utils.Globals
from source import utils
from source.gui.Button import Moveable
from source.gui.WidgetHandler import WidgetBase
from source.utils import limit_positions, images, colors
from source.utils.Globals import pictures_path


class CelestialObject(WidgetBase, Moveable):
    possible_directions = [-1, 1]
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        Moveable.__init__(self, x, y, width, height, kwargs)

        self.rotation = 0
        self.rotation_direction = random.choice(CelestialObject.possible_directions)
        self.rotation_speed = random.uniform(0.1,1.0)
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
            # self.image_rect.x = x
            # self.image_rect.y = y
            self.image_rect.center = (x,y)

        self.parent = kwargs.get("parent")
        self.ui_parent = kwargs.get("ui_parent")
        self.zoomable = True

        # append to list
        getattr(self.parent, self.type).append(self)

    def listen(self, events):
        pass

    def rot_center(self, image, angle, x, y):

        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

        return rotated_image, new_rect

    def draw(self):
        self.set_screen_position()
        if not self._hidden:
            if self.image:
                if self.type == "asteroid":

                    #image = pygame.transform.rotate(self.image,self.rotation )


                    rotated_image, new_rect =  self.rot_center(self.image, self.rotation,self._x, self._y  )

                    self.image = rotated_image
                    self.image_rect = new_rect
                    self.win.blit(self.image, (self.image_rect))
                    self.rotation += self.rotation_speed * self.rotation_direction
                    return


                self.image_rect.x = self.getX() + self.image.get_size()[0] / 2 * self.get_zoom()
                self.image_rect.y = self.getY() + self.image.get_size()[1] / 2 * self.get_zoom()
                self.win.blit(self.image, (self.image_rect))

            elif self.type == "pulsating_star":
                t = pygame.time.Clock().get_time() * 0.001
                s = 2 * math.pi * random.random()
                x, y = self.getX(), self.getY()

                flicker = s
                c = int(127 * max(0.5, 1 + math.cos(t + flicker)))

                gfxdraw.pixel(self.win, int(x), int(y), (c, c, c))

            elif self.type == "quadrant":
                if utils.Globals.show_grid:
                    x,y = utils.Globals.app.pan_zoom_handler.world_2_screen(self.x , self.y)
                    pygame.draw.rect(self.win, colors.frame_color, (
                    x,y, self.getWidth() / self.get_zoom(), self.getHeight() / self.get_zoom()), 1)

            else:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                # pygame.draw.circle(self.win, color, (self._x + self._width , self._y), self.width)
                pygame.draw.lines(self.win, color, True, [(self._x + 1, self._y), (self._x + 1, self._y)])




class Universe(WidgetBase, Moveable):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        Moveable.__init__(self, x, y, width, height, kwargs)

        self.parent = kwargs.get("parent")
        self.layer = kwargs.get("layer", 0)
        self.amount = int(math.sqrt(math.sqrt(width)) * source.utils.Globals.settings["universe_density"])

        # define borders
        self.left_end = 0  # -self.getWidth()
        self.right_end = self.getWidth()
        self.top_end = 0  # -self.getHeight()
        self.bottom_end = self.getHeight()

        # images
        self.star_images = {
            0: images[pictures_path]["stars"]["star_30x30.png"],
            1: images[pictures_path]["stars"]["star_50x50.png"],
            2: images[pictures_path]["stars"]["star1_50x50.png"],
            3: images[pictures_path]["stars"]["star2_100x100.png"]
            }

        self.asteroid_images = {
            0: images[pictures_path]["celestial objects"]["asteroid_40x33.png"],
            }

        self.comet_images = {
            0: images[pictures_path]["celestial objects"]["comet_90x38.png"]
            }

        self.nebulae_images = {
            0: images[pictures_path]["celestial objects"]["nebulae_300x300.png"]
            }

        self.galaxy_images = {
            0: images[pictures_path]["celestial objects"]["galaxy_.png"],
            1: images[pictures_path]["celestial objects"]["galaxy3_small.png"]
            }

        # drawing lists
        self.star = []
        self.pulsating_star = []
        self.asteroid = []
        self.nebulae = []
        self.galaxy = []
        self.comet = []
        self.universe = []
        self.quadrant = []

        # create universe
        self.create_universe()

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

        # puslatoing stars
        for i in range(int(self.amount / 3)):
            x = random.randint(self.left_end, self.right_end)
            y = random.randint(self.top_end, self.bottom_end)
            w = 1
            star = CelestialObject(self.win, x, y, w, w, layer=self.layer, parent=self, type="pulsating_star")

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

    def create_quadrant(self):
        quadrant_amount = 10
        quadrant_size_x = 2000
        quadrant_size_y = 2000
        for x in range(quadrant_amount):
            for y in range(quadrant_amount):
                w,h = quadrant_size_x, quadrant_size_y
                quadrant = CelestialObject(
                    self.win, quadrant_size_x * x, quadrant_size_y * y, w, h,
                    image=None, layer=0, parent=self, type="quadrant")

    def create_universe(self):
        self.create_stars()
        self.create_galaxys()
        self.create_nebulaes()
        self.create_comets()
        self.create_asteroids()
        self.create_quadrant()

        self.universe = self.star + self.pulsating_star + self.galaxy + self.nebulae + self.comet + self.asteroid + self.quadrant
        # self.universe = self.pulsating_star
        # print("Scene Objects: ", len(self.universe))

    def draw(self):
        for celestial_object in self.universe:
            if not celestial_object.type == "quadrant":
                limit_positions(celestial_object)
            celestial_object.draw()
            # if celestial_object.type == "quadrant":
            #     if not celestial_object._hidden:
            #         print (celestial_object.getX())

        #print (len([i for i in self.universe if i.type == "quadrant" and not i._disabled]))
        #print ([i.layer for i in self.universe if i.type == "quadrant"])

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
