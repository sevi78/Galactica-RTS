print ("__init__.py")
from pygame.event import Event
from pygame_widgets.mouse import Mouse
from pygame_widgets.util import drawText
from .WidgetHandler import WidgetHandler as wh, WidgetBase
from .Button import *
from .config import production, planet_positions
from .Globals import *
import source.AppHelper
#import BackgroundImage
import source.BuildingEditor
#import BuildingPanel
#import BuildingWidget
#import Button
#import CollectableItem
import source.Colors
import source.config
import source.EventPanel
#import FogOfWar
import source.Globals
import source.Icon
import source.Images
#import InfoPanel
import source.Levels
import source.Navigation
import source.paning_and_zooming
#import Planet
import source.Player
import source.ProgressBar
import source.SaveLoad
import source.Settings
#import Ship
#import Ships
#import Slider
import source.Sounds
import source.texts
import source.ToolTip
#import UIBuilder
#import UniverseBackground
import source.WidgetHandler
from .Sounds import sounds
def update(events: [Event]):
    Mouse.updateMouseState()
    wh.main(events)
