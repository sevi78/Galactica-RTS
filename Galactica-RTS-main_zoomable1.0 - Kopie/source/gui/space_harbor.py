import pygame
from pygame_widgets.util import drawText
from source.gui.BuildingWidget import BuildingWidget
from source.gui import set_event_text, check_if_enough_resources_to_build
from source.gui.Button import ImageButton, Button
from source.gui.WidgetHandler import WidgetBase
from source.utils import colors, images, pictures_path, sounds
from source.utils.config import create_info_panel_ship_text, ship_prices


class SpaceHarbor(WidgetBase):
    """
    displays ship buttons to build spaceships
    """
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        self.parent = kwargs.get("parent", None)
        self.frame_color = colors.frame_color

        # construct surface
        self.surface = pygame.surface.Surface((width, height))
        self.surface.set_alpha(19)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.x = self.parent.surface_rect.x + self.parent.spacing
        self.surface_rect.y = self.parent.y
        self.spacing = self.parent.spacing
        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, 1)

        # text
        self.font = self.parent.font
        self.info_text = kwargs.get("infotext")

        # buttons
        self.spacehunter_button = ImageButton(win=self.win,
            x=self.getX(),
            y=self.getY(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                images[pictures_path]["ships"]["spacehunter_30x30.png"], (25, 25)),
            tooltip="build spacehunter",
            info_text= create_info_panel_ship_text("spacehunter"),
            frame_color=colors.frame_color,
            moveable=False,
            include_text=True,
            layer=self.layer,
            onClick=lambda: self.build_ship("spacehunter"),
            )

        self.cargoloader_button = ImageButton(win=self.win,
            x=self.getX() + self.getWidth()/2,
            y=self.getY(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                images[pictures_path]["ships"]["cargoloader_30x30.png"], (25, 25)),
            tooltip="build cargoloader",
            info_text=create_info_panel_ship_text("cargoloader"),
            frame_color=colors.frame_color,
            moveable=False,
            include_text=True,
            layer=self.layer,
            onClick=lambda: self.build_ship("cargoloader"),
            )

        self.spaceship_button = ImageButton(win=self.win,
            x=self.getX() + self.getWidth(),
            y=self.getY(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                images[pictures_path]["ships"]["spaceship_30x30.png"], (25, 25)),
            tooltip="build spaceship",
            info_text=create_info_panel_ship_text("spaceship"),
            frame_color=colors.frame_color,
            moveable=False,
            include_text=True,
            layer=self.layer,
            onClick=lambda: self.build_ship("spaceship"),
            )

        # initial hide the buttons
        self.spaceship_button.hide()
        self.cargoloader_button.hide()
        self.spacehunter_button.hide()

    def set_info_text(self):
        self.parent.parent.info_panel.text = self.info_text

    def set_visible(self):
        if not self.parent.parent.selected_planet:
            visible = False
            return visible

        if "space harbor" in self.parent.parent.selected_planet.buildings:
            self.spaceship_button.show()
            self.cargoloader_button.show()
            self.spacehunter_button.show()
            visible = True
        else:
            self.spaceship_button.hide()
            self.cargoloader_button.hide()
            self.spacehunter_button.hide()
            visible = False

        return visible

    def listen(self, events):
        pass

    def draw(self):
        if not self.set_visible():
            return

        # frame
        self.surface_rect.x = self.parent.surface_rect.x
        self.surface_rect.y = self.parent.y + self.spacing + 5
        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, 1)
        self.win.blit(self.surface, self.surface_frame)

        # label
        drawText(self.win, "Space Harbor", self.frame_color,
            (self.surface_rect.x + self.parent.spacing_x-36, self.surface_rect.y + self.spacing, self.getWidth(), 20), self.font, "center")

        # buttons
        self.spacehunter_button.setX(self.surface_rect.x + self.spacing * 3)
        self.spacehunter_button.setY(self.surface_rect.y + self.spacing + 20)

        self.spaceship_button.setX(self.surface_rect.x + self.getWidth()/2 - self.spaceship_button.getWidth()/2)
        self.spaceship_button.setY(self.surface_rect.y + self.spacing + 20)

        self.cargoloader_button.setX(self.surface_rect.x + self.getWidth() - self.cargoloader_button.getWidth() - self.spacing * 3)
        self.cargoloader_button.setY(self.surface_rect.y + self.spacing + 20)

    def build_ship(self, ship):
        price = ship_prices[ship]
        player = self.parent.parent.player
        app = self.parent.parent
        planet = app.selected_planet

        if check_if_enough_resources_to_build(ship):
            # pay
            for key, value in price.items():
                setattr(player, key, getattr(player, key) - value)

            # building widget
            widget_width = self.parent.getWidth()
            widget_height = 35
            spacing = 5

            # get the position and size
            win = pygame.display.get_surface()
            height = win.get_height()
            y = height - spacing - widget_height - widget_height * len(app.building_widget_list)

            sounds.play_sound(sounds.bleep2, channel=7)

            building_widget = BuildingWidget(win=app.win,
                x=app.building_panel._x,
                y=y,
                width=widget_width,
                height=widget_height,
                name=ship,
                fontsize=18,
                progress_time=5,
                parent=app,
                key="",
                value=0,
                planet=app.selected_planet,
                tooltip=ship, layer=4
                )

            # add building widget to building cue to make shure it can be build only if building_cue is < building_slots_amount
            planet.building_cue += 1
