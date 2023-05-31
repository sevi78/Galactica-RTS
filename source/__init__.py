from pygame.event import Event
from pygame_widgets.mouse import Mouse

from source.WidgetHandler import WidgetHandler as wh


def update(events: [Event]):
    Mouse.updateMouseState()
    wh.main(events)
