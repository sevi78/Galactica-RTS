import pygame

import source.utils.Globals
from source.gui.Button import Moveable
from source.gui.WidgetHandler import WidgetBase
from source.utils import colors
from source.utils.Globals import WIDTH, HEIGHT


class BackgroundImage(WidgetBase, Moveable):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        Moveable.__init__(self, x, y, width, height, kwargs)
        self.layer = kwargs.get("layer", 0)
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.surface.set_colorkey((60, 60, 60))
        self.surface.set_alpha(0)
        self.image = kwargs.get("image", None)
        self.image = pygame.transform.scale(self.image, (self.win.get_width(), self.win.get_height()))
        self.color = colors.background_color

    def draw(self):
        if source.utils.Globals.draw_background_image:
            self.win.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(self.win, self.color, (0, 0, self._width, self._height))

    def listen(self, events):
        pass
