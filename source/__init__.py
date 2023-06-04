
from pygame.event import Event
from pygame_widgets.mouse import Mouse

from source.WidgetHandler import WidgetHandler as wh

from source.config import production, planet_positions

def update(events: [Event]):
    Mouse.updateMouseState()
    wh.main(events)
