import sys

import pygame
from pygame_widgets.util import drawText

import Globals

WIDTH, HEIGHT = 800, 600
world_size = (500,500)
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.init()

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


class Zoom():
    def __init__(self, width, height, world_size):

        self.mouse_position = (0,0)
        self.zoom = 1.0
        self.mouse_pressed = False
        self.mouse_wheel = False
        self.key_pressed = False
        self.world_position = (0,0)
        self.screen_position = (0,0)
        self.world_size = world_size


    def listen(self, events):
        self.mouse_position = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

            # ctrl:
            if event.type == pygame.KEYDOWN:
                if event.key == 1073742048:
                    self.key_pressed = True

            # ctrl release
            elif event.type == pygame.KEYUP:
                if event.key == 1073742048:
                    self.key_pressed = False


            # mouse all buttons
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False

            # mouse wheel
            if event.type == pygame.MOUSEWHEEL:
                if event.y == -1 or event.y == 1:
                    self.zoom += event.y / 100
                    self.mouse_wheel = True
            else:
                self.mouse_wheel = False

        # both, then act
        if self.key_pressed and self.mouse_pressed:
            self.set_screen_position()

    def draw(self):
        spacing = 26
        y = spacing
        for i in self.__dict__:
            text = drawText(win, str(i), (130, 230, 130), (
            (spacing, y), (200, 26)), pygame.font.SysFont(None, 18), "left")
            y += spacing

        # srcreen
        pygame.draw.rect(win, (222, 222, 222), (
        self.screen_position, (pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height())), 1)

        # world
        pygame.draw.rect(win, (222, 222, 122), (
            self.world_position,
            (self.world_size[0], self.world_size[1])), 1)

    def set_screen_position(self):
        mouse_offset_x, mouse_offset_y  = self.mouse_position[0] - self.world_position[0], self.mouse_position[1] - self.world_position[1]
        center_x = pygame.display.get_surface().get_width()/2
        center_y = pygame.display.get_surface().get_height()/2
        offset_x = center_x + self.mouse_position[0] + self.world_position[0]
        offset_y = center_y + self.mouse_position[1] + self.world_position[1]

        #self.screen_position = (self.world_position[0] + self.mouse_position[0],self.world_position[1] +  self.mouse_position[1] )
        self.world_position = (self.screen_position[0] + self.mouse_position[0] + mouse_offset_x, self.screen_position[1] +  self.mouse_position[1] + mouse_offset_y)
        print (self.screen_position)
        #self.world_position = (self.screen_position[0] - offset_x - self.world_position[0], self.screen_position[1] - offset_y - self.world_position[1])
        #self.draw()



zoom = Zoom(WIDTH, HEIGHT, world_size)
run = True
if __name__ == "__main__":
    while run:
        events = pygame.event.get()

        win.fill(0)
        zoom.listen(events)
        zoom.draw()
        pygame.display.update()