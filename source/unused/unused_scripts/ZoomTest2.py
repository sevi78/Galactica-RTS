import pygame
import sys
import pygame_widgets
from Button import ImageButton

pygame.init()
WIDTH = 1000
HEIGHT = 1000
pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
win = pygame.display.get_surface()

# create test array
buttons = []
spacing = 100
for x in range(10):
    for y in range(10):
        b = ImageButton(win,x*spacing,y*spacing,30,30, isSubWidget=False,image=pygame.image.load("C:\\Users\\sever\\Documents\\Galactica2.8\\pictures\\planets\\zork_50x50.png"), onClick=lambda :print ("OK"))
        buttons.append(b)

class Zoom:
    def __init__(self,width, height, zoomobjects):
        self.width = WIDTH
        self.height = HEIGHT
        self.zoomfactor = 1.0
        self.zoom_factor_scale = 0.1
        self.zoom_direction = 1
        self.zoomobjects = zoomobjects
        self.zerox = 0
        self.zeroy = 0
    def update(self,events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.zoomfactor = 1.0
                    self.zoomfactor += self.zoom_factor_scale

                elif event.button == 5:
                    self.zoomfactor = 1.0
                    self.zoomfactor -= self.zoom_factor_scale

                if event.button == 4 or 5:
                    for i in buttons:
                        self.set_position(i)
                if event.button == 1:
                    self.zoomfactor = 1.0

    def set_position(self, obj):
        # Get the mouse wheel delta
        zoom = pygame.mouse.get_rel()[1]

        # Calculate the new width and height based on the zoom factor
        zoom_factor = self.zoomfactor + zoom * 0.1
        new_width = int(obj.getWidth() * zoom_factor)
        new_height = int(obj.getHeight() * zoom_factor)

        # Calculate the new x and y positions based on the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        new_x = mouse_x - new_width / 2
        new_y = mouse_y - new_height / 2

        # Set the new x, y, width, and height values for the object
        obj.setX(new_x)
        obj.setY(new_y)
        obj.setWidth(new_width)
        obj.setHeight(new_height)


zoom = Zoom(WIDTH, HEIGHT, buttons)
def quit_game(events):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

run = True
while run:
    events = pygame.event.get()
    win.fill((123,23,32))
    pygame_widgets.update(events)
    zoom.update(events)
    quit_game(events)
    pygame.display.update()


    """rx = 1/w*x, rx1 = rx*w1-mx-w1/2*zoom"""