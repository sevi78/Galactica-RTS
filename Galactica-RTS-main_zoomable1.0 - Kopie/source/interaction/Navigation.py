from pprint import pprint

from pygame_widgets.util import drawText

import source.utils.Globals
from source.gui.WidgetHandler import WidgetHandler, WidgetBase
from source.utils import limit_positions, colors
from source.utils.Globals import *


class Navigation(WidgetBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, *args, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)

        self.zoom = 1
        self.mp = None
        self.mouse_pressed = None
        self.mouse_wheel = None
        self.key_pressed = None
        self.parent = kwargs.get("parent")
        self.set_moveables()

        self.dist_x = None
        self.dist_y = None
        self.center_x = pygame.display.get_surface().get_width() / 2
        self.center_y = pygame.display.get_surface().get_height() / 2
        self.left = self.parent.universe.left_end + self.center_x * -1
        self.right = self.parent.universe.right_end - self.center_x
        self.top = self.parent.universe.top_end + self.center_y * -1
        self.bottom = self.parent.universe.bottom_end - self.center_y

        self.scene_x = 0
        self.scene_y = 0

        self.acceleration = 150.0
        self.acceleration_max = 5.0
        self.acceleration_min = 1.0

        self.scene_width = kwargs.get("scene_width")
        self.scene_height = kwargs.get("scene_height")
        self.not_to_draw = ['_isSubWidget', "parent", "not_to_draw",
                            '_hidden',
                            '_disabled', 'layers', "layer", 'moveables', "win", 'x',
                            'y',
                            '_width',
                            '_height',
                            'property', ]

        self.to_draw = [i for i in self.__dict__.keys() if
                        not i in WidgetBase.__dict__.keys() and not i in self.not_to_draw]

    def set_moveables(self):
        self.moveables = WidgetHandler.layers[0] + WidgetHandler.layers[1] + WidgetHandler.layers[3] + \
                         WidgetHandler.layers[8] + WidgetHandler.layers[4]

    def listen(self, events):
        if not source.utils.Globals.navigation:
            return

        for event in events:
            # ctrl:
            if event.type == pygame.KEYDOWN:
                if event.key == 1073742048:  # ctrl:
                    self.key_pressed = True

            elif event.type == pygame.KEYUP:
                if event.key == 1073742048:
                    self.key_pressed = False

            # mouse all buttons
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False

            if event.type == pygame.MOUSEWHEEL:
                if event.y == -1 or event.y == 1:
                    self.zoom += event.y / 100
                    self.mouse_wheel = True
            else:
                self.mouse_wheel = False

        # both, then act
        if self.key_pressed and self.mouse_pressed:
            self.calculate()
            self.show()
        else:
            self.hide()

        if self.key_pressed and self.mouse_wheel:
            self.calculate()
            self.show()
        else:
            self.hide()

    def calculate(self):
        # screen center
        self.center_x = pygame.display.get_surface().get_width() / 2
        self.center_y = pygame.display.get_surface().get_height() / 2

        # mouse position
        self.mp = pygame.mouse.get_pos()

        # distance to center
        self.dist_x = (self.center_x - self.mp[0]) * -1
        self.dist_y = (self.center_y - self.mp[1]) * -1

        # set self.position to mouse cursor
        self.setX(self.mp[0])
        self.setY(self.mp[1])
        self.drag()
        # self.debug()

    def drag(self):
        # set scene position
        self.scene_x -= self.x - self.dist_x / self.acceleration
        self.scene_y -= self.y - self.dist_y / self.acceleration
        self.drag_objects()

    def drag_objects(self):
        # # set new position of objects
        for i in self.moveables:
            i.setX(i.getX() - (self.dist_x / self.acceleration))
            i.setY(i.getY() - (self.dist_y / self.acceleration))
            limit_positions(i)

    def draw(self):
        if not self._hidden and source.utils.Globals.navigation:
            # center
            self.center_x = pygame.display.get_surface().get_width() / 2
            self.center_y = pygame.display.get_surface().get_height() / 2
            pygame.draw.circle(source.utils.Globals.win, colors.frame_color, (
                pygame.display.get_surface().get_width() / 2, pygame.display.get_surface().get_height() / 2), 15, 1)

            color = colors.frame_color
            font = pygame.font.SysFont(None, 18)
            win = self.parent.win
            text_spacing = 20
            text_id = 1

            for i in self.to_draw:
                text = str(i) + ": " + str(getattr(self, i))
                drawText(win, text, color, (
                    (self.center_x, self.center_y + text_spacing * text_id), (400, 500)), font, "left")
                text_id += 1

            pygame.draw.circle(source.utils.Globals.win, colors.frame_color, (
                (self.getX(), self.getY())), 15, 1)

    def navigate_to_(self, obj):
        target = [i for i in self.parent.ships if i.name == obj][0]
        old_x = self.getX()
        old_y = self.getY()

        self._x = target.getX()
        self._y = target.getY()
        self.dist_x = self.getX() - old_x
        self.dist_y = self.getY() - old_y

        for i in self.moveables:
            i.setX(i.getX() - self.dist_x)
            i.setY(i.getY() - self.dist_y)
            limit_positions(i)

    def navigate_to__(self, obj):
        target = [i for i in self.parent.ships if i.name == obj][0]
        old_x = self.getX()
        old_y = self.getY()

        self._x = target.getX()
        self._y = target.getY()
        self.dist_x = self.getX() - old_x
        self.dist_y = self.getY() - old_y

        for i in self.moveables:
            new_x = i.getX() - self.dist_x
            new_y = i.getY() - self.dist_y
            i.setX(new_x)
            i.setY(new_y)
            limit_positions(i)

    def navigate_to(self, obj):
        return
        target = [i for i in self.parent.ships if i.name == obj][0]
        old_x = self.getX()
        old_y = self.getY()

        self._x = target.getX()
        self._y = target.getY()
        self.dist_x = self.getX() - old_x
        self.dist_y = self.getY() - old_y

        self.center_x = pygame.display.get_surface().get_width() / 2
        self.center_y = pygame.display.get_surface().get_height() / 2

        for i in self.moveables:
            new_x = i.getX() - self.dist_x + self.center_x
            new_y = i.getY() - self.dist_y + self.center_y
            i.setX(new_x)
            i.setY(new_y)
            limit_positions(i)

        self.calculate()
    def debug(self):
        pprint(self.__dict__)
