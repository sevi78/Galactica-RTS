from pygame.event import Event
from pygame_widgets import Mouse

from source.gui.WidgetHandler import WidgetHandler

print ("__init__.py")

def update(events: [Event]):
    Mouse.updateMouseState()
    WidgetHandler.main(events)
