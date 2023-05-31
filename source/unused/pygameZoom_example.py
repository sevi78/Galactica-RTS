from pprint import pprint

import pygame
import math
import sys
from pygameZoom import PygameZoom
from pygame_widgets import update
from pygame_widgets.util import drawText

import Globals
import source
from WidgetHandler import WidgetBase


class Planet_Image(WidgetBase):
    def __init__(self, win):
        WidgetBase.__init__(self, self.parent.win, 100,100,50,50, False)
        pass
    def listen(self, events):
        pass

    def draw(self):
        pass


class Debugger:
    def draw_dict(self, **kwargs):
        obj = kwargs.get("obj", self)
        color = Globals.colors.frame_color
        font = pygame.font.SysFont(None, 18)
        win = self.WIN
        text_spacing = 20
        text_id = 1

        for i in obj.__dict__:
            pprint("_ _ _ _ _ _ _ _ _ _ _ _ ")
            pprint("debugging: ")
            pprint("_______________________")
            pprint(obj.__dict__)




            text = str(i) + ": " + str(getattr(obj, i))
            drawText(self.WIN, text, color, (
            (100,100 + text_spacing * text_id), (400, 500)), font, "left")
            text_id += 1
            
class Window(Debugger):
    def __init__(self):
        pygame.init()
        Debugger.__init__(self)
        self.WIDTH, self.HEIGHT = 1500, 800
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.CLOCK = pygame.time.Clock()
        self.FPS = 30
        self.run = True
        self.pygameZoom = PygameZoom(500, 400)
        self.pygameZoom.set_background((255, 0, 0))
        self.x = 0
        self.y = 0

        #self.planet = Planet_Image()
        self.loop()

    def drawTree(self, a, b, pos, deepness):
        if deepness:
            c = a + int(math.cos(math.radians(pos)) * deepness * 10.0)
            d = b + int(math.sin(math.radians(pos)) * deepness * 10.0)
            self.pygameZoom.draw_line((127, 255, 0), a, b, c, d, 1)
            self.drawTree(c, d, pos - 25, deepness - 1)
            self.drawTree(c, d, pos + 25, deepness - 1)

    def refresh_window(self):
        self.WIN.fill(0)
        # self.drawTree(500, 800, -90, 12)
        self.pygameZoom.draw_ellipse((255, 255, 0), (200, 200, 100, 100))
        self.pygameZoom.draw_circle((255, 255, 0), 200, 200, 20)
        self.pygameZoom.draw_rect((0, 0, 0), 100, 100, 100, 100)
        self.pygameZoom.draw_line((255, 255, 255), 0, 0, 200, 200)
        self.pygameZoom.draw_polygon((0,0,255), [(200,400),(300,2),(400,400)])
        surface = pygame.image.load("C:\\Users\\sever\\Documents\\Galactica2.8\\pictures\\planets\\zork_150x150.png")
        self.pygameZoom.blit(surface, (100, 100))
        #self.drawTree(10,20,100,15)

        self.pygameZoom.render(self.WIN, (300, 300))
        self.draw_dict(obj=self.pygameZoom)

        pygame.display.update()


    def events(self):
        for e in pygame.event.get():
            update(e)
            if e.type == pygame.QUIT:
                self.run = False

    def loop(self):
        while self.run:
            self.refresh_window()
            self.events()
            self.CLOCK.tick(self.FPS)
        pygame.quit()
        sys.exit()


win = Window()