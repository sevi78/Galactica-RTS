import pygame
from pygame_widgets.util import drawText

import Globals
import source.Globals
from Planet import Planet
from WidgetHandler import WidgetBase


class PygameZoom(object):
    shapes = []
    zoom_strength = 0.05  # higher = stronger
    zoom = 1
    last_point = None
    position_in_window = (0, 0)
    background = 0
    zoomingDisabled = False
    draggingDisabled = False

    def __init__(self, W, H) -> None:
        self.WIDTH = W
        self.HEIGHT = H
        self.boundaries = [0, W, 0, H]
        self.shapes = []

    # Shapes
    class Line(object):
        def __init__(self, x1, y1, x2, y2, width, color, outer) -> None:
            super().__init__()
            self.x1 = x1
            self.x2 = x2
            self.y1 = y1
            self.y2 = y2
            self.color = color
            self.width = width
            self.outer = outer

        def draw(self, surface):
            pygame.draw.line(surface, self.color, self.outer.map_point(self.x1, self.y1),
                             self.outer.map_point(self.x2, self.y2))

    class Circle(object):
        def __init__(self, x, y, r, width, color, outer) -> None:
            super().__init__()
            self.x = x
            self.y = y
            self.r = r
            self.width = width
            self.color = color
            self.outer = outer

        def draw(self, surface):
            scaled_r = self.r * self.outer.zoom
            pygame.draw.circle(surface, self.color, self.outer.map_point(self.x, self.y), scaled_r, self.width)

    class Rectangle(object):
        def __init__(self, x, y, w, h, width, color, outer, **kwargs) -> None:
            super().__init__()
            self.parent = kwargs.get("parent")
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.width = width
            self.color = color
            self.outer = outer

        def draw(self, surface, **kwargs):
            new_w = self.w * self.outer.zoom
            new_h = self.h * self.outer.zoom
            new_x, new_y = self.outer.map_point(self.x, self.y)
            pygame.draw.rect(surface, self.color, (new_x, new_y, new_w, new_h), self.width)
            parent = self.parent

            # parent._x = new_x / self.outer.zoom #- pygame.mouse.get_po s()[0]
            # parent._y = new_y / self.outer.zoom #- pygame.mouse.get_pos()[1]s
            # parent._width = new_w
            # parent._height = new_h
            # parent.image_rect = (new_x, new_y, new_w, new_h)

            parent.setX(self.x)
            parent.setY(self.y)
            parent.setWidth(new_w)
            parent.setHeight(new_h)

    class GameObject:
        #class GameObject(WidgetBase):
        def __init__(self,win,  x, y, w, h, width, color, outer, **kwargs) -> None:
            #WidgetBase.__init__(self,win, x,y,w,h,isSubWidget=False, )
            self.parent = kwargs.get("parent")
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.width = width
            self.color = color
            self.outer = outer
            self.image = kwargs.get("image")



        def draw(self, surface, **kwargs):
            #print ("draw", self.parent._x, self.parent._y, self.parent.getWidth(), self.parent.getHeight())
            new_w = self.w * self.outer.zoom
            new_h = self.h * self.outer.zoom
            new_x, new_y = self.outer.map_point(self.x, self.y)
            #pygame.draw.rect(surface, self.color, (new_x, new_y, new_w, new_h), self.width)
            scaled_image = pygame.transform.scale(self.image, (new_w, new_h))
            self.image_rect = (new_x, new_y, new_w, new_h)
            surface.blit(scaled_image, self.image_rect)
            #print (surface, new_x, new_y, new_w, new_h)

            #drawText(surface, str(new_x) ,Globals.colors.frame_color,((self.x,self.y),(100,30)),pygame.font.SysFont(None,20))

            if self.parent:
                self.parent.setX(new_x)
                self.parent.setY(new_y)
                self.parent.setWidth(new_w)
                self.parent.setHeight(new_h)
            #print ("FPS", pygame.time.Clock().get_fps())
        def listen(self, events): 
            pass



    class Ellipse(object):
        def __init__(self, color, rect, width, outer) -> None:
            super().__init__()
            self.color = color
            self.rect = rect
            self.width = width
            self.outer = outer

        def draw(self, surface, **kwargs):
            x, y = self.outer.map_point(self.rect[0], self.rect[1])
            pygame.draw.ellipse(surface, self.color,
                                (x, y, self.rect[2] * self.outer.zoom, self.rect[3] * self.outer.zoom), self.width)

    class Polygon(object):
        def __init__(self, color, points, width, outer) -> None:
            super().__init__()
            self.color = color
            self.points = points
            self.width = width
            self.outer = outer

        def draw(self, surface, **kwargs):
            points = []
            for p in self.points:
                points.append(self.outer.map_point(p[0], p[1]))
            pygame.draw.polygon(surface, self.color, points, self.width)

    class Blit(object):
        def __init__(self, surface, start,outer):
            super().__init__()
            self.surface = surface
            self.start = start
            self.outer = outer

        def draw(self, surface):
            scaled = pygame.transform.scale(self.surface, (int(self.surface.get_width() * self.outer.zoom), int(self.surface.get_height() * self.outer.zoom)))
            surface.blit(scaled, self.outer.map_point(self.start[0], self.start[1]))

    def map_point(self, x, y):
        new_x = (x - self.boundaries[0]) * self.zoom
        new_y = (y - self.boundaries[2]) * self.zoom
        return new_x, new_y

    def draw_line(self, color, x1, y1, x2, y2, width=1, **kwargs):
        self.shapes.append(self.Line(x1, y1, x2, y2, width, color, self))

    def draw_rect(self, color, x, y, width, height, w=0,**kwargs):
        self.shapes.append(self.Rectangle(x, y, width, height, w, color, self, parent=kwargs.get(("parent"))))

    def draw_game_object(self,win, color, x, y, width, height, w=0, **kwargs):
        self.shapes.append(self.GameObject(win,x, y, width, height, w, color, self, **kwargs))

    def draw_circle(self, color, x, y, r, width=0, **kwargs):
        self.shapes.append(self.Circle(x, y, r, width, color, self))

    def draw_ellipse(self, color, rect, width=0, **kwargs):
        self.shapes.append(self.Ellipse(color, rect, width, self))

    def draw_polygon(self, color, points, width=0, **kwargs):
        self.shapes.append(self.Polygon(color, points, width, self))

    def blit(self, surface, start):
        self.shapes.append(self.Blit(surface, start,self))

    def set_background(self, value):
        self.background = value

    def set_zoom_strength(self, value):
        self.zoom_strength = value

    def generate_surface(self):
        self.update_zoom()
        surface = pygame.Surface((self.WIDTH, self.HEIGHT))

        #surface.fill(self.background)
        for shape in self.shapes:
            #print ("shape_", shape )
            shape.draw(surface = surface)

        #self.shapes = []

        return surface

    def render(self, window, pos):
        self.position_in_window = pos
        window.blit(self.generate_surface(), pos)

    def follow_point(self, x, y, zoom):
        self.zoom = zoom
        scale_x = self.WIDTH / zoom
        scale_y = self.HEIGHT / zoom

        self.boundaries[0] = x - scale_x / 2
        self.boundaries[1] = x + scale_x / 2
        self.boundaries[2] = y - scale_y / 2
        self.boundaries[3] = y + scale_y / 2

        self.correct_boundaries()

    def allow_zooming(self, bool):
        self.zoomingDisabled = not bool

    def allow_dragging(self, bool):
        self.draggingDisabled = not bool

    def get_mouse_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.position_in_window[0] <= mouse_pos[0] <= self.position_in_window[0] + self.WIDTH and \
                self.position_in_window[1] <= mouse_pos[1] <= self.position_in_window[1] + self.HEIGHT:
            # If mouse is on image
            return mouse_pos[0] - self.position_in_window[0], mouse_pos[1] - self.position_in_window[1]
        else:
            return False

    def correct_boundaries(self):
        if self.boundaries[0] < 0:
            self.boundaries[1] += abs(self.boundaries[0])
            self.boundaries[0] = 0

        if self.boundaries[1] > self.WIDTH:
            self.boundaries[0] -= self.boundaries[1] - self.WIDTH
            self.boundaries[1] = self.WIDTH

        if self.boundaries[2] < 0:
            self.boundaries[3] += abs(self.boundaries[2])
            self.boundaries[2] = 0

        if self.boundaries[3] > self.HEIGHT:
            self.boundaries[2] -= self.boundaries[3] - self.HEIGHT
            self.boundaries[3] = self.HEIGHT

    def update_boundaries(self, operation):
        scale_x = (self.boundaries[1] - self.boundaries[0]) * self.zoom_strength
        scale_y = (self.boundaries[3] - self.boundaries[2]) * self.zoom_strength
        mouse_pos = self.get_mouse_pos()
        if mouse_pos is False:
            return
        mouse_x = mouse_pos[0] / self.WIDTH
        mouse_y = mouse_pos[1] / self.HEIGHT

        if operation == "zoom in":
            self.boundaries[0] += scale_x * mouse_x
            self.boundaries[1] -= scale_x * (1 - mouse_x)
            self.boundaries[2] += scale_y * mouse_y
            self.boundaries[3] -= scale_y * (1 - mouse_y)
        elif operation == "zoom out":
            self.boundaries[0] -= scale_x * mouse_x
            self.boundaries[1] += scale_x * (1 - mouse_x)
            self.boundaries[2] -= scale_y * mouse_y
            self.boundaries[3] += scale_y * (1 - mouse_y)
        self.zoom = self.WIDTH / (self.boundaries[1] - self.boundaries[0])

        if self.zoom <= 1:
            self.zoom = 1
            self.boundaries = [0, self.WIDTH, 0, self.HEIGHT]
            return

        self.correct_boundaries()

    def update_zoom(self):
        # If mouse is not on image, exit
        if self.get_mouse_pos() is False or self.zoomingDisabled:
            self.last_point = None
            return

        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    self.update_boundaries("zoom in")
                elif e.button == 5:
                    if self.zoom > 1:
                        self.update_boundaries("zoom out")
                elif e.button == 1:
                    self.last_point = self.get_mouse_pos()
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self.last_point = None
            elif e.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] == 1:
                mouse_pos = self.get_mouse_pos()
                if mouse_pos is False:
                    continue

                if self.last_point is None:
                    self.last_point = mouse_pos
                    continue

                if not self.draggingDisabled:
                    offset_x = ((self.last_point[0] - mouse_pos[0]) / self.WIDTH) * (
                                self.boundaries[1] - self.boundaries[0])
                    offset_y = ((self.last_point[1] - mouse_pos[1]) / self.HEIGHT) * (
                                self.boundaries[3] - self.boundaries[2])

                    if self.boundaries[0] >= 0 and self.boundaries[1] <= self.WIDTH:
                        self.boundaries[0] += offset_x
                        self.boundaries[1] += offset_x

                    if self.boundaries[2] >= 0 and self.boundaries[3] <= self.HEIGHT:
                        self.boundaries[2] += offset_y
                        self.boundaries[3] += offset_y

                    self.correct_boundaries()
                    self.last_point = mouse_pos


