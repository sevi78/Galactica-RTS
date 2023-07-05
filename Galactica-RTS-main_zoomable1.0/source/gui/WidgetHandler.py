from abc import abstractmethod, ABC
from pprint import pprint

import pygame
from pygame import Vector2
from pygame.event import Event

import source.utils.Globals
from source import utils
from source.utils import get_distance

from source.utils.saveload import *


class Debugger:
    def draw_dict(self):
        for i in self.__dict__:
            pprint("_ _ _ _ _ _ _ _ _ _ _ _ ")
            pprint("debugging: ")
            pprint("_______________________")
            pprint(self.__dict__)


class WidgetBase(ABC, Debugger):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        """ Base for all widgets

        :param win: Surface on which to draw
        :type win: pygame.Surface
        :param x: X-coordinate of top left
        :type x: int
        :param y: Y-coordinate of top left
        :type y: int
        :param width: Width of button
        :type width: int
        :param height: Height of button
        :type height: int
        """

        self.win = win
        # world position
        self.x = x
        self.y = y

        # screen position
        self._x = x
        self._y = y

        self._width = width
        self._height = height
        self._isSubWidget = isSubWidget
        self.size_x = width
        self.size_y = height
        self.enable_orbit = False
        self.orbit_distance = 0
        self.orbit_speed =  0.007
        self.orbit_angle = 0
        self.offset = Vector2(0, 0)


        self._hidden = False
        self._disabled = False
        self.zoomable = False
        self.property = kwargs.get("property", None)
        self.layer = kwargs.get("layer", None)
        self.layers = kwargs.get("layers", None)

        self.image = kwargs.get("image", None)
        self.image_raw = kwargs.get("image", None)
        self.debug = False


        if isSubWidget:
            self.hide()

        WidgetHandler.addWidget(self)

    def __del__(self):
        """ pffff  how to clean delete ?? still some junk in the memory """
        for key, widget_list in WidgetHandler.layers.items():
            if self in widget_list:
                widget_list.remove(self)

    def load_settings(self):
        settings = load_file("settings")

        for key, value in settings.items():
            if key in self.__dict__.items():
                setattr(self,key)
                #print (getattr(self, key ))
                widgets = WidgetHandler.get_all_widgets()

                for i in widgets:
                    if hasattr(i, key):
                        setattr(i, key, value)

                #print ([str(i.name) + str(i.moveable) for i in widgets if hasattr(i, "enable_orbit")])

    @abstractmethod
    def listen(self, events):
        pass

    @abstractmethod
    def draw(self, **kwargs):
        pass

    def __repr__(self):
        return f'{type(self).__name__}(x = {self._x}, y = {self._y}, width = {self._width}, height = {self._height})'

    def contains(self, x, y):
        return (self._x < x - self.win.get_abs_offset()[0] < self._x + self._width) and \
            (self._y < y - self.win.get_abs_offset()[1] < self._y + self._height)

    def hide(self):
        self._hidden = True


    def show(self):
        self._hidden = False

    def disable(self):
        self._disabled = True

    def enable(self):
        self._disabled = False

    def isSubWidget(self):
        return self._isSubWidget

    def moveX(self, x):
        self._x += x

    def moveY(self, y):
        self._y += y

    def get(self, attr):
        """Default setter for any attributes. Call super if overriding

        :param attr: Attribute to get
        :return: Value of the attribute
        """
        if attr == 'x':
            return self._x

        if attr == 'y':
            return self._y

        if attr == 'width':
            return self._width

        if attr == 'height':
            return self._height

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def get_position(self):
        return (self._x, self._y)

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    def isVisible(self):
        return not self._hidden

    def isEnabled(self):
        return not self._disabled

    def set(self, attr, value):
        """Default setter for any attributes. Call super if overriding

        :param attr: Attribute to set
        :param value: Value to set
        """
        if attr == 'x':
            self._x = value

        if attr == 'y':
            self._y = value

        if attr == 'width':
            self._width = value

        if attr == 'height':
            self._height = value

    def setX(self, x):
        self._x = x

    def setY(self, y):
        self._y = y

    def set_screen_size(self):
        panzoom = source.utils.Globals.app.pan_zoom_handler
        zoom = panzoom.zoom

        # get new_size size
        new_size = (self.size_x * zoom, self.size_y * zoom)

        # set new image size
        if hasattr(self, "image_raw") and hasattr(self, "image"):
            if self.image:
                self.image = pygame.transform.scale(self.image_raw, new_size)

        # only for ships
        if hasattr(self,"image_rot"):
            self.image_rot = pygame.transform.scale(self.image_raw, new_size)
            self.image_rot_rect = self.image_raw.get_rect()

        # set new size
        self.setWidth(new_size[0] * zoom)
        self.setHeight(new_size[1] * zoom)

    def setWidth(self, width):
        self._width = width

    def setHeight(self, height):
        self._height = height

    def setIsSubWidget(self, isSubWidget):
        self._isSubWidget = isSubWidget
        if isSubWidget:
            WidgetHandler.removeWidget(self)
        else:
            WidgetHandler.addWidget(self)

    def set_orbit_object(self, obj):
        try:
            self.orbit_object = obj
            self.orbit_distance = get_distance(self.center, obj.center)
            self.offset.x = self.orbit_object.center[0] - self.center[0]
            self.offset.y = self.orbit_object.center[1] - self.center[1]

            self.orbit_speed = (self.offset.x / self.orbit_distance) * (source.utils.Globals.time_factor / 1000) * source.utils.Globals.game_speed
        except ZeroDivisionError:
            print ("set_orbit_object error: ", self.name, obj.name)

    def orbit(self, **kwargs):
        if not self.orbit_object:
            return

        self.orbit_speed = (self.offset.x / self.orbit_distance) * (source.utils.Globals.time_factor / 1000) * source.utils.Globals.game_speed#1
        self.orbit_angle += self.orbit_speed

        if hasattr(self, "property"):
            if self.property == "ship":
                orbit_center = self.orbit_object._x, self.orbit_object._y

            else:
                orbit_center = self.orbit_object.x, self.orbit_object.y


        orbit_point = orbit_center - self.offset.rotate(self.orbit_angle)

        return orbit_point

    def set_screen_position(self):
        panzoom = source.utils.Globals.app.pan_zoom_handler
        zoom = panzoom.zoom
        offset_x = panzoom.world_offset_x
        offset_y = panzoom.world_offset_y

        # get new coordinates
        if self.zoomable:
            x, y = panzoom.world_2_screen(self.x, self.y)
        else:
            x, y = self.x, self.y

        # if orbiting get position from orbit
        if hasattr(self, "enable_orbit"):
            if self.enable_orbit:
                if hasattr(self, "property"):
                    if self.property ==" ship":
                        orbit_point = panzoom.screen_2_world(self.orbit_object.center)
                    else:
                        orbit_point = self.orbit()
                        x, y = panzoom.world_2_screen(orbit_point[0], orbit_point[1])


        # if it is a ship
        if hasattr(self, "image_rot"):
            if self.target:# and not self.enable_orbit:
                if hasattr(self.target, "_x"):
                    tx, ty = self.target._x, self.target._y
                else:
                    #tx, ty = panzoom.screen_2_world(self.target[0], self.target[1])
                    tx, ty = self.target


                dx = (self._x - tx)
                dy = (self._y - ty)
                #dist   = get_distance((self._x, self._y),(tx, ty))

                self.x -= dx / utils.Globals.fps / self.get_zoom() * self.speed * utils.Globals.game_speed
                self.y -= dy / utils.Globals.fps / self.get_zoom() * self.speed * utils.Globals.game_speed


                # xw,yw =  panzoom.world_2_screen(dx, dy)
                # self.x -= xw * self.speed * utils.Globals.game_speed
                # self.y -= yw * self.speed * utils.Globals.game_speed

        # if it is button
        if hasattr(self, "ui_parent"):
            if self.ui_parent:
                x,y = self.ui_parent.getX(), self.ui_parent.getY()

        # set new position
        self.setX(x - self.getWidth() / 2 )
        self.setY(y - self.getHeight() / 2)

        # set new size
        self.set_screen_size()
        if hasattr(self, "set_center"):
            self.set_center()

    def get_zoom(self):
        if utils.Globals.app:
            return utils.Globals.app.pan_zoom_handler.zoom
        else:
            return 1



class WidgetHandler:
    print("WidgetHandler: init")
    layers = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: [], 14: []}
    layer_switch = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0}

    for key, value in layer_switch.items():
        layer_switch[key] = 1

    layer_switch["2"] = 0

    # print (layers)
    """
    layers: 
    0 = background
    1 = universe
    2 = 
    3 = planets
    4 = 
    5 = fog of war
    6 = 
    7 =
    8 = ships
    9 = ui 
    """

    @staticmethod
    def main(events: [Event]) -> None:
        # all_widgets = WidgetHandler.get_all_widgets()
        #
        # print(all_widgets)
        WidgetHandler.set_visible(events)
        # 0:[...]
        for key, widgetlist in WidgetHandler.layers.items():
            # print ("WidgetHandler.layers.keys():", key, value)
            # get widget
            for widget in widgetlist:
                layer = widget.layer

                # if no layer defined, use layer 10
                if str(layer) == "None":
                    layer = 10

                # if layer is on
                if WidgetHandler.layer_switch[str(layer)] == 1:
                    widget.draw()

                    if widget.isSubWidget:
                        widget.listen(events)

    @staticmethod
    def get_all_widgets():
        all_widgets = []
        for layer in WidgetHandler.layers.values():
            all_widgets.extend(layer)
        return all_widgets

    @staticmethod
    def addWidget(widget: WidgetBase) -> None:
        if str(widget.layer) == "None":
            # print("non layered: ", widget)
            WidgetHandler.layers[9].append(widget)
        else:
            WidgetHandler.layers[widget.layer].append(widget)

    def set_visible(events):
        numbers = [49, 50, 51, 52, 53, 54, 55, 56, 57, 48]
        others = [39]  # ,94]
        key = None

        for event in events:
            if event.type == pygame.KEYDOWN:
                # 1-0
                if event.key in numbers:
                    number = event.key - 48
                    key = str(number)

                    # set value
                    if WidgetHandler.layer_switch[key] == 0:
                        WidgetHandler.layer_switch[key] = 1
                        print("layer: " + key, WidgetHandler.layer_switch[key], WidgetHandler.layers[int(key)])
                        return
                    if WidgetHandler.layer_switch[key] == 1:
                        WidgetHandler.layer_switch[key] = 0
                        print("layer: " + key, WidgetHandler.layer_switch[key])
                        print("layer objects: ", len(WidgetHandler.layers[int(key)]))
                        return

                # next

                # elif event.key in others:
                #     key = "9"
                #
                #     # set value
                #     if WidgetHandler.layer_switch[key] == 0:
                #         WidgetHandler.layer_switch[key] = 1
                #         return
                #     if WidgetHandler.layer_switch[key] == 1:
                #         WidgetHandler.layer_switch[key] = 0
                #         return

        # print(WidgetHandler.layer_switch)
