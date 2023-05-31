import os
from os.path import isfile, join
from pprint import pprint

import source
from source.Globals import pictures_path
from source.Levels import level_dict
from source.Planet import Planet

dict = {}



l = list(level_dict[1].keys())

for i in l:
    dict[str(l.index(i))] = i

#pprint (dict)


# gets values from save file(settings.json)
#settings = source.SaveLoad.load_file("planets" + os.sep + planet_name + ".json")



level = 1# self.level = 1 of app
moveable = source.Globals.moveable


#pictures_path = os.path.split(dirpath)[0] + os.sep + "pictures" + os.sep


def create_planets(level):
    """
    creates the ppanets based on the level from Lovels (level_dict)
    :param level:
    :return:
    """
    dirpath = os.path.dirname(os.path.realpath(__file__))
    database_path = os.path.split(dirpath)[0] + os.sep + "database" + os.sep
    level_path = database_path + "levels" + os.sep + "level" + str(level) + os.sep + "planets" + os.sep
    files = [f for f in os.listdir(level_path) if isfile(join(level_path, f))]

    for planet in files:

        # get with from image
        width = int(planet["image_name"].split("_")[1].split("x")[0])
        height = int(planet["image_name"].split("_")[1].split("x")[1].split(".png")[0])
        planet_button = Planet(win=source.Globals.win,
            x=int(planet["x"]),
            y=int(planet["y"]),
            width=width,
            height=height,
            isSubWidget=False,
            image=source.Globals.images[pictures_path]["planets"][planet["image_name"]],
            transparent=True,
            info_text=planet["info_text"],
            text=planet["name"],
            textColour=source.Globals.colors.frame_color,
            property="planet",
            name=planet["name"],
            parent=None,
            tooltip="send your ship to explore the planet!",
            possible_resources=planet["possible_resources"],
            moveable=moveable,
            hover_image=source.Globals.images[pictures_path]["icons"]["selection_150x150.png"],
            textVAlign="below_the_bottom",
            layer=3)
        #self.planet_buttons.append(planet_button)

    # # set orbit_object
    # sun = [i for i in self.planets if i.name == "Sun"][0]
    # for i in self.planets:
    #     if not i == sun:
    #         i.set_orbit_object(sun)