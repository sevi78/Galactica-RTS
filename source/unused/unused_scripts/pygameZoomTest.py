import pygame
import pygame_widgets

from pygameZoom_edit import PygameZoom
import  sys
from Button import ImageButton
class Window:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1000, 800
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        self.CLOCK = pygame.time.Clock()
        self.FPS = 30
        self.run = True
        self.pygameZoom = PygameZoom(self.WIDTH, self.HEIGHT)
        self.pygameZoom.set_background((0, 0, 0))
        self.game_objects = []
        self.createGameObjects()
        self.loop()

        self.pygameZoom.set_zoom_strength(0.08)
        self.pygameZoom.allow_zooming(True)

    def loop(self):
        while self.run:
            events = pygame.event.get()
            self.refresh_window()
            self.events()
            self.CLOCK.tick(self.FPS)

        pygame.quit()
        sys.exit()

    def events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run = False

    def createGameObjects(self):
        spacing = 200
        for x in range(5):
            for y in range(5):
                go = ImageButton(self.WIN, x * spacing, y * spacing, 30, 30, isSubWidget=False,
                    image=pygame.image.load("C:\\Users\\sever\\Documents\\Galactica2.8\\pictures\\planets\\zork_50x50.png"),
                    onClick=lambda: print("OK"),
                    name= "test")
                self.game_objects.append(go)

    def refresh_window(self):
        self.WIN.fill(0)
        # Draw shapes
        spacing = 200
        # for i in self.game_objects:
        #
        #     #self.pygameZoom.draw_game_object(i.getX(), i.getY(), i.getWidth(), i.getHeight(), self.WIN, i)
        #     #print(i.getX(),i.getY,i.getWidth(), i.getHeight())
        #     self.pygameZoom.draw_rect((23,43,12),i.getX(), i.getY(), i.getWidth(), i.getHeight())
        #     #print ([i.x for i in self.pygameZoom.shapes])

        for i in self.game_objects:
            image = i.image
            self.pygameZoom.blit(image, (i._x, i._y), button=i)

        """
        for x in range(5):
            for y in range(5):

                #self.pygameZoom.draw_game_object( x * 100, y * 100, 50, 50, self.WIN)
                image = pygame.image.load("C:\\Users\\sever\\Documents\\Galactica2.8\\pictures\\planets\\zork_150x150.png")
                self.pygameZoom.blit(pygame.transform.scale(image, (50, 50)), (x * 200, y * 200), button = ImageButton(self.WIN, x * spacing, y * spacing, 30, 30, isSubWidget=False,
                    image=pygame.image.load("C:\\Users\\sever\\Documents\\Galactica2.8\\pictures\\planets\\zork_50x50.png"),
                    onClick=lambda: print("OK"),
                    name= "test"))

                # b = ImageButton(self.WIN, x * spacing, y * spacing, 30, 30, isSubWidget=False,
                #     image=pygame.image.load("C:\\Users\\sever\\Documents\\Galactica2.8\\pictures\\planets\\zork_50x50.png"),
                #     onClick=lambda: print("OK"),
                #     name= "test")
                # self.pygameZoom.blit(b, (x * spacing, y * spacing))

        # print ("pygameZoom.boundaries: ", self.pygameZoom.boundaries)
        # print (dir(self.pygameZoom.shapes[0]))
        # print (self.pygameZoom.shapes[0].outer.boundaries)
        # End of draw shapes section


        #events =
        """


        pygame_widgets.update(pygame.event.get())
        self.pygameZoom.render(self.WIN, (0, 0))

        pygame.display.update()






win = Window()