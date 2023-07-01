import random

import pygame
from pygame_widgets.mouse import Mouse, MouseState

import source.game_play.GameEvents
from source.game_play.GameEvents import GameEvent, Deal
import source.utils.Globals
from source.game_play.GameEvents import game_events, resources
from source.gui.Button import Button
from source.gui.WidgetHandler import WidgetBase
from source.utils import colors, sounds, images, Globals
from source.utils.Globals import pictures_path


# pygame.init()
# WIDTH = 1200
# HEIGHT = 900
# pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
# win = pygame.display.get_surface()


class EventPanel(WidgetBase):
    def __init__(self, win, x, y, width, height, **kwargs):
        super().__init__(win, x, y, width, height, **kwargs)

        self.layer = kwargs.get("layer", 9)
        self.win = win
        self.parent = kwargs.get("parent")
        self.frame_color = colors.frame_color
        self.bg_color = pygame.colordict.THECOLORS["black"]
        self.font = pygame.font.SysFont(None, 32)
        self.title_font = pygame.font.SysFont(None, 50)
        self.center = kwargs.get("center", True)

        # surface
        self.surface = pygame.surface.Surface((width, height))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect[0] = x
        self.surface_rect[1] = y
        self.image = images[pictures_path]["textures"]["event_panel.png"]
        self.image_scaled = pygame.transform.scale(self.image, (width, height))

        # events
        self.game_event = None
        self.game_events = game_events
        self.event_time = 0
        self.min_intervall = 3500
        self.intervall = 5000
        self.random_event_time = self.intervall * Globals.time_factor

        # text
        self.text_surfaces = {}
        self.border = 0
        self.size = (width + self.getX() - self.getWidth()/6, height + self.getHeight()) # used fro text wrapper, makes no sense but works
        self.word_height_sum = 0

        self.title = None
        self.title_surface_rect = None
        self.title_surface = None

        self.body = None
        self.end_text = None
        self.end_text_surface_rect = None
        self.end_text_surface = None

        self.functions = []
        self.event_cue = []
        self.obsolete_events = []

        # Buttons
        self.yes_button = Button(self.win, self.getX() + self.getWidth()/2 -30,
            self.y + self.getHeight(), 60, 60, isSubWidget=False,
            image= pygame.transform.scale(images[pictures_path]["icons"]["yes_icon.png"], (60,60)),
            transparent=True,parent=self, onClick=lambda: self.accept())

        self.no_button = Button(self.win, self.getX() + self.getWidth()/2 + 30,
            self.y + self.getHeight(), 60, 60, isSubWidget=False,
            image=pygame.transform.scale(images[pictures_path]["icons"]["no_icon.png"], (60, 60)),
            transparent=True, parent=self, onClick=lambda: self.decline())

        # set start event event
        self.set_game_event(self.game_events["start"])

    def accept(self):
        if self.game_event.functions:
            if self.game_event.deal:
                self.game_event.deal.make_deal()
                self.hide()

        self.close_event()
        Globals.game_paused = False

    def decline(self):
        self.hide()
        self.close_event()
        Globals.game_paused = False

    def set_text(self):
        self.title = self.game_event.title
        self.body = self.game_event.body
        self.end_text = self.game_event.end_text
        self.functions = self.game_event.functions

        if not self.functions:
            self.yes_button.hide()
            self.no_button.hide()
        else:
            self.yes_button.show()
            self.no_button.show()

        self.show()

        Globals.game_paused = True
        self.obsolete_events.append(self.game_event.name)

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
            if self.center:
                # image
                self.win.blit(self.image_scaled, self.surface_rect)

                # title
                self.title_surface = self.title_font.render(self.title, self.font, colors.ui_dark)
                self.title_surface_rect = self.title_surface.get_rect()
                self.title_surface_rect.x = self.x + self.getWidth() / 2 - self.title_surface.get_width() / 2
                self.title_surface_rect.y = (self.y + self.getHeight() / 8)
                self.win.blit(self.title_surface, self.title_surface_rect)

                # body
                self.wrap_text(self.body,(self.get_position()[0] + self.getWidth()/6, self.title_surface_rect.y + 60),self.font,colors.ui_dark)

                # end_text
                self.end_text_surface = self.font.render(self.end_text, self.font, colors.ui_dark)
                self.end_text_surface_rect = self.end_text_surface.get_rect()
                self.end_text_surface_rect.x = self.x + self.getWidth() / 2 - self.end_text_surface.get_width() / 2
                self.end_text_surface_rect.y = self.y + self.getHeight() - self.getHeight()/3
                self.win.blit(self.end_text_surface, self.end_text_surface_rect)

                # buttons
                self.yes_button.setX(self.x + self.getWidth() / 2 - self.yes_button.getWidth())
                self.yes_button.setY(self.end_text_surface_rect.y + self.yes_button.getHeight()/2)

                self.no_button.setX(self.x + self.getWidth() / 2)
                self.no_button.setY(self.yes_button.getY())

                # sound
                pygame.mixer.music = sounds.intro_drama
                pygame.mixer.music.play(fade_ms=1000)

        else:
            pygame.mixer.Sound.fadeout(sounds.intro_drama, 5000)
            self.yes_button.hide()
            self.no_button.hide()

    def listen(self, events):
        mouseState = Mouse.getMouseState()
        for event in events:
            if mouseState == MouseState.CLICK:
                if not self.functions:
                    if not self._hidden:
                        self.close_event()
                    self.hide()
                    source.utils.Globals.game_paused = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.set_game_event(self.game_events["friendly_trader"])





    def set_game_event(self, event):
        if not event in self.event_cue:
            self.event_cue.append(event)


        self.game_event = self.event_cue[0]
        if self.game_event.deal:
            self.game_event.deal.create_friendly_offer()
        self.game_event.set_body()
        self.set_text()

    def close_event(self):
        self.event_cue.pop(0)
        self.obsolete_events.append(self.game_event)

    def create_random_event(self):
        if self.event_time > self.random_event_time:
            self.random_event_time += random.randint(self.min_intervall, self.intervall) * Globals.game_speed
            event = GameEvent(
                name="alien_deal_random",
                title="Deal Offer",
                body="the alien population of the planet (not set) offers you a deal: they want 200 food for 33 technology.",
                end_text="do you accept the offer?",
                deal= Deal(offer={random.choice(resources): random.randint(0, 1000)}, request={random.choice(resources): random.randint(0, 1000)}),
                functions={"yes": None, "no": None},
                )
            event.offer = {random.choice(resources): random.randint(0, 1000)}
            event.request = {random.choice(resources): random.randint(0, 1000)}
            game_events[event.name] = event.name
            self.set_game_event(event)

    def debug_events(self, function):
        print ("function:", function)
        print("self.game_events", self.game_events)
        print ("self.event_cue",self.event_cue)
        print ("self.obsolete_events", self.obsolete_events)

    def update(self):
        """
        calls the game events based on time or conditions
        """
        self.event_time += 1 * Globals.game_speed
        self.create_random_event()

        player = self.parent.player
        if player.population >= 500:
            if not "goal1" in self.obsolete_events:
                self.set_game_event(self.game_events["goal1"])

        if player.population >= 1000:
            if not "goal2" in self.obsolete_events:
                self.set_game_event(self.game_events["goal2"])

        if player.population >= 10000:
            if not "goal3" in self.obsolete_events:
                self.set_game_event(self.game_events["goal3"])
#
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
#     update(events)
#
#     quit_game(events)
#     pygame.display.update()