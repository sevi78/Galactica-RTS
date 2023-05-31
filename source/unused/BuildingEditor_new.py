
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - MULTI-INPUT
Shows different inputs (widgets).
"""

#__all__ = ['main']

import pygame_menu
import source.Globals
import source.SaveLoad
# Constants and global variables
FPS = 60
WINDOW_SIZE = (840, 680)


class BuildingEditor:


    def __init__(self, **kwargs) -> None:
        self.surface = source.Globals.win

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

        self.prices_menu = pygame_menu.Menu(
            height=WINDOW_SIZE[1] * 0.85,
            theme=settings_menu_theme,
            title='Building Prices:',
            width=WINDOW_SIZE[0] * 0.9,)

        # get name and dict, create text input for name, min population, production time
        for building, dict in source.config.prices.items():
            self.prices_menu.add.text_input(
                                building + ":",
                                maxwidth=0,
                                textinput_id=building,
                                input_underline='',
                                align=pygame_menu.locals.ALIGN_CENTER,
                                input_type=pygame_menu.locals.INPUT_INT,
                                fontcolor= source.Globals.colors.frame_color)

            self.prices_menu.add.text_input(
                "minimum population to build:",
                maxwidth=0,
                textinput_id=building + ".minimum population",
                default= source.config.build_population_minimum[building],
                input_underline='',
                align=pygame_menu.locals.ALIGN_LEFT,
                input_type=pygame_menu.locals.INPUT_INT,
                fontcolor=source.Globals.colors.frame_color)

            self.prices_menu.add.text_input(
                "building production time:",
                maxwidth=0,
                textinput_id=building + ".building_production_time",
                default=source.config.building_production_time[building],
                input_underline='',
                align=pygame_menu.locals.ALIGN_LEFT,
                input_type=pygame_menu.locals.INPUT_INT,
                fontcolor=source.Globals.colors.frame_color)

            # get resource and value, create text input for value
            for resource, value  in dict.items():
                self.prices_menu.add.text_input(
                                    resource + ': ',
                                    default=value,
                                    maxwidth=0,
                                    textinput_id=building + "." + resource,
                                    input_underline='',
                                    align=pygame_menu.locals.ALIGN_LEFT,
                                    input_type = pygame_menu.locals.INPUT_INT)

        def data_fun_prices() -> None:
            """
            Print data of the menu.
            """
            data = self.prices_menu.get_input_data()
            print('Settings data:', data)
            for k in data.keys():
                print(f'\t{k}\t=>\t{data[k]}')

            # store data into file
            #source.Globals.settings = data
            source.SaveLoad.write_file("buildings_prices.json", data)

        # Add final buttons
        self.prices_menu.add.button('Store data', data_fun_prices, button_id='store')  # Call function
        self.prices_menu.add.button('Restore original values', self.prices_menu.reset_value)
        self.prices_menu.add.button('Return to main menu', pygame_menu.events.BACK,
                                 align=pygame_menu.locals.ALIGN_LEFT)
        # ___________________________________________________________________________________________________________________
        # create production menu
        # ___________________________________________________________________________________________________________________

        self.production_menu = pygame_menu.Menu(
            height=WINDOW_SIZE[1] * 0.85,
            theme=settings_menu_theme,
            title='Building Production:',
            width=WINDOW_SIZE[0] * 0.9,)

        # get name and dict, create text input for name
        for building, dict in source.config.production.items():
            self.production_menu.add.text_input(
                building + ":",
                maxwidth=0,
                textinput_id=building,
                input_underline='',
                align=pygame_menu.locals.ALIGN_CENTER,
                input_type=pygame_menu.locals.INPUT_INT,
                fontcolor=source.Globals.colors.frame_color)

            # get resource and value, create text input for value
            for resource, value in dict.items():
                self.production_menu.add.text_input(
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
            data = self.production_menu.get_input_data()
            print('Settings data:', data)
            for k in data.keys():
                print(f'\t{k}\t=>\t{data[k]}')

            # store data into file
            source.SaveLoad.write_file("buildings_production.json", data)

        # Add final buttons
        self.production_menu.add.button('Store data', data_fun_production, button_id='store')  # Call function
        self.production_menu.add.button('Restore original values', self.production_menu.reset_value)
        self.production_menu.add.button('Return to main menu', pygame_menu.events.BACK,
                                 align=pygame_menu.locals.ALIGN_LEFT)

        # -------------------------------------------------------------------------
        # Create menus: Main menu
        # -------------------------------------------------------------------------
        main_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
        main_menu_theme.title_font = pygame_menu.font.FONT_COMIC_NEUE
        main_menu_theme.widget_font = pygame_menu.font.FONT_COMIC_NEUE
        main_menu_theme.widget_font_size = 30

        self.main_menu = pygame_menu.Menu(
            height=WINDOW_SIZE[1] ,
            theme=main_menu_theme,
            title='Building Editor',
            width=WINDOW_SIZE[0],
            )

        self.main_menu.add.button('Building Prices', self.prices_menu)
        self.main_menu.add.button('Building Production', self.production_menu)
        self.main_menu.add.button('Exit', self.close_menu)


    def close_menu(self):

        source.Globals.building_editor_draw = False
        print("close_menu",source.Globals.building_editor_draw )
        self.main_menu.close()
    def draw(self):
        if source.Globals.building_editor_draw:
            self.main_menu.mainloop(self.surface, None, disable_loop= False, fps_limit=FPS, clear_surface=False)