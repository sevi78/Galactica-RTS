import os
from os.path import isfile, join

import pygame

pygame.init()


print ("main")
images = {}

dirpath = os.path.dirname(os.path.realpath(__file__))
pictures_path = os.path.split(dirpath)[0].split("source")[0] + "pictures" + os.sep


def load_folders(folder, dict):
    subfolders = [str(f.path).split(os.sep)[-1] for f in os.scandir(folder) if f.is_dir()]
    dict[folder] = {}

    for sub in subfolders:
        path = os.path.join(folder, sub)
        files = [f for f in os.listdir(path) if isfile(join(path, f))]
        # print (files)
        dict[folder][sub] = {}
        for image in os.listdir(path):
            filename, file_extension = os.path.splitext(image)
            if file_extension == ".png":
                img = pygame.image.load(os.path.join(folder, sub, image))
                img.convert_alpha()
                dict[folder][sub][image] = img  #


load_folders(os.path.join(pictures_path), images)
