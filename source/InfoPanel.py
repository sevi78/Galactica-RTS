import pygame


import source.Globals
from source.Button import ImageButton
from source.WidgetHandler import WidgetBase


class ShipButtons:
    def __init__(self):
        self.visible = False
        self.speed_up_button = ImageButton(source.Globals.win,self.getX(), self.getY() + self.getHeight(), 32,32,
            isSubWidget=False,image=source.Globals.images[source.Globals.pictures_path]["icons"]["speed_up.png"],
            onClick=lambda : print("Ok") )

        self.radius_button = ImageButton(source.Globals.win,self.getX() + self.getWidth(), self.getY() + self.getHeight(),
            32,32, isSubWidget=False, image=source.Globals.images[source.Globals.pictures_path]["icons"]["radius.png"],
            onClick=lambda : print("Ok"))

    def reposition_buttons(self):
        self.spacing = 15
        self.speed_up_button.setX(self.getX() + self.getWidth() + self.spacing)
        self.speed_up_button.setY(self.getY() + self.getHeight())
        self.radius_button.setX(self.getX() + self.getWidth() + self.spacing)
        self.radius_button.setY(self.getY() + self.getHeight() - self.spacing * 3)

    def hide_buttons(self):
        self.speed_up_button.hide()
        self.radius_button.hide()

    def show_buttons(self):
        self.speed_up_button.show()
        self.radius_button.show()

class InfoPanel(WidgetBase):
    def __init__(self, win, x, y, width, height, isSubWidget, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        self.layer = kwargs.get("layer", 4)
        self.parent = kwargs.get("parent")
        self.width = width
        self.height = height
        self.size = (self.width, self.height)
        self.win = win
        self.font = pygame.font.Font(None, 18)
        self.text = ""
        self.color = (0, 0, 0)
        self.bg_color = pygame.colordict.THECOLORS["black"]
        self.pos = [x,y]
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.border = 10
        self.set_colors (source.Globals.colors.frame_color, (12, 10, 1))
        self.rect_frame = None
        self.planet_image = None
        self.planet_rect = None
        self.rect_filled = pygame.Surface((self.width,self.height))

        # text
        self.word_height_sum = 0
        self.text_surfaces = {}
        self.update_text()

        # visible
        self.visible = True

    def update_text(self):
        # Wrap text before rendering onto surface
        self.wrap_text(self.text, self.pos, self.font, self.color)
        self.set_size_from_text()

    def set_text(self, text):
        """
        this is called from outside:
        :param text:
        :return:
        """
        self.text = text
        self.update_text()

    def set_colors(self, color, bg_color):
        self.color = color
        self.bg_color = bg_color

    def set_planet_image(self, planet_image, **kwargs):
        size = kwargs.get("size", None)
        align = kwargs.get("align", "center")
        alpha = kwargs.get("alpha", 128)

        if size:
            self.planet_image = pygame.transform.scale(planet_image, size)
        else:
            self.planet_image = pygame.transform.scale(planet_image, (planet_image.get_width()*2, planet_image.get_height()*2))

        self.planet_rect = self.planet_image.get_rect()

        if align == "topright":
            self.planet_rect.right = self.rect_filled.get_rect().right + self.getX()
            self.planet_rect.top = self.rect_filled.get_rect().top + self.getY()

        if align == "center":
            self.planet_rect.left = self.x + self.rect_frame.width / 2
            self.planet_rect.centery = self.y + self.rect_frame.height / 2

        if alpha:
            self.planet_image.set_alpha(alpha)

    def set_size_from_text(self):
        # self.set_height(self.word_height_sum)
        self.height = self.word_height_sum
        self.size = self.width, self.height

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
                    x = pos[0] + self.border # Reset the x.
                    y += word_height  # Start on new row.
                self.text_surfaces[str(x) + "_" + str(y)] = word_surface
                # self.win.blit(word_surface, (x, y))
                x += word_width + space

            x = pos[0] + self.border  # Reset the x.
            y += word_height  # Start on new row.

            # get the last height value
            self.word_height_sum = y

    def draw(self):
        if self.parent.build_menu_visible: return
        # gets the wrapped text
        self.update_text()

        # draw the panel
        self.rect_filled = pygame.Surface((self.width, self.height +  10))
        self.rect_filled.fill(self.bg_color)
        self.rect_filled.set_alpha(128)
        # self.win.blit(self.rect_filled, self.pos)

        # draw the frame

        self.rect_frame = pygame.draw.rect(self.win, source.Globals.colors.frame_color, pygame.Rect(self.x, self.y, self.width,
                                                                                             self.height +  10),1)
        # draw the planet icon
        if hasattr(self, 'planet_image') and self.planet_image:
            self.win.blit(self.planet_image, self.planet_rect)


        # draw the texts
        for pos,txt in self.text_surfaces.items():
            x = int(pos.split("_")[0])
            y = int(pos.split("_")[1])
            self.win.blit(txt, (x, y))

        # reset text_surfaces for correct displaying
        self.text_surfaces = {}

    def listen(self, events):
        pass

    def update(self,events):
        # self.build_icon.update(events)
        if self.visible:
            self.draw()

