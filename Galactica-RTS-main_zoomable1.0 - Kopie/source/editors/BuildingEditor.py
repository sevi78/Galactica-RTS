"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - MULTI-INPUT
Shows different inputs (widgets).
"""

__all__ = ['main']

import pygame_menu

import source.utils.Globals
from source.utils import colors
from source.utils.config import load_settings, prices, build_population_minimum, building_production_time, production
from source.utils.saveload import write_file

# Constants and global variables
FPS = 60
WINDOW_SIZE = (840, 680)
global settings_run
settings_run = True

"""
todo: main() should be __init__ of class BuildingEditor. 
this class should be stored in app.(UIBuilder).
if settings_run: should be in draw() of class wich calls the mainloop.

"""


def main(test: bool = False, **kwargs) -> None:
    surface = source.utils.Globals.win

    # -------------------------------------------------------------------------
    # Theme setting
    # -------------------------------------------------------------------------
    settings_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
    settings_menu_theme.title_offset = (5, -2)
    settings_menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
    settings_menu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_LIGHT
    settings_menu_theme.widget_font_size = 20

    # ___________________________________________________________________________________________________________________
    # create price menu
    # ___________________________________________________________________________________________________________________

    prices_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.85,
        theme=settings_menu_theme,
        title='Building Prices:',
        width=WINDOW_SIZE[0] * 0.9, )

    # # get name and dict, create text input for name, min population, production time
    load_settings()
    for building, dict in prices.items():
        prices_menu.add.text_input(
            building + ":",
            maxwidth=0,
            textinput_id=building,
            input_underline='',
            align=pygame_menu.locals.ALIGN_CENTER,
            input_type=pygame_menu.locals.INPUT_INT,
            fontcolor=colors.frame_color)

        prices_menu.add.text_input(
            "minimum population to build:",
            maxwidth=0,
            textinput_id=building + ".minimum population",
            default=build_population_minimum[building],
            input_underline='',
            align=pygame_menu.locals.ALIGN_LEFT,
            input_type=pygame_menu.locals.INPUT_INT,
            fontcolor=colors.frame_color)

        prices_menu.add.text_input(
            "building production time:",
            maxwidth=0,
            textinput_id=building + ".building_production_time",
            default=building_production_time[building],
            input_underline='',
            align=pygame_menu.locals.ALIGN_LEFT,
            input_type=pygame_menu.locals.INPUT_INT,
            fontcolor=colors.frame_color)

        # get resource and value, create text input for value
        for resource, value in dict.items():
            prices_menu.add.text_input(
                resource + ': ',
                default=value,
                maxwidth=0,
                textinput_id=building + "." + resource,
                input_underline='',
                align=pygame_menu.locals.ALIGN_LEFT,
                input_type=pygame_menu.locals.INPUT_INT)
        prices_menu.add.none_widget("none_widget" + building)

    def data_fun_prices() -> None:
        """
        Print data of the menu.
        """
        data = prices_menu.get_input_data()
        print('Settings data:', data)
        for k in data.keys():
            print(f'\t{k}\t=>\t{data[k]}')

        # store data into file
        write_file("buildings_prices.json", data)

    # Add final buttons
    prices_menu.add.button('Store data', data_fun_prices, button_id='store')  # Call function
    prices_menu.add.button('Restore original values', prices_menu.reset_value)
    prices_menu.add.button('Return to main menu', pygame_menu.events.BACK,
        align=pygame_menu.locals.ALIGN_LEFT)
    # ___________________________________________________________________________________________________________________
    # create production menu
    # ___________________________________________________________________________________________________________________

    production_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.85,
        theme=settings_menu_theme,
        title='Building Production:',
        width=WINDOW_SIZE[0] * 0.9, )

    # get name and dict, create text input for name
    for building, dict in production.items():
        production_menu.add.text_input(
            building + ":",
            maxwidth=0,
            textinput_id=building,
            input_underline='',
            align=pygame_menu.locals.ALIGN_CENTER,
            input_type=pygame_menu.locals.INPUT_INT,
            fontcolor=colors.frame_color)

        # get resource and value, create text input for value
        for resource, value in dict.items():
            production_menu.add.text_input(
                resource + ': ',
                default=value,
                maxwidth=0,
                textinput_id=building + "." + resource,
                input_underline='',
                align=pygame_menu.locals.ALIGN_LEFT,
                input_type=pygame_menu.locals.INPUT_INT)

    def data_fun_production() -> None:
        """
        Print data of the menu.
        """
        data = production_menu.get_input_data()
        print('Settings data:', data)
        for k in data.keys():
            print(f'\t{k}\t=>\t{data[k]}')

        # store data into file
        write_file("buildings_production.json", data)

    # Add final buttons
    production_menu.add.button('Store data', data_fun_production, button_id='store')  # Call function
    production_menu.add.button('Restore original values', prices_menu.reset_value)
    production_menu.add.button('Return to main menu', pygame_menu.events.BACK,
        align=pygame_menu.locals.ALIGN_LEFT)

    # -------------------------------------------------------------------------
    # Create menus: Main menu
    # -------------------------------------------------------------------------
    main_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
    main_menu_theme.title_font = pygame_menu.font.FONT_COMIC_NEUE
    main_menu_theme.widget_font = pygame_menu.font.FONT_COMIC_NEUE
    main_menu_theme.widget_font_size = 30

    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1],
        onclose=pygame_menu.events.BACK,  # User press ESC button
        theme=main_menu_theme,
        title='Building Editor',
        width=WINDOW_SIZE[0])

    main_menu.add.button('Building Prices', prices_menu)
    main_menu.add.button('Building Production', production_menu)

    if settings_run:
        main_menu.mainloop(surface, None, disable_loop=False, fps_limit=FPS, clear_surface=False)
