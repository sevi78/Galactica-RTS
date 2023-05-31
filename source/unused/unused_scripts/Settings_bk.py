
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - MULTI-INPUT
Shows different inputs (widgets).
"""

__all__ = ['main']

from typing import Tuple, Optional

import pygame
import pygame_menu
from pygame_menu.examples import create_example_window

import source.Globals
import source.SaveLoad

# Constants and global variables
FPS = 60
WINDOW_SIZE = (640, 480)

sound: Optional['pygame_menu.sound.Sound'] = None
surface: Optional['pygame.Surface'] = None
main_menu: Optional['pygame_menu.Menu'] = None


def main_background() -> None:
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    """
    surface.fill((40, 40, 40))





def update_menu_sound(value: Tuple, enabled: bool) -> None:
    """
    Update menu sound.

    :param value: Value of the selector (Label and index)
    :param enabled: Parameter of the selector, (True/False)
    """
    assert isinstance(value, tuple)
    if enabled:
        main_menu.set_sound(sound, recursive=True)
        print('Menu sounds were enabled')
    else:
        main_menu.set_sound(None, recursive=True)
        print('Menu sounds were disabled')


def main(test: bool = False, **kwargs) -> None:
    """
    Main program.

    :param test: Indicate function is being tested
    """

    # -------------------------------------------------------------------------
    # source.Globals
    # -------------------------------------------------------------------------
    global main_menu
    global sound
    global surface

    # -------------------------------------------------------------------------
    # Create window
    # -------------------------------------------------------------------------
    surface =  create_example_window('Galactica - Settings', WINDOW_SIZE,init_pygame=False)#kwargs.get("surface")
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Set sounds
    # -------------------------------------------------------------------------
    sound = pygame_menu.sound.Sound()

    # Load example sounds
    sound.load_example_sounds()

    # Disable a sound
    sound.set_sound(pygame_menu.sound.SOUND_TYPE_ERROR, None)

    # -------------------------------------------------------------------------
    # Create menus: Settings
    # -------------------------------------------------------------------------
    settings_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
    settings_menu_theme.title_offset = (5, -2)
    settings_menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
    settings_menu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_LIGHT
    settings_menu_theme.widget_font_size = 20

    # gets values from save file(settings.json)
    save = source.SaveLoad.load_save()


    # create menu
    settings_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.85,
        theme=settings_menu_theme,
        title='Settings',
        width=WINDOW_SIZE[0] * 0.9
    )

    settings_menu.add.text_input(
        'TODO: ',
        maxwidth=19,
        textinput_id='todo',
        input_underline='_'
    )
    settings_menu.add.text_input(
        'FPS: ',
        maxchar=3,
        default= int(save["fps"]),
        textinput_id='fps',
        input_underline='_'
    )

    # Selectable items
    widths = [("1920",),
             ("1400",),
             ("800",)]

    # Create selector with 3 options
    settings_menu.add.selector(
        'WIDTH:\t',
        widths,
        selector_id='width',
        default=save["width"][1]
    )

    heights = [("1080",),
              ("800",),
              ("600",)]

    # Create selector with 3 options
    settings_menu.add.selector(
        'HEIGHT:\t',
        heights,
        selector_id='height',
        default=save["height"][1]
        )

    # settings_menu.add.dropselect_multiple(
    #     title='Pick 3 colors',
    #     items=[('Black', (0, 0, 0)),
    #            ('Blue', (0, 0, 255)),
    #            ('Cyan', (0, 255, 255)),
    #            ('Fuchsia', (255, 0, 255)),
    #            ('Green', (0, 255, 0)),
    #            ('Red', (255, 0, 0)),
    #            ('White', (255, 255, 255)),
    #            ('Yellow', (255, 255, 0))],
    #     dropselect_multiple_id='pickcolors',
    #     max_selected=3,
    #     open_middle=True,
    #     selection_box_height=6  # How many options show if opened
    # )

    # Create switch
    settings_menu.add.toggle_switch('Navigation', save["navigation"],
                                    toggleswitch_id='navigation')

    settings_menu.add.toggle_switch('Moveable', save["moveable"],
                                    toggleswitch_id='moveable',
                                    )

    settings_menu.add.range_slider('Game Speed:', save["game_speed"], (1, 25), 1,
                                    rangeslider_id='game_speed',
                                    value_format=lambda x: str(int(x)))

    settings_menu.add.range_slider('Time Factor:', save["time_factor"], (1, 10), 1,
        rangeslider_id='time_factor',
        value_format=lambda x: str(int(x)))

    def data_fun() -> None:
        """
        Print data of the menu.
        """
        print('Settings data:')
        data = settings_menu.get_input_data()
        for k in data.keys():
            print(f'\t{k}\t=>\t{data[k]}')

        source.Globals.settings = data
        source.SaveLoad.write_save(data)

    # Add final buttons
    settings_menu.add.button('Store data', data_fun, button_id='store')  # Call function
    settings_menu.add.button('Restore original values', settings_menu.reset_value)
    settings_menu.add.button('Return to main menu', pygame_menu.events.BACK,
                             align=pygame_menu.locals.ALIGN_CENTER)

    # # -------------------------------------------------------------------------
    # # Create menus: More settings
    # # -------------------------------------------------------------------------
    # more_settings_menu = pygame_menu.Menu(
    #     height=WINDOW_SIZE[1] * 0.85,
    #     theme=settings_menu_theme,
    #     title='More Settings',
    #     width=WINDOW_SIZE[0] * 0.9
    # )
    #
    # more_settings_menu.add.image(
    #     pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU,
    #     scale=(0.25, 0.25),
    #     align=pygame_menu.locals.ALIGN_CENTER
    # )
    # more_settings_menu.add.color_input(
    #     'Color 1 RGB: ',
    #     color_type='rgb'
    # )
    # more_settings_menu.add.color_input(
    #     'Color 2 RGB: ',
    #     color_type='rgb',
    #     default=(255, 0, 0),
    #     input_separator='-'
    # )
    #
    # def print_color(color: Tuple) -> None:
    #     """
    #     Test onchange/onreturn.
    #
    #     :param color: Color tuple
    #     """
    #     print('Returned color: ', color)
    #
    # more_settings_menu.add.color_input(
    #     'Color in Hex: ',
    #     color_type='hex',
    #     hex_format='lower',
    #     color_id='hex_color',
    #     onreturn=print_color
    # )
    #
    # more_settings_menu.add.vertical_margin(25)
    # more_settings_menu.add.button(
    #     'Return to main menu',
    #     pygame_menu.events.BACK,
    #     align=pygame_menu.locals.ALIGN_CENTER
    # )

    # -------------------------------------------------------------------------
    # Create menus: Column buttons
    # -------------------------------------------------------------------------
    # button_column_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
    # button_column_menu_theme.background_color = pygame_menu.BaseImage(
    #     image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
    #     drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
    # )
    # button_column_menu_theme.widget_font_size = 25

    # button_column_menu = pygame_menu.Menu(
    #     columns=2,
    #     height=WINDOW_SIZE[1] * 0.45,
    #     rows=3,
    #     theme=button_column_menu_theme,
    #     title='Textures+Columns',
    #     width=WINDOW_SIZE[0] * 0.9
    # )
    # for i in range(4):
    #     button_column_menu.add.button(f'Button {i}', pygame_menu.events.BACK)
    # button_column_menu.add.button(
    #     'Return to main menu', pygame_menu.events.BACK,
    #     background_color=pygame_menu.BaseImage(
    #         image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_METAL
    #     )
    # ).background_inflate_to_selection_effect()

    # -------------------------------------------------------------------------
    # Create menus: Main menu
    # -------------------------------------------------------------------------
    main_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
    main_menu_theme.title_font = pygame_menu.font.FONT_COMIC_NEUE
    main_menu_theme.widget_font = pygame_menu.font.FONT_COMIC_NEUE
    main_menu_theme.widget_font_size = 30

    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        onclose=pygame_menu.events.EXIT,  # User press ESC button
        theme=main_menu_theme,
        title='Main menu',
        width=WINDOW_SIZE[0] * 0.8
    )

    main_menu.add.button('Settings', settings_menu)
    # main_menu.add.button('More Settings', more_settings_menu)
    # main_menu.add.button('Menu in textures and columns', button_column_menu)
    # main_menu.add.selector('Menu sounds ',
    #                        [('Off', False), ('On', True)],
    #                       onchange=update_menu_sound)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        #clock.tick(FPS)

        # Paint background
        main_background()

        # Main menu
        main_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
