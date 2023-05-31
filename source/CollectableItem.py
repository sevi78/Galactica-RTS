import source.Globals
from source.AppHelper import get_distance
from source.Button import Button, Moveable
from source.Sounds import sounds

class CollectableItem(Button,Moveable):
    def __init__(self, win, x, y, width, height,  **kwargs):
        Button.__init__(self, win, x, y, width, height, **kwargs)
        Moveable.__init__(self,x,y,width,height, kwargs)
        self.moveable = False
        self.explored = False
        self.property = "item"
        self.onClick = lambda: self.execute(kwargs)
        self.collectable = True
        self.layer = kwargs.get("layer", 1)
        self.parent = kwargs.get("parent")
        self.image = kwargs.get("image")
        self.info_text = kwargs.get("infotext")
        self.energy = kwargs.get("energy", 0)
        self.food = kwargs.get("food", 0)
        self.minerals = kwargs.get("minerals", 0)
        self.water = kwargs.get("water", 0)
        self.population = kwargs.get("population", 0)
        self.technology = kwargs.get("technology", None)
        self.resources =  {"water": self.water, "energy":self.energy, "food":self.food, "minerals":self.minerals}
        self.collect_text = ""

    def collect_resources(self, collector):
        for key, value in self.resources.items():
            if value > 0:
                self.collect_text += str(value) + " of " + key + " "
                setattr(collector, key, getattr(collector, key) + value)
                collector.set_resources()
                collector.set_info_text()
                sounds.play_sound(sounds.collect_success)

    def get_collected(self):
        collector = None
        # find the nearest ship
        for i in source.Globals.app.ships:
            dist = get_distance((self.getX(), self.getY()), (i.getX(), i.getY()))
            if dist <= 50:
                collector = i

        if collector:
            self.collect_resources(collector)
            source.Globals.app.event_text = "You are a lucky Guy! you just found some resources: " + self.collect_text
            # self.disable()
            # self.hide()
            self.__del__()

    def execute(self, kwargs):
        self.get_collected()

    def move(self, events):
        """
        calls the move function from the Button Class
        :param events:
        :return:
        """

        super().move(events,self)

    def get_explored(self):
        if not self.explored:
            for i in source.Globals.app.ships:
                dist = get_distance((self.getX(), self.getY()), (i.getX(), i.getY()))
                if dist <= i.fog_of_war_radius:
                    self.show()
                    self.enable()
                    self.explored = True
