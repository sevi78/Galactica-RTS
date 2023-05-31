import pygame

import source.Globals
from source.Button import Moveable
from source.Globals import WIDTH, HEIGHT
from source.WidgetHandler import WidgetBase


class BackgroundImage(WidgetBase, Moveable):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        Moveable.__init__(self, x, y, width, height, kwargs)
        self.layer = kwargs.get("layer", 0)
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.surface.set_colorkey((60, 60, 60))
        self.image = kwargs.get("image", None)
        self.image = pygame.transform.scale(self.image, (self.win.get_width(), self.win.get_height()))
        self.color = source.Globals.colors.background_color

    def draw(self):
        if source.Globals.draw_background_image:
            self.win.blit(self.image, (self.x,self.y))
        else:
            pygame.draw.rect(self.win, self.color, (0,0, self._width, self._height))

    def listen(self, events):
        pass
