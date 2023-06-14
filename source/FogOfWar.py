import pygame

import source.Globals
from source.Button import Moveable
from source.WidgetHandler import WidgetBase


class FogOfWar(WidgetBase, Moveable):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        Moveable.__init__(self, x, y, width, height, kwargs)
        self.layer = kwargs.get("layer", 2)
        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey((60, 60, 60))

    def draw(self):
        self.win.blit(self.surface, (self._x, self._y))

    def listen(self, events):
        pass

    def draw_fog_of_war(self, obj, **kwargs):
        """
        draws the fog of war circle based on the fog of war raduis of the obj
        :param obj:
        :param kwargs:
        :return:
        """
        if source.Globals.app == None:  # bullshit here, bad initializing
            return
        x, y = kwargs.get("x", obj.getX() + obj.getWidth() / 2), kwargs.get("y", obj.getY() + obj.getHeight() / 2)

        # recalculate position because fog of war surface is moved too
        x = x - source.Globals.app.fog_of_war.getX()
        y = y - source.Globals.app.fog_of_war.getY()
        radius = kwargs.get("radius", obj.fog_of_war_radius)
        pygame.draw.circle(surface=self.surface, color=(60, 60, 60), center=(
            x, y), radius=radius, width=0)
