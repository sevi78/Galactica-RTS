import pygame
from unused.pygameZoom import PygameZoom

import Globals


class ZoomWindow:
    def __init__(self, **kwargs):
        #pygame.init()
        self.parent = kwargs.get("parent", None)
        self.WIDTH, self.HEIGHT = Globals.WIDTH, Globals.HEIGHT
        self.WIN = kwargs.get("win")
        self.CLOCK = pygame.time.Clock()
        self.FPS = 30
        self.run = True
        self.pygameZoom = PygameZoom(self.WIDTH, self.HEIGHT)
        #self.pygameZoom.set_background((0, 0, 0))
        self.x = 0
        self.y = 0
        self.loop()
        print (self.__dict__)

    def refresh_window(self):
        #self.WIN.fill(0)
        for i in self.parent.planets:

            # self.pygameZoom.draw_game_object(win=self.WIN,color= Globals.colors.frame_color,
            #    x=i.x, y=i.y, width=i.getWidth(), height=i.getHeight(), w=1, parent = i)

            self.pygameZoom.draw_rect( color=Globals.colors.frame_color,
                x=i.x, y=i.y, width=i.getWidth(), height=i.getHeight(), w=1, parent=i)

            #self.pygameZoom.draw_line((255, 255, 255), 0, 0, 200, 200)
            self.pygameZoom.render(Globals.win, (0,0))
            #pygame.display.update()

    def events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run = False

    def loop(self):
        #while self.run:
        self.refresh_window()
        #self.events()
        self.CLOCK.tick(self.FPS)
        # pygame.quit()
        # sys.exit()