from pprint import pprint

import pygame
from pygame_widgets.util import drawText

import source.Globals
from source.AppHelper import limit_positions
from source.Colors import Colors
from source.WidgetHandler import WidgetHandler, WidgetBase



class PanZoom:
    def __init__(self):
        self.sx = 0
        self.sy = 0
        self.wx = 0
        self.wy = 0
        self.ox = 0
        self.oy = 0

    def world_to_screen(self):
        self.sx = self.wx - self.ox
        self.sx = self.wx - self.oy

    def screen_to_world(self):
        self.sx = self.wx + self.ox
        self.sx = self.wx + self.oy






