import pygame as pg
import pygame.transform

import source
from source.gui.WidgetHandler import *
from source.utils import debug_positions

# Zoom with mousewheel, pan with left mouse button



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
        self.zoom_max = 1.5
        self.zoom_min = 0.0001

        self.update_screen = True
        self.panning = False
        self.pan_start_pos = None

    def listen(self, events):
        # Mouse screen coords
        mouse_x, mouse_y = pg.mouse.get_pos()
        #print (self.zoom)

        # event handler
        for event in events:

            if event.type == pg.MOUSEBUTTONDOWN:
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
                if source.utils.Globals.enable_pan:
                    self.pan(mouse_x, mouse_y)


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

    def navigate_to(self, obj, **kwargs):
        """
        sets the world offset to the objects position
        """

        # get ship to navigate to if not object is set
        ship = kwargs.get("ship", None)

        if not obj and ship:
            obj = [i for i in self.parent.ships if i.name == ship][0]

        # set position
        self.world_offset_x, self.world_offset_y = self.screen_2_world(obj.getX() - self.screen_width / 2, obj.getY() - self.screen_height / 2)

        # set info panel
        obj.set_info_text()
