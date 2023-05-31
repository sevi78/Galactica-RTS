import pygame
import sys

import Globals
from unused.pygameZoom import PygameZoom


class Window:
    def __init__(self, **kwargs):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1920,1080
        self.WIN = kwargs.get("win",pygame.display.set_mode((self.WIDTH, self.HEIGHT)))
        self.CLOCK = pygame.time.Clock()
        self.FPS = 30
        self.run = True
        self.pygameZoom = PygameZoom(1920, 1080)
        #self.pygameZoom.set_background((0, 0, 0))
        self.x = 0
        self.y = 0

        self.grid_size_x = 180
        self.grid_size_y = self.grid_size_x
        self.grid_limit = int(pygame.display.get_surface().get_height() / self.grid_size_y)
        self.font = pygame.font.get_fonts()

        self.createGrid()

        self.loop()

    def refresh_window(self):
        #self.WIN.fill(0)



        #self.pygameZoom.draw_line((255, 255, 255), 0, 0, 200, 200)
        self.pygameZoom.render(self.WIN, (0,0))
        pygame.display.update()

    def createGrid(self):


        for x in range(self.grid_limit):
            for y in range(self.grid_limit):
                self.pygameZoom.draw_game_object(self.WIN, (
                100, 200, 0), self.grid_size_x * x, self.grid_size_y * y, self.grid_size_x, self.grid_size_y, 1, image = Globals.images[
                    Globals.pictures_path]["planets"]["zork_50x50.png"])
                # drawText(self.WIN, str(grid_size_x * x) + str(grid_size_y * y) + str(grid_size_x) + str(grid_size_y),
                #     Globals.colors.frame_color,((grid_size_x * x, grid_size_y * y),(grid_size_x, grid_size_y)),pygame.font.SysFont(None,20))
        print ("createGrid")
    def events(self):
        for e in pygame.event.get():
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