
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - MULTI-INPUT
Shows different inputs (widgets).
"""

__all__ = ['main']

import json
import os

import pygame_menu

import source.Globals
import source.SaveLoad

# Constants and global variables
FPS = 60
WINDOW_SIZE = (840, 680)
#
# sound: Optional['pygame_menu.sound.Sound'] = None
# surface: Optional['pygame.Surface'] = None
# main_menu: Optional['pygame_menu.Menu'] = None
global settings_run
settings_run = True


def quit_menu():
    print("quitting main_menu")
    settings_run = False

def main(test: bool = False, **kwargs) -> None:
    # global main_menu
    # global sound
    # global surface
    surface =  source.Globals.win#create_example_window('Galactica - Settings', WINDOW_SIZE,init_pygame=False)#kwargs.get("surface") #

    # -------------------------------------------------------------------------
    # Create menus: Settings
    # -------------------------------------------------------------------------
    settings_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
    settings_menu_theme.title_offset = (5, -2)
    settings_menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
    settings_menu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_LIGHT
    settings_menu_theme.widget_font_size = 20



    planet = source.Globals.app.selected_planet
    if not planet:
        return
    elif planet:
        planet_name = planet.name
        # create menu
        settings_menu = pygame_menu.Menu(
            height=WINDOW_SIZE[1] * 0.85,
            theme=settings_menu_theme,
            title=planet_name,
            width=WINDOW_SIZE[0] * 0.9,
            )

        # gets values from save file(settings.json)
        level = source.Globals.app.level
        dirpath = os.path.dirname(os.path.realpath(__file__))
        database_path = os.path.split(dirpath)[0] + os.sep + "database" + os.sep
        pictures_path = os.path.split(dirpath)[0] + os.sep + "pictures" + os.sep
        level_path = database_path + "levels" + os.sep + "level" + str(level) + os.sep

        with open(os.path.join(level_path + "planets" + os.sep + planet_name + ".json"), 'r+') as file:
            settings = json.load(file)


        # set images
        image_name_small = settings["image_name_small"]#level_dict[1][planet_name]["image_name"]
        image_name_big = settings["image_name_big"]#planet_name + "_150x150.png"

        # add images
        settings_menu.add.image(os.path.join(pictures_path + "planets" + os.sep + image_name_small))
        settings_menu.add.image(os.path.join(pictures_path + "planets" + os.sep + image_name_big))

        # iterate over planet_config, so we can add new fields to planet
        for key, value in planet.planet_config.__dict__.items():
            # check for type to make shure input is correct format
                if "int" in str(type(value)):
                    input_type = pygame_menu.locals.INPUT_INT

                if "str" in str(type(value)):
                    input_type = pygame_menu.locals.INPUT_TEXT

                if "float" in str(type(value)):
                    input_type = pygame_menu.locals.INPUT_FLOAT

                if "None" in str(type(value)):
                    input_type = pygame_menu.locals.INPUT_TEXT


                # ckeck if value exists and take value from file,  otherwise take default from planet_config
                if key in settings.keys():
                    default = settings[key]
                else:
                    default = str(value)
                    print (f"PlanetEditor error: could not find {key} in {planet_name}.json!")

                # construct text_input
                settings_menu.add.text_input(
                    str(key) + ': ',
                    default= default,
                    maxwidth=0,
                    textinput_id=key,
                    input_underline='',
                    align=pygame_menu.locals.ALIGN_LEFT,
                    input_type=input_type)

    def data_fun() -> None:
        """
        Print data of the menu.
        """
        data = settings_menu.get_input_data()
        print('Settings data:', data)
        for k in data.keys():
            print(f'\t{k}\t=>\t{data[k]}')

        # store data into file
        #source.Globals.settings = data
        #source.SaveLoad.write_file("planets" + os.sep + planet_name + ".json", data)
        with open(os.path.join(level_path + "planets" + os.sep + planet_name + ".json"), 'w') as file:
            json.dump(data, file)

    # Add final buttons

    settings_menu.add.vertical_fill(30, "vf")
    settings_menu.add.button('Store data', data_fun, button_id='store')  # Call function
    settings_menu.add.button('Restore original values', settings_menu.reset_value)
    settings_menu.add.button('Return to main menu', pygame_menu.events.BACK,
                             align=pygame_menu.locals.ALIGN_LEFT)

    # -------------------------------------------------------------------------
    # Create menus: Main menu
    # -------------------------------------------------------------------------
    main_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
    main_menu_theme.title_font = pygame_menu.font.FONT_COMIC_NEUE
    main_menu_theme.widget_font = pygame_menu.font.FONT_COMIC_NEUE
    main_menu_theme.widget_font_size = 30

    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] ,
        onclose=pygame_menu.events.BACK,  # User press ESC button
        theme=main_menu_theme,
        title='Planet Editor',
        width=WINDOW_SIZE[0]
    )

    main_menu.add.button('Planets', settings_menu)

    if settings_run:
        # Main menu
        main_menu.mainloop(surface, None, disable_loop=test, fps_limit=FPS, clear_surface=False)
