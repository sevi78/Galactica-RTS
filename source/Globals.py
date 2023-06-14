# initialize pygame and window
import os

import pygame

import source.SaveLoad

# load settings
settings = source.SaveLoad.load_file("settings.json")
# print (settings)

pygame.init()

global WIDTH
WIDTH = int(settings["width"][0][0])  # windowsize[0]

global HEIGHT
HEIGHT = int(settings["height"][0][0])  # windowsize[1]

global win
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

# root path
# dirty hack to get version of the game based on the folder name
file_path = os.path.dirname(os.path.realpath(__file__))
abs_root = os.path.split(file_path)[0]
global root
root = abs_root.split(os.sep)[-1]

# load all Images
import source.Images


global images
images = source.Images.images

dirpath = os.path.dirname(os.path.realpath(__file__))

global pictures_path
pictures_path = os.path.split(dirpath)[0] + os.sep + "pictures" + os.sep

# colors
from source.Colors import Colors

global colors
colors = Colors()

# Sounds
from source.Sounds import Sounds

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

# global build_menu_visible
# build_menu_visible = False
global frames_per_second
frames_per_second = int(settings["fps"])  # 60

global scene_width
scene_width = int(settings["scene_width"])  # 60

global scene_height
scene_height = int(settings["scene_height"])  # 60

global navigation
navigation = settings["navigation"]  # True

global draw_background_image
draw_background_image = settings["draw_background_image"]

# global set_building_editor_draw
# def set_building_editor_draw(value):
#     print ("set_building_editor_draw: ", value)
#     building_editor_draw = value

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

global show_orbit
show_orbit = False

global show_grid
show_grid = False

