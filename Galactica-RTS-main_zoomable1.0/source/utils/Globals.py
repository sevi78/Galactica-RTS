# initialize pygame and window

import pygame

from source.utils.saveload import *

# load settings
settings = load_file("settings.json")

#pygame.init()

global WIDTH
WIDTH = int(settings["WIDTH"][0][0])  # windowsize[0]

global HEIGHT
HEIGHT = int(settings["HEIGHT"][0][0])  # windowsize[1]

global win
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
# root path
# dirty hack to get version of the game based on the folder name
file_path = os.path.dirname(os.path.realpath(__file__))
abs_root = os.path.split(file_path)[0]

global root
root = abs_root.split(os.sep)[-1]

# load all Images

# global images
# images = source.utils.Images.images

dirpath = os.path.dirname(os.path.realpath(__file__))

global pictures_path
pictures_path = os.path.split(dirpath)[0].split("source")[0] + "pictures" + os.sep

# colors

# global colors
# colors = Colors()

# Sounds
from source.utils.sounds import Sounds

global sounds
sounds = Sounds()

# Game variables
global moveable
moveable = settings["moveable"]  # True

global app
app = None

global tooltip_text
tooltip_text = ""

global game_paused
game_paused = False

global time_factor
time_factor = int(settings["time_factor"])  # 1

global game_speed
game_speed = int(settings["game_speed"])  # 10

global fps
fps = int(settings["fps"])  # 60

global scene_width
scene_width = int(settings["scene_width"])  # 60

global scene_height
scene_height = int(settings["scene_height"])  # 60

global draw_background_image
draw_background_image = settings["draw_background_image"]

global building_editor_draw
building_editor_draw = False

global enable_zoom
enable_zoom = settings["enable_zoom"]  # False

global enable_pan
enable_pan = settings["enable_pan"]

global debug
debug = False

global enable_orbit
enable_orbit = settings["enable_orbit"]

global enable_game_events
enable_game_events = settings["enable_game_events"]

global show_orbit
show_orbit = False

global show_grid
show_grid = False
