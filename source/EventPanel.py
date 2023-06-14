import pygame
from pygame_widgets.mouse import Mouse, MouseState
from pygame_widgets.util import drawText

import source.Globals
from source.EventText import EventText
from source.Globals import pictures_path
from source.WidgetHandler import WidgetBase


# pygame.init()
# WIDTH = 1200
# HEIGHT = 900
# pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
# win = pygame.display.get_surface()


class EventPanel(WidgetBase, EventText):
    def __init__(self, win, x, y, width, height, **kwargs):
        super().__init__(win, x, y, width, height, **kwargs)
        EventText.__init__(self)
        self.layer = kwargs.get("layer", 9)
        self.win = win
        self.parent = kwargs.get("parent")
        self.frame_color = source.Globals.colors.frame_color
        self.bg_color = pygame.colordict.THECOLORS["black"]
        self.font = pygame.font.SysFont(None, 32)
        self.title_font = pygame.font.SysFont(None, 50)
        self.center = kwargs.get("center", True)

        # surface
        self.surface = pygame.surface.Surface((width, height))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect[0] = x
        self.surface_rect[1] = y
        self.image = source.Globals.images[pictures_path]["textures"][
            "event_panel.png"]  # pygame.image.load(os.path.split (source.Globals.dirpath)[0] + os.sep + "event_panel.png")
        self.image_scaled = pygame.transform.scale(self.image, (width, height))

        # text
        self.text_surfaces = {}
        self.border = 0
        self.size = (width, height)
        self.word_height_sum = 0

        self.title = None
        self.body = None
        self.functions = []

        self.obsolete_text = []
        self.set_text("start")

    def set_text(self, key):
        self.title = self.text[key]["title"]
        self.body = self.text[key]["body"]
        self.functions = self.text[key]["functions"]

        self.show()

        source.Globals.game_paused = True
        self.obsolete_text.append(key)

    def center_pos(self, width, height):
        win = pygame.display.get_surface()
        win_width = win.get_width()
        win_height = win.get_height()

        x = win_width / 2 - width / 2
        y = win_height / 2 - height / 2
        pos = (x, y)

        return pos

    def wrap_text(self, text, pos, font, color=pygame.Color('white')):
        """ text wrapper function """
        if not text: return
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = self.size  # Use self instead of undefined surface variable
        x, y = pos

        x += self.border
        y += self.border

        # store the sum of all words to get the max height of all text to resize the panel
        self.word_height_sum = 0

        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()

                self.word_height_sum += word_height

                if x + word_width >= max_width:
                    x = pos[0] + self.border  # Reset the x.
                    y += word_height  # Start on new row.
                self.text_surfaces[str(x) + "_" + str(y)] = word_surface
                self.win.blit(word_surface, (x, y))
                x += word_width + space

            x = pos[0] + self.border  # Reset the x.
            y += word_height  # Start on new row.

            # get the last height value
            self.word_height_sum = y

    def draw(self):
        if not self._hidden:
            # self.surface.fill(self.bg_color)
            # self.win.blit(self.surface, self.surface_rect)
            # self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, 1)

            if self.center:
                # image
                pos = self.center_pos(self.getWidth(), self.getHeight())
                self.surface_rect[0] = pos[0]
                self.surface_rect[1] = pos[1]
                self.win.blit(self.image_scaled, self.surface_rect)

                # title
                self.title_surface = self.title_font.render(self.title, self.font, source.Globals.colors.ui_dark)
                self.title_surface_rect = self.title_surface.get_rect()
                x = pos[0] + self.getWidth() / 2 - self.title_surface.get_width() / 2
                self.title_surface_rect.x = x
                self.title_surface_rect.y = (pos[1] + self.getHeight() / 8)

                self.win.blit(self.title_surface, self.title_surface_rect)

                self.body_text = drawText(self.win, self.body, source.Globals.colors.ui_dark,
                    (pos[0] + self.getWidth() / 6, (pos[1] + self.getHeight() / 8 * 2), self.getWidth() / 6 * 4,
                     self.getHeight() / 8 * 7), self.font, "center")

                pygame.mixer.music = source.Globals.sounds.intro_drama
                pygame.mixer.music.play(fade_ms=1000)

        else:
            pygame.mixer.Sound.fadeout(source.Globals.sounds.intro_drama, 5000)

    def listen(self, events):
        mouseState = Mouse.getMouseState()
        for event in events:
            if mouseState == MouseState.CLICK:
                self.hide()
                source.Globals.game_paused = False

    def update(self):
        player = self.parent.player
        if player.population >= 500:
            if not "goal1" in self.obsolete_text:
                self.set_text("goal1")

        if player.population >= 1000:
            if not "goal2" in self.obsolete_text:
                self.set_text("goal2")

# ep = EventPanel(win=win, x=300,y=200,width=900,height=600, center= True)
#
# def quit_game(events):
#     # quit the game with quit icon or esc
#     for event in events:
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             quit()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 sys.exit()
# #ep.hide()
# run = True
# while run:
#     # get events, only do this once!! and exactly here. otherwise performance is very bad
#     events = pygame.event.get()
#
#     # call functions, don't mess up the order :)
#
#     win.fill((123,23,32))
#
#     pygame_widgets.update(events)
#
#     quit_game(events)
#     pygame.display.update()
