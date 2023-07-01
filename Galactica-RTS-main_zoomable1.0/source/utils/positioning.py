import math

import pygame
from pygame_widgets.util import drawText

import source
from source.utils.Globals import debug


def get_distance(pos_a, pos_b):
    """
    returns the distance betweeen two positions
    :param pos_a:
    :param pos_b:
    :return: distance
    """
    x = pos_a[0]
    y = pos_a[1]
    x1 = pos_b[0]
    y1 = pos_b[1]

    dist_x = (x1 - x)
    dist_y = (y1 - y)
    distance = math.dist((x, y), (x1, y1))

    return distance


def limit_positions(obj):
    """
    this hides the obj if it is outside the screen
    """
    win = pygame.display.get_surface()
    test = 100
    zero = 0
    win_width = win.get_width()
    win_height = win.get_height()
    x = obj.getX()
    y = obj.getY()
    if hasattr(obj, "center"):
        obj.set_center()
    #
    # if obj.type == "star" and not obj._hidden and x in range(-10, 10):
    #     print ("x, y, obj.getWidth(), obj._hidden", x, y, obj.getWidth(), obj._hidden)

    if hasattr(obj, "property"):
        if obj.property == "ship" or obj.property == "planet":
            pass
        else:
            hide_obj_outside_view(obj, win_height, win_width, x, y, zero)
    else:
        hide_obj_outside_view(obj, win_height, win_width, x, y, zero)


def hide_obj_outside_view(obj, win_height, win_width, x, y, zero):
    if x <= zero or x >= win_width:
        obj.hide()
    elif y <= zero or y >= win_height:
        obj.hide()
    else:
        obj.show()


def debug_positions(x, y, color, text, size, **kwargs):
    if not debug:
        return
    # color = kwargs.get("color", "red")
    # x,y = kwargs.get("x"), kwargs.get("y")
    # size = kwargs.get("size")
    text = text + str(int(x)) + ", " + str(int(y))
    text_spacing = 15

    pygame.draw.circle(source.win, color, (x, y), size, 1)
    font = pygame.font.SysFont(None, 18)
    drawText(source.win, text, color, (x, y, 400, 30), font, "left")