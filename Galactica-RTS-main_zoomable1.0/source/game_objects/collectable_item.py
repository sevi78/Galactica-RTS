from pygame_widgets import Mouse
from pygame_widgets.mouse import MouseState

import source.utils.Globals
from source.gui import WidgetBase

from source.gui.Button import ImageButton, Moveable
from source.utils import get_distance
from source.utils.sounds import sounds


class CollectableItem(WidgetBase, Moveable):
    def __init__(self, win, x, y, width, height, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, **kwargs)
        #ImageButton.__init__(self, win, x, y, width, height, **kwargs)
        Moveable.__init__(self, x, y, width, height, kwargs)
        self.on_hover = None
        self.on_hover_release = False
        self.zoomable = True
        self.moveable = True
        self.explored = False
        self.property = "item"
        self.onClick = lambda: self.execute(kwargs)
        self.collectable = True
        self.layer = kwargs.get("layer", 1)
        self.parent = kwargs.get("parent")
        self.image = kwargs.get("image")
        self.image_raw = kwargs.get("image")
        self.imageRect = self.image.get_rect()
        self.info_text = kwargs.get("infotext")
        self.tooltip = kwargs.get("tooltip", None)
        self.energy = kwargs.get("energy", 0)
        self.food = kwargs.get("food", 0)
        self.minerals = kwargs.get("minerals", 0)
        self.water = kwargs.get("water", 0)
        self.population = kwargs.get("population", 0)
        self.technology = kwargs.get("technology", None)
        self.resources = {"water": self.water, "energy": self.energy, "food": self.food, "minerals": self.minerals, "technology": self.technology}
        self.collect_text = ""

        self.parent.collectables.append(self)

    def collect_resources(self, collector):
        for key, value in self.resources.items():
            if value > 0:
                self.collect_text += str(value) + " of " + key + " "
                if getattr(collector, key) + value > getattr(collector, key + "_max"):
                    setattr(collector, key, getattr(collector, key + "_max"))
                else:
                    setattr(collector, key, getattr(collector, key) + value)

                collector.set_resources()
                collector.set_info_text()
                sounds.play_sound(sounds.collect_success)

    def get_collected(self):
        collector = None
        # find the nearest ship
        for i in source.utils.Globals.app.ships:
            dist = get_distance((self.getX(), self.getY()), (i.getX(), i.getY()))
            if dist <= 150:
                collector = i

        if collector:
            self.collect_resources(collector)
            source.utils.Globals.app.event_text = "You are a lucky Guy! you just found some resources: " + self.collect_text
            self.__del__()

    def execute(self, kwargs):
        self.get_collected()

    def move(self, events):
        """
        calls the move function from the Button Class
        :param events:
        :return:
        """
        super().move(events, self)

    def get_explored(self):
        if not self.explored:
            for i in source.utils.Globals.app.ships:
                dist = get_distance((self.getX(), self.getY()), (i.getX(), i.getY()))
                if dist <= i.fog_of_war_radius:
                    self.show()
                    self.enable()
                    self.explored = True
    def draw(self, **kwargs):

        #self.set_screen_position(self._x, self._y)
        self.set_screen_position()
        self.win.blit(self.image, (self._x, self._y))

    def on_hover_release_callback(self, x, y):
        if self.contains(x, y):
            self.on_hover = True
            self.on_hover_release = False
        else:
            self.on_hover_release = True

        if self.on_hover and self.on_hover_release:
            self.on_hover = False

            return True

        return False

    def reset_tooltip(self):
        if not self._hidden:
            x, y = Mouse.getMousePos()
            if self.on_hover_release_callback(x, y):
                # print ("reseting tooltip: " ,self, self.name)
                source.utils.Globals.tooltip_text = ""
    def listen(self, events):
        self.reset_tooltip()
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                # print("Button.listen")
                if mouseState == MouseState.RELEASE and self.clicked:
                    self.clicked = False


                elif mouseState == MouseState.CLICK:
                    self.clicked = True
                    self.get_collected()

                elif mouseState == MouseState.DRAG and self.clicked:
                    pass

                elif mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                    pass

                    # set tooltip
                    if self.tooltip:
                        if self.tooltip != "":
                            source.utils.Globals.tooltip_text = self.tooltip


            else:
                self.clicked = False
    #
    #     print("CollectableItem.listen")