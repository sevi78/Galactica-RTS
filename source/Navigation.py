from pprint import pprint

import pygame
from pygame_widgets.util import drawText


import source.Globals
from source.Globals import *
from source.AppHelper import limit_positions
from source.WidgetHandler import WidgetHandler, WidgetBase


class Navigation_old:
    def __init__(self, parent):
        self.parent = parent
        self.x = 0
        self.y = 0
        # self.limit_x = source.Globals.scene_width - pygame.display.get_surface().get_width()
        # self.limit_y = source.Globals.scene_height -pygame.display.get_surface().get_height()

        # define borders
        self.left_end = self.parent.universe.left_end - pygame.display.get_surface().get_width()/2
        self.right_end = self.parent.universe.right_end - pygame.display.get_surface().get_width()/2
        self.top_end = self.parent.universe.top_end - pygame.display.get_surface().get_height()/2
        self.bottom_end = self.parent.universe.bottom_end - pygame.display.get_surface().get_height()/2

        self.position_x = pygame.display.get_surface().get_width()/2
        self.position_y = pygame.display.get_surface().get_height()/2
        self.value = 0.0
        self.acceleration = 35.0
        self.acceleration_max = 5.0
        self.acceleration_min = 1.0
        self.moveables = WidgetHandler.layers[0] + WidgetHandler.layers[1] + WidgetHandler.layers[3] + WidgetHandler.layers[8] + WidgetHandler.layers[4]
        self.moving = False
        self.stopps = {"left":False, "right":False, "up":False, "down":False}
        self.stopp = False
        self.key_pressed = False
        self.mouse_pressed = False

    def accelerate(self):
        if self.value + self.acceleration < self.acceleration_max:
            self.value += self.acceleration
        else:
            self.value = self.acceleration_max

    def slowdown(self):
        if self.value - self.acceleration > self.acceleration_min:
            self.value -= self.acceleration
        else:
            self.value = self.acceleration_min

    def calculate_distance_to_center(self):
        mp = pygame.mouse.get_pos()
        mp_x = mp[0]
        mp_y = mp[1]

        win = pygame.display.get_surface()
        win_width = win.get_width()
        win_height = win.get_height()
        center_x = win_width / 2
        center_y = win_height / 2

        dist_x = center_x - mp_x
        dist_y = center_y - mp_y
        return dist_x, dist_y

    def drag(self, events):
        """
        drags the background and updates the positions of the Elements
        :param events:
        :return:
        """

        if not source.Globals.navigation:
            return

        for event in events:
            # ctrl:
            if event.type == pygame.KEYDOWN:
                if event.key == 1073742048:# ctrl:
                    self.key_pressed = True

            elif event.type == pygame.KEYUP:
                if event.key == 1073742048:
                    self.key_pressed = False
            # mouse all buttons
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False

        # both, then act
        if self.key_pressed == True and self.mouse_pressed == True:
            dist_x, dist_y = self.calculate_distance_to_center()
            if self.position_x >= self.left_end and self.position_x <= self.right_end and \
                    self.position_y >= self.top_end and self.position_y <= self.bottom_end:
                self.x = dist_x / self.acceleration
                self.y = dist_y / self.acceleration
                self.position_x -= self.x
                self.position_y -= self.y
                self.move_objects()
            else:
                if self.position_x < self.left_end:
                    self.position_x = self.left_end
                elif self.position_x > self.right_end:
                    self.position_x = self.right_end
                if self.position_y < self.top_end:
                    self.position_y = self.top_end
                elif self.position_y > self.bottom_end:
                    self.position_y = self.bottom_end

        # if self.key_pressed == True and self.mouse_pressed == True:
        #     dist_x, dist_y = self.calculate_distance_to_center()
        #     if self.position_x >= self.left_end and self.position_x <= self.right_end and \
        #             self.position_y >= self.top_end and self.position_y <= self.bottom_end:
        #         self.x = dist_x / self.acceleration
        #         self.y = dist_y / self.acceleration
        #         self.position_x -= self.x
        #         self.position_y -= self.y
        #         self.move_objects()


        # if self.key_pressed == True and self.mouse_pressed == True:
        #     #self.limit_position()
        #
        #
        #
        #     dist_x, dist_y = self.calculate_distance_to_center()
        #     self.x = dist_x / self.acceleration
        #     self.y = dist_y / self.acceleration
        #
        #     if self.position_x -self.x >= self.left_end:
        #         self.position_x -= self.x
        #         self.debug_position()
        #         self.move_objects()
        #     else:
        #         self.position_x += self.x
        #
        # if self.key_pressed == True and self.mouse_pressed == True:
        #     dist_x, dist_y = self.calculate_distance_to_center()
        #     self.x = dist_x / self.acceleration
        #     self.y = dist_y / self.acceleration
        #     self.position_x -= self.x
        #     self.position_Y -= self.Y
        #
        #     self.move_objects()

            # elif self.position_x > self.right_end:
            #     self.position_x = self.right_end - 1
            #     return
            # else:
            #     self.move_objects()
            #     self.debug_position()




    def limit_position(self):
        # zero_x = self.limit_x * -1
        # zero_y = self.limit_y * -1
        # self.stopp = False
        #
        # if self.position_x < zero_x:
        #     self.position_x = zero_x +10
        #     self.stopp = True
        # elif self.position_x > float(self.limit_x):
        #     self.position_x = self.limit_x-10
        #     self.stopp = True
        #
        # elif self.position_y < zero_y:
        #     self.position_y = zero_y +10
        #     self.stopp = True
        # elif self.position_y > float(self.limit_y):
        #     self.position_y = self.limit_y-10
        #     self.stopp = True
        # else:
        #     self.stopp = False
        self.stopps["left"] = self.position_x < self.left_end
        self.stopps["right"] = self.position_x > self.right_end
        self.stopps["up"] = self.position_x > self.right_end
        self.stopps["down"] = self.position_y > self.bottom_end


        # if self.position_x < self.left_end:
        #     #self.position_x = self.left_end
        #     self.stopps["left"] = 1
        # else:
        #     self.stopps["left"] = 0
        #
        # if self.position_x > self.right_end:
        #     self.stopps["right"] = 1
        #
        # elif self.position_y < self.top_end:
        #     #self.position_y = self.top_end
        #     self.stopp = True
        # elif self.position_y > self.bottom_end:
        #     #self.position_y = self.bottom_end
        #     self.stopp = True
        # else:
        #
        #     self.stopp = False

        if any(self.stopps.values()):
            self.stopp = True

        if self.stopp:
            source.Globals.app.event_text = "you have reached the end of the universe!!"

        print("_____________________________________________________________")
        print("Navigation.limit_position:self.position_x, self.position_y: ", self.position_x, self.position_y)
        # print("zero_x, zero_y,", zero_x, zero_y, )
        # print("self.limit_x, self.limit_y,:", self.limit_x, self.limit_y, )
        print ("self.stopp: ", self.stopp)

        return self.stopp

    def debug_position(self):
        print ("debug_position")
        color = source.Globals.colors.frame_color
        font = pygame.font.SysFont(None, 18)
        win = self.parent.win
        text_spacing = 20
        text_id = 1

        # center
        center_x = pygame.display.get_surface().get_width() / 2
        center_y = pygame.display.get_surface().get_height() / 2
        pygame.draw.circle (source.Globals.win, source.Globals.colors.frame_color, (pygame.display.get_surface().get_width()/2, pygame.display.get_surface().get_height()/2), 15, 1)

        text = "x:" + str(int(self.x)) + " / y:" + str(int(self.y))
        drawText(win, text, color, ((center_x, center_y + text_spacing * text_id), (400, 500)), font, "left")
        text_id += 1

        text = "position_x:" + str(int(self.position_x)) + " / position_y:" + str(int(self.position_y))
        drawText(win, text, color,((center_x, center_y + text_spacing * text_id),(400, 500)), font, "left")
        text_id += 1


        # from mouse to self position
        # pygame.draw.line(source.Globals.win, source.Globals.colors.frame_color, pygame.mouse.get_pos(), (
        # self.position_x, self.position_y))

        # universe
        pygame.draw.rect(source.Globals.win, source.Globals.colors.ui_white,
            [source.Globals.app.universe.left_end,source.Globals.app.universe.top_end,source.Globals.scene_width, source.Globals.scene_height ], 1)

        text = "scene_width: " +  str(source.Globals.scene_width) + " scene_height: " +  str(source.Globals.scene_height)
        drawText(win, text, color, ((center_x, center_y + text_spacing * text_id), (400, 500)), font, "left")
        text_id += 1

        text = "left_end: " + str(self.left_end) + " right_end: " + str(self.right_end) + " top_end: " + str(self.top_end) + " bottom_end: " + str(self.bottom_end)
        drawText(win, text, color, ((center_x, center_y + text_spacing * text_id), (400, 500)), font, "left")
        text_id += 1

        # navigation
        drawText(win, "stopp: " + str(self.stopp), color, ((center_x, center_y + text_spacing * text_id), (400, 500)), font, "left")
        text_id += 1

        pygame.draw.rect(source.Globals.win, source.Globals.colors.frame_color,
            [self.left_end, self.top_end,
             self.right_end, self.bottom_end], 1)



    def move_objects(self):
        # if not self.limit_position():
        #     self.position_x -= self.x
        #     self.position_y -= self.y
        # else:
        #     source.Globals.app.event_text = "you have reached the end of the universe!!"
        #
        # if not self.stopp:

        # if (not self.position_x < self.left_end ) and (not self.position_x > self.right_end ) \
        #     and (not self.position_y < self.top_end) and (not self.position_y > self.bottom_end):
        #     self.position_x -= self.x
        #     self.position_y -= self.y
        #     for i in self.moveables:
        #         i._x -= self.x * -1
        #         i._y -= self.y * -1
        #         if hasattr(i, "set_center"):
        #             if callable(i.set_center):
        #                 i.set_center()
        #
        #         limit_positions(i)
        # else:
        #     source.Globals.app.event_text = "you have reached the end of the universe!!"
        # if self.position_x < self.left_end:
        #     self.position_x = self.left_end
        #
        # elif self.position_x > self.right_end:
        #     self.position_x = self.right_end
        # else:
        #     self.position_x -= self.x
        #
        # if self.position_y < self.top_end:
        #     self.position_y = self.top_end
        # elif self.position_y > self.bottom_end:
        #     self.position_y = self.bottom_end
        # else:
        #     self.position_y -= self.y

        # if self.stopps["left"]:
        #     self.position_x += self.x
        # else:
        #     self.position_x -= self.x
        #
        # self.position_y -= self.y

        for i in self.moveables:
            i._x -= self.x * -1
            i._y -= self.y * -1
            if hasattr(i, "set_center"):
                if callable(i.set_center):
                    i.set_center()

            limit_positions(i)


        print ("Visible Objects: ", len([i for i in self.moveables if not i._hidden]))
        print ((self.position_x, self.position_y), pygame.mouse.get_pos())

        #source.Globals.win.blit (source.Globals.app.background_image.surface, (0,0))

    def navigate_to(self, obj):# not working yet

        ship = [i for i in source.Globals.app.ships if i.name == obj][0]
        print("navigate_to: ", ship)
        self.position_x = ship.getX()
        self.position_y = ship.getY()
        for i in self.moveables:
            i._x -= self.x * -1
            i._y -= self.y * -1
            if hasattr(i, "set_center"):
                if callable(i.set_center):
                    i.set_center()

            limit_positions(i)



class Navigation(WidgetBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, *args, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)

        self.zoom = 1
        self.mp = None
        self.mouse_pressed = None
        self.mouse_wheel = None
        self.key_pressed = None
        self.parent = kwargs.get("parent")
        self.moveables = WidgetHandler.layers[0] + WidgetHandler.layers[1] + WidgetHandler.layers[3] + \
                         WidgetHandler.layers[8] + WidgetHandler.layers[4]

        self.dist_x = None
        self.dist_y = None
        self.center_x = pygame.display.get_surface().get_width()/2
        self.center_y = pygame.display.get_surface().get_height()/2
        self.left = self.parent.universe.left_end + self.center_x *-1
        self.right = self.parent.universe.right_end - self.center_x
        self.top = self.parent.universe.top_end + self.center_y * -1
        self.bottom = self.parent.universe.bottom_end - self.center_y

        self.scene_x = 0
        self.scene_y = 0

        self.acceleration = 35.0
        self.acceleration_max = 5.0
        self.acceleration_min = 1.0

        self.scene_width = kwargs.get("scene_width")
        self.scene_height = kwargs.get("scene_height")
        self.not_to_draw = ['_isSubWidget', "parent","not_to_draw" ,
             '_hidden',
             '_disabled','layers', "layer",'moveables',"win", 'x',
             'y',
             '_width',
             '_height',
             'property',]
        self.to_draw = [i for i in self.__dict__.keys() if not i in WidgetBase.__dict__.keys() and not i in self.not_to_draw]



    def listen(self, events):
        if not navigation:
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
                    self.zoom += event.y/100
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
        self.center_x = pygame.display.get_surface().get_width()/2
        self.center_y = pygame.display.get_surface().get_height()/2
        # mouse position
        self.mp = pygame.mouse.get_pos()

        # distance to center
        self.dist_x = (self.center_x - self.mp[0]) * -1
        self.dist_y = (self.center_y - self.mp[1]) * -1

        # set self.position to mouse cursor
        self.setX(self.mp[0])
        self.setY(self.mp[1])

        # limit position
        # left
        # if self.scene_x  > self.left:
        #     self.drag()
        # elif self.dist_x > 0:
        #     self.drag()
        #
        # # right
        # elif self.scene_x < self.right:
        #     self.drag()
        # elif self.dist_x < 0:
        #     self.drag()
        # # top
        # elif self.scene_y < self.top:
        #     self.drag()
        # elif self.dist_y < 0:
        #      self.drag()
        #
        # # bottom
        # elif self.scene_y < self.bottom:
        #     self.drag()
        # elif self.dist_y < 0:
        #     self.drag()
        self.drag()
        #self.debug()

    def drag(self):
        # set scene position
        self.scene_x -= self.x - self.dist_x / self.acceleration
        self.scene_y -= self.y - self.dist_y / self.acceleration
        self.drag_objects()


    def drag_objects(self):
        # # set new position of objects
        for i in self.moveables:

                i.setX(i.getX() - (self.dist_x / self.acceleration ))
                i.setY(i.getY() - (self.dist_y  / self.acceleration ))
                limit_positions(i)

    def draw_grid(self):
        width = pygame.display.get_surface().get_width()
        height = pygame.display.get_surface().get_height()

        for x in range(width):
            if str(x).endswith("00"):
                pygame.draw.line(self.win, source.Globals.colors.frame_color,(x,0),(x,height),)
                
    def draw(self):
        if not self._hidden and navigation:
            # center
            self.center_x = pygame.display.get_surface().get_width() / 2
            self.center_y = pygame.display.get_surface().get_height() / 2
            pygame.draw.circle(source.Globals.win, source.Globals.colors.frame_color, (
            pygame.display.get_surface().get_width() / 2, pygame.display.get_surface().get_height() / 2), 15, 1)

            color = source.Globals.colors.frame_color
            font = pygame.font.SysFont(None, 18)
            win = self.parent.win
            text_spacing = 20
            text_id = 1

            for i in self.to_draw:
                text = str(i) + ": " + str(getattr(self,  i))
                drawText(win, text, color, ((self.center_x, self.center_y + text_spacing * text_id), (400, 500)), font, "left")
                text_id += 1


            pygame.draw.circle(source.Globals.win, source.Globals.colors.frame_color, (
                (self.getX(), self.getY())), 15, 1)

            #self.draw_grid()
    def debug(self):
        pprint(self.__dict__)



