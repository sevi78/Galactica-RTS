import pygame as pg
import pygame.transform

import source
from source import Globals
from source.AppHelper import debug_positions

from source.WidgetHandler import *

# Zoom with mousewheel, pan with left mouse button

SCREEN_WIDTH = 920  # sprite_sheet.get_rect().size[0]
SCREEN_HEIGHT = 800  # sprite_sheet.get_rect().size[1]
WORLD_WIDTH = 2000
WORLD_HEIGHT = 2000
# screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()


class PanZoomHandler:
    def __init__(self, screen, screen_width, screen_height, world_width, world_height, **kwargs):
        self.key_pressed = False
        self.zoomable = False
        self.parent = kwargs.get("parent")
        self.zoomable_widgets = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.legacy_screen = pg.Surface((self.screen_width, self.screen_height), pygame.RESIZABLE)
        self.screen = screen
        self.new_screen = None

        self.world_width = world_width
        self.world_height = world_height
        self.world_right = 0
        self.world_left = 0
        self.world_top = 0
        self.world_bottom = 0
        self.world_offset_x = 0
        self.world_offset_y = 0

        self.mouseworld_y_before = None
        self.mouseworld_x_before = None
        self.mouseworld_y_after = None
        self.mouseworld_x_after = None

        self.scale_up = 1.2
        self.scale_down = 0.8

        self.tab = 1
        self.zoom = 1
        self.zoom_max = 20
        self.zoom_min = 0.1

        self.update_screen = True
        self.panning = False
        self.pan_start_pos = None

    def listen(self, events):
        # print ("panning_and_zooming:", self.parent.planets)
        # Mouse screen coords
        mouse_x, mouse_y = pg.mouse.get_pos()

        # event handler
        for event in events:
            # ctrl:
            if event.type == pygame.KEYDOWN:
                if event.key == 1073742048:  # ctrl:
                    self.key_pressed = True

            elif event.type == pygame.KEYUP:
                if event.key == 1073742048:
                    self.key_pressed = False

            # if not self.key_pressed:
            #     return

            elif event.type == pg.MOUSEBUTTONDOWN:
                # self.set_zoom(event, mouse_x, mouse_y)
                if event.button == 4 or event.button == 5:
                    # X and Y before the zoom
                    self.mouseworld_x_before, self.mouseworld_y_before = self.screen_2_world(mouse_x, mouse_y)

                    # ZOOM IN/OUT
                    if event.button == 4 and self.zoom < self.zoom_max:
                        self.zoom *= self.scale_up
                    elif event.button == 5 and self.zoom > self.zoom_min:
                        self.zoom *= self.scale_down

                    # X and Y after the zoom
                    self.mouseworld_x_after, self.mouseworld_y_after = self.screen_2_world(mouse_x, mouse_y)

                    # Do the difference between before and after, and add it to the offset
                    self.world_offset_x += self.mouseworld_x_before - self.mouseworld_x_after
                    self.world_offset_y += self.mouseworld_y_before - self.mouseworld_y_after
                    self.tab = 1

                    debug_positions(self.mouseworld_x_after, self.mouseworld_y_after, "brown", "pan_zoom.listen: self.mouseworld_x_after, self.mouseworld_y_after: ", 13)
                    debug_positions(self.mouseworld_x_before, self.mouseworld_y_before, "orange", "pan_zoom.listen: self.mouseworld_x_before, self.mouseworld_y_before: ", 25)
                    debug_positions(self.world_offset_x, self.world_offset_y, "pink", "pan_zoom.listen: self.world_offset_x, self.world_offset_y: ", 15)

                elif event.button == 1:
                    # PAN START
                    self.panning = True
                    self.pan_start_pos = mouse_x, mouse_y

                    self.tab = 1

            elif event.type == pg.MOUSEBUTTONUP:

                if event.button == 1 and self.panning:
                    # PAN STOP
                    self.panning = False
                    self.tab = 2
                elif event.button == 4 or event.button == 5:
                    self.tab = 2

            if self.panning:
                if source.Globals.enable_pan:
                    self.pan(mouse_x, mouse_y)

            #print("MBU ", self.tab)
            # Draw the screen
            if self.tab == 1:  # and self.key_pressed == True:
                if source.Globals.enable_zoom:
                    self.pan_and_zoom()


    def pan_and_zoom(self):
        """
        the main function:
        iterates over the lists of object to be pan_zoomed
        parent is the app
        every zoomable object nedds to have an attribute "zoomable" and must be registred in one of these lists:

        """
        # print("pan_and_zoom: ")
        for zoomable_object in self.parent.planets:
            self.set_position_and_size(zoomable_object)
            new_size = (zoomable_object.size_x * self.zoom, zoomable_object.size_y * self.zoom)
            zoomable_object.image = pygame.transform.scale(zoomable_object.planet_image, new_size)
            zoomable_object.set_center()

        for zoomable_object in self.parent.universe.universe:
            self.set_position_and_size(zoomable_object)
            if zoomable_object.image_raw:
                new_size = (zoomable_object.size_x * self.zoom, zoomable_object.size_y * self.zoom)
                zoomable_object.image = pygame.transform.scale(zoomable_object.image_raw, new_size)

        for zoomable_object in self.parent.ships:
            x, y = self.world_2_screen(zoomable_object.x, zoomable_object.y)
            if zoomable_object.moving:
                nx, ny = self.screen_2_world((zoomable_object.x - self.world_offset_x) * self.zoom, (
                            zoomable_object.y - self.world_offset_y) * self.zoom)
                zoomable_object._x = nx
                zoomable_object._y = ny
            else:

                zoomable_object.setX(x - (zoomable_object.getWidth() / 2))
                zoomable_object.setY(y - (zoomable_object.getHeight() / 2))
                zoomable_object.setWidth(zoomable_object.size_x * self.zoom)
                zoomable_object.setHeight(zoomable_object.size_y * self.zoom)
                zoomable_object.image_rot = pygame.transform.scale(zoomable_object.image_raw, (
                zoomable_object.getWidth() * self.zoom, zoomable_object.getHeight() * self.zoom))
            # zoomable_object.image_rot_rect = zoomable_object.image_raw.get_rect()

            # nx,ny = self.screen_2_world(zoomable_object._x-self.world_offset_x, zoomable_object._y-self.world_offset_x)

        # print (self.parent.collectables, self.parent)
        for zoomable_object in self.parent.collectables:
            self.set_position_and_size(zoomable_object)
            zoomable_object.image = pygame.transform.scale(zoomable_object.image_raw,
                (zoomable_object.getWidth() * self.zoom, zoomable_object.getHeight() * self.zoom))

    def set_position_and_size(self, zoomable_object):
        x, y = self.world_2_screen(zoomable_object.x, zoomable_object.y)
        zoomable_object.setX(x - zoomable_object.getWidth() / 2)
        zoomable_object.setY(y - zoomable_object.getHeight() / 2)
        zoomable_object.setWidth(zoomable_object.size_x * self.zoom)
        zoomable_object.setHeight(zoomable_object.size_y * self.zoom)

    def set_zoom(self, event, mouse_x, mouse_y):
        if event.button == 4 or event.button == 5:
            # X and Y before the zoom
            self.mouseworld_x_before, self.mouseworld_y_before = self.screen_2_world(mouse_x, mouse_y)

            # ZOOM IN/OUT
            if event.button == 4 and self.zoom < self.zoom_max:
                self.zoom *= self.scale_up
            elif event.button == 5 and self.zoom > self.zoom_min:
                self.zoom *= self.scale_down

            # X and Y after the zoom
            self.mouseworld_x_after, self.mouseworld_y_after = self.screen_2_world(mouse_x, mouse_y)

            # Do the difference between before and after, and add it to the offset
            self.world_offset_x += self.mouseworld_x_before - self.mouseworld_x_after
            self.world_offset_y += self.mouseworld_y_before - self.mouseworld_y_after

            # set grid_width
            self.set_grid_width()
        else:
            self.tab = 2

        if event.button == 1:
            # PAN START
            self.panning = True
            self.pan_start_pos = mouse_x, mouse_y

    def pan(self, mouse_x, mouse_y):
        # Pans the screen if the left mouse button is held
        self.world_offset_x -= (mouse_x - self.pan_start_pos[0]) / self.zoom
        self.world_offset_y -= (mouse_y - self.pan_start_pos[1]) / self.zoom
        self.pan_start_pos = mouse_x, mouse_y

    def world_2_screen(self, world_x, world_y):
        screen_x = (world_x - self.world_offset_x) * self.zoom
        screen_y = (world_y - self.world_offset_y) * self.zoom
        return [screen_x, screen_y]

    def screen_2_world(self, screen_x, screen_y):
        world_x = (screen_x / self.zoom) + self.world_offset_x
        world_y = (screen_y / self.zoom) + self.world_offset_y
        return [world_x, world_y]

#
# pan_zoom_handler = PanZoomHandler(screen, SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT)
# zoomable_widget = Zoomable_Widget(screen, 100,100,100,100,isSubWidget=False,image=sprite_sheet, onClick=lambda: print("ok"))
# pan_zoom_handler.zoomable_widgets.append(zoomable_widget)
#
# # game loop
# loop = True
# while loop:
#     # Banner FPS
#     #pg.display.set_caption('(%d FPS)' % (clock.get_fps()))
#
#     # events, listen
#     events = pg.event.get()
#     pan_zoom_handler.listen(events)
#
#     # looping
#     update(events)
#     pg.display.update()
#     clock.tick(600)
