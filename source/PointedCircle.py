import pygame
import math


class Pixel:
    def __init__(self, screen, color, pos, size=8):
        self.screen = screen
        self.color = color
        self.pos = pos
        self.size = size

    def update(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.size)


class PointedCircle:
    def __init__(self, win, x,y, step, color):
        self.screen = win
        self.color = color
        self.pixels = []
        self.x, self.y = x,y
        self.step = step#20
        self.angle = 0

        for i in range(36):
            x -= math.sin(self.angle*math.pi/180) * self.step
            y += math.cos(self.angle*math.pi/180) * self.step
            self.angle += 10
            self.pixels.append(Pixel(self.screen, self.color, (self.x + x,self.y +  y), 3))


    def update(self):


        for p in self.pixels:
            p.update()


#
# pointed_circle = PointedCircle(pygame.display.set_mode((800,600)), 100,100,20,"red")
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     pointed_circle.screen.fill(0)
#     pointed_circle.update()
#
#     pygame.display.update()