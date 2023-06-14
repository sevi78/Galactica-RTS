import pygame
from pygame.locals import MOUSEMOTION

import source.Globals
from source.WidgetHandler import WidgetBase


class ToolTip(WidgetBase):
    def __init__(self, surface, x, y, width, height, color, text_color, isSubWidget, parent, **kwargs):
        super().__init__(surface, x, y, width, height, isSubWidget, **kwargs)
        self.layer = kwargs.get("layer", 4)
        self.visible = False
        self.win = surface
        self.color = color
        self.text_color = text_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size = (self.width, self.height)
        self.rect_filled = None
        self.parent = parent

        # text
        self._text = ""
        self.font = None
        self.text_img = None
        self.txt_rect = None

    @property
    def text(self, text):
        return self._text
    @text.setter
    def text(self, value):
        if value != self._text:
            self._text = value

    def move(self, events):

        if self.visible:
            for event in events:
                if event.type == MOUSEMOTION:
                    if self.text_img:
                        # limit position x
                        max_x = pygame.display.get_surface().get_width()
                        x = event.pos[0] + self.text_img.get_width() / 2
                        min_x = 0
                        x1 = event.pos[0] - self.text_img.get_width() / 2

                        if x > max_x:
                            self.x = max_x - self.text_img.get_width() - 10
                        elif x1 < min_x:
                            self.x = min_x
                        # else center
                        else:
                            self.x = event.pos[0] - self.text_img.get_width() / 2
                            self.y = event.pos[1] + self.text_img.get_height()
        else:
            self.x = -1000
            self.y = -1000

    def get_text(self):
        self._text = source.Globals.tooltip_text
        if self._text != "":
            self.visible = True
        else:
            self.visible = False

    def draw_bordered_rect(self, x, y):
        for i in range(4):
            pygame.draw.rect(self.win, (0, 0, 0), (x - i, y - i, 155, 155), 5)

    def draw(self):
        self.font = pygame.font.SysFont(None, 18)
        self.text_img = self.font.render(self._text, True, self.text_color)
        self.width = self.text_img.get_width() + 10
        self.height = self.text_img.get_height() + 10
        self.size = (self.width, self.height)
        self.rect_filled = pygame.surface.Surface(self.size)
        self.rect_filled.set_alpha(23)
        self.win.blit(self.rect_filled, (self.x, self.y))
        self.win.blit(self.text_img, (self.x + 5, self.y + 5))
        # self.draw_bordered_rect(self.x, self.y)

    def listen(self, events):
        pass

    def update(self, events):
        self.get_text()
        self.move(events)
        self.draw()
