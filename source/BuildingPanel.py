import time

import pygame
from pygame_widgets.util import drawText

import source.Sounds
import source.BuildingEditor
import source.Globals
import source.PlanetEditor
import source.Settings
from source.Button import Button, ImageButton
from source.Globals import pictures_path
from source.Navigation import Navigation
from source.Slider import Slider
from source.WidgetHandler import WidgetBase


class BuildingPanel(WidgetBase):
    """
    displays the planets buildings, population , production
    """

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)

        self.planet_building_text = None
        self.planet_text = None
        self.hover = False
        self.singleton_buildings_images = {}
        self.singleton_buildings = []
        self.layer = kwargs.get("layer", 9)
        self.parent = kwargs.get("parent")
        self.frame_color = source.Globals.colors.frame_color
        self.clockslider_height = 7
        self.time_factor = 1
        self.year = 77812
        self.bg_color = pygame.colordict.THECOLORS["black"]
        self.font = pygame.font.SysFont(None, 18)
        self.resource_image_size = (15, 15)
        self.x = 0
        self.y = 0
        self.startTime = time.time()

        # construct surface
        self.surface = pygame.surface.Surface((width, height))
        self.surface.fill(self.bg_color)
        self.surface.set_alpha(19)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.x = x
        self.surface_rect.y = y
        self.size_x = kwargs.get("size_x")
        self.size_y = kwargs.get("size_y")
        self.spacing = kwargs.get("spacing")
        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, 1)

        # construct planet_surface
        self.planet_surface_size_y = 600
        self.planet_surface = pygame.surface.Surface((width, self.planet_surface_size_y))
        self.planet_surface.fill(self.bg_color)
        self.planet_surface.set_alpha(0)
        self.planet_surface_rect = self.planet_surface.get_rect()
        self.planet_surface_rect.x = x
        self.planet_surface_rect.y = y + self.surface.get_height()
        self.planet_surface_frame = pygame.draw.rect(self.win, self.frame_color, self.planet_surface_rect, 1)

        # planet image
        self.planet_image = None

        # construct slider
        self.spacing_x = 35
        self.clock_slider = Slider(win=self.win,
            x=self.surface_rect.x + self.spacing_x + self.spacing_x,
            y=self.surface_rect.y + int(self.spacing / 2),
            width=self.surface_rect.width - self.spacing - self.spacing_x * 2,
            height=self.clockslider_height,
            min=1, max=15, step=1, handleColour=pygame.color.THECOLORS["blue"], layer=self.layer)

        self.clock_slider.colour = self.frame_color
        self.clock_slider.setValue(source.Globals.game_speed)

        # construct texts
        self.time_warp_text = self.font.render(str(self.clock_slider.getValue()) + "x", True, self.frame_color)
        self.year_text = self.parent.ui_helper.hms(self.year)

        # construct icon
        self.image = source.Globals.images[pictures_path]["icons"]["clock.png"]
        self.image_size = self.image.get_size()
        self.clock_icon = Button(win=self.win,
            x=self.surface_rect.x + (self.spacing / 2),
            y=self.surface_rect.y + (self.spacing / 2),
            width=self.image_size[0],
            height=self.image_size[1],
            isSubWidget=False,
            image=self.image,
            tooltip="this is the time, don't waste it !",
            frame_color=self.frame_color,
            transparent=True,
            onClick=lambda: self.clock_slider.setValue(1),
            parent=self.parent, layer=self.layer
            )

        self.arrow_size = 15
        self.minus_arrow_button = Button(win=self.win,
            x=self.clock_icon.getX() + self.spacing * 2,
            y=self.clock_slider.getY() - self.clock_slider.getHeight() - 2,
            width=self.image_size[0],
            height=self.image_size[1],
            isSubWidget=False,
            image=pygame.transform.scale(
                source.Globals.images[pictures_path]["icons"]["arrow-left.png"], (self.arrow_size, self.arrow_size)),
            tooltip="decrease time",
            frame_color=self.frame_color,
            transparent=True,
            onClick=lambda: self.set_clockslider_value(-1),
            parent=self.parent, layer=self.layer
            )

        self.plus_arrow_button = Button(win=self.win,
            x=self.clock_icon.getX() + self.spacing * 2 + self.arrow_size,
            y=self.clock_slider.getY() - self.clock_slider.getHeight() - 2,
            width=self.image_size[0],
            height=self.image_size[1],
            isSubWidget=False,
            image=pygame.transform.scale(
                source.Globals.images[pictures_path]["icons"]["arrow-right.png"], (self.arrow_size, self.arrow_size)),
            tooltip="increase time",
            frame_color=self.frame_color,
            transparent=True,
            onClick=lambda: self.set_clockslider_value(+1),
            parent=self.parent, layer=self.layer
            )
        self.parent.icons.append(self.clock_icon)

        # settings icon
        self.settings_icon = ImageButton(win=self.win,
            x=self.getX() - 25,
            y=self.clock_slider.getY(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(source.Globals.images[pictures_path]["icons"]["settings_40x40.png"], (25, 25)),
            tooltip="settings: WARNING! Closes Game if clicked, work in progress...",
            frame_color=source.Globals.colors.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: source.Settings.main(surface=self.win))

        # ships

        # ship icon
        self.spacehunter_icon = ImageButton(win=self.win,
            x=self.settings_icon.getX() - 25,
            y=self.clock_slider.getY(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                source.Globals.images[pictures_path]["ships"]["spacehunter_30x30.png"], (25, 25)),
            tooltip="navigate to this ship, not working yet",
            frame_color=source.Globals.colors.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: Navigation.navigate_to(self.parent.navigation, "spacehunter"))

        self.info_icon = ImageButton(win=self.win,
            x=self.spacehunter_icon.getX() - 25,
            y=self.clock_slider.getY(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(source.Globals.images[pictures_path]["icons"]["info_30x30.png"], (25, 25)),
            tooltip="information about game controls",
            frame_color=source.Globals.colors.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: self.set_info_text())

        self.planet_editor_icon = ImageButton(win=self.win,
            x=self.info_icon.getX() - 50,
            y=self.clock_slider.getY(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                source.Globals.images[pictures_path]["planets"]["Zeta Bentauri_60x60.png"], (25, 25)),
            tooltip="open planet editor",
            frame_color=source.Globals.colors.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: source.PlanetEditor.main(surface=self.win))

        self.building_editor_icon = ImageButton(win=self.win,
            x=self.info_icon.getX() - 50,
            y=self.clock_slider.getY(),
            width=25,
            height=25,
            isSubWidget=False,
            parent=self,
            image=pygame.transform.scale(
                source.Globals.images[pictures_path]["icons"]["building_icon.png"], (25, 25)),
            tooltip="open building editor",
            frame_color=source.Globals.colors.frame_color,
            moveable=False,
            include_text=True, layer=self.layer,
            onClick=lambda: source.BuildingEditor.main(surface=self.win))


    def set_global_variable(self, key, value):
        setattr(source.Globals, key, value)

    def set_info_text(self):
        source.Globals.app.info_panel.text = "Ship: rightclick to move to a planet, or reload the ship. \n\n ctrl and mouse click to navigate \n\n" \
                                             "numbers 1-9 to make layers visible or not \n\nb to open build menu"

    def set_clockslider_value(self, value):
        if value < 0:
            if self.clock_slider.min + 1 < self.clock_slider.getValue() - value:
                self.clock_slider.setValue(self.clock_slider.getValue() + value)
        elif value > 0:
            if self.clock_slider.max + 1 > self.clock_slider.getValue() + value:
                self.clock_slider.setValue(self.clock_slider.getValue() + value)

    def listen(self, events):
        # set tooltip text and destroys building
        self.hover = False
        for event in events:
            for building_name, image_rect in self.singleton_buildings_images.items():
                if image_rect.collidepoint(pygame.mouse.get_pos()):
                    self.hover = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.destroy_building(building_name)
                    else:
                        if source.Globals.tooltip_text == "":
                            source.Globals.tooltip_text = f"Are you sure you want to destroy this {building_name}? You will probably not get anything back."
            if not self.hover:
                if source.Globals.tooltip_text.startswith("Are you sure you want to destroy this"):
                    source.Globals.tooltip_text = ""

    def set_planet_building_display(self):
        """ sets text to the planet building texts based on buildings"""
        buildings = "None"
        if self.parent.selected_planet:
            buildings = ""
            for i in self.parent.selected_planet.buildings:
                buildings += i + ", "

        return buildings

    def set_planet_production_display(self):
        """ sets text to the planet building texts based on production"""
        text = "None"
        if self.parent.selected_planet:
            text += ""

        return text

    def reposition(self):
        win = pygame.display.get_surface()
        width = win.get_width()
        height = win.get_height()
        # reposition
        self.surface_rect.x = width - self.surface.get_width()
        self.clock_icon._x = self.surface_rect.x + (self.spacing / 2)
        self.clock_slider._x = self.surface_rect.x + self.spacing_x + self.spacing_x
        self.planet_surface_rect.x = self.surface_rect.x
        self.minus_arrow_button._x = self.clock_icon.getX() + self.spacing * 2 + 3
        self.plus_arrow_button._x = self.clock_icon.getX() + self.spacing * 2 + self.arrow_size + 3
        self.settings_icon._x = self.clock_icon.getX() - self.spacing - self.settings_icon.getWidth()
        self.spacehunter_icon._x = self.settings_icon._x - self.spacing - self.settings_icon.getWidth()
        self.info_icon._x = self.spacehunter_icon._x - self.spacing - self.settings_icon.getWidth()
        self.planet_editor_icon._x = self.info_icon._x - self.spacing - self.settings_icon.getWidth()
        self.building_editor_icon._x = self.planet_editor_icon._x - self.spacing - self.settings_icon.getWidth()

    def destroy_building(self, b):
        print("destroy_building", b)
        self.parent.selected_planet.buildings.remove(b)
        self.parent.selected_planet.calculate_production()
        self.parent.selected_planet.calculate_population()
        self.parent.event_text = f"you destroyed one {b}! You will not get anything back from it! ... what a waste ..."
        source.sounds.play_sound(source.sounds.destroy_building)

    def update_time(self):
        self.year += 0.01 * self.time_factor
        source.Globals.time_factor = self.time_factor

    def draw(self):
        """
        draws the ui elements
        :return:
        """
        self.reposition()

        # TIME__________________________________________________________________________________________________________
        # draw surface and frame
        # self.win.blit(self.surface,self.surface_rect)
        self.update_time()

        # frame
        self.surface_frame = pygame.draw.rect(self.win, self.frame_color, self.surface_rect, 1)
        self.win.blit(self.surface, self.surface_frame)

        # clock
        self.time_warp_text = self.font.render(str(self.clock_slider.getValue()) + "x", True, self.frame_color)
        self.win.blit(self.time_warp_text,
            (self.surface_rect.x + self.spacing_x, self.clock_icon._y + self.clock_icon.imageRect.height / 2))

        self.year_text = self.font.render("year: " + str(round(self.year, 2)), True, self.frame_color)
        self.win.blit(self.year_text, (self.surface_rect.x + self.spacing_x + self.spacing_x,self.clock_icon._y +
                                       self.clock_icon.getHeight() - self.year_text.get_height()))
        self.time_factor = self.clock_slider.getValue()

        # PLANET Image _________________________________________________________________________________________________
        # draw planet_surface and frame
        # self.win.blit(self.planet_surface, self.planet_surface_rect)
        self.planet_surface_frame = pygame.draw.rect(self.win, self.frame_color, self.planet_surface_rect, 1)
        self.win.blit(self.planet_surface, self.planet_surface_frame)

        # UI____________________________________________________________________________________________________________
        x = self.planet_surface_rect.x
        self.y = self.planet_surface_rect.y + self.spacing

        # planet text
        self.planet_text = drawText(self.win, self.parent.set_planet_name(), source.Globals.colors.frame_color,
            (x, self.y, self.getWidth(), self.planet_surface.get_height()), self.font, "center")

        x = self.planet_surface_rect.x + self.spacing
        self.y += self.spacing * 2

        if self.parent.selected_planet:
            # draw population text
            # population
            drawText(self.win, "population: " + str(int(self.parent.selected_planet.population)) + "/" + str(int(self.parent.selected_planet.population_limit)), self.frame_color, (
                x + self.spacing_x, self.y, self.getWidth(), 20), self.font, "left")
            image = source.Globals.images[pictures_path]["resources"]["city_25x25.png"]

            self.win.blit(image, (x, self.y))

            self.y += self.spacing * 3

            # draw background planet icon
            name = self.parent.selected_planet.name
            pic = name + "_150x150.png"

            if pic in source.Globals.images[pictures_path]["planets"].keys():
                self.planet_image = source.Globals.images[pictures_path]["planets"][pic]
            else:
                self.planet_image = pygame.transform.scale(self.parent.selected_planet.image.copy(), (150, 150))

            self.planet_image.set_alpha(128)
            self.win.blit(self.planet_image, self.planet_surface_rect.midtop)

            # buildings ________________________________________________________________________________________________
            self.singleton_buildings = []

            for sb in self.parent.selected_planet.buildings:
                if not sb in self.singleton_buildings:
                    self.singleton_buildings.append(sb)

            self.singleton_buildings_images = {}

            y = 0
            for b in self.singleton_buildings:
                # because of the dynamic creation of this panel, we cannot use a button, this would lead to memory leaks
                # and performance problems - so we just blit an image and get its rect as button surface

                image = pygame.transform.scale(source.Globals.images[pictures_path]["buildings"][b + "_25x25.png"],
                    self.resource_image_size)

                # get rect for storage
                image_rect = image.get_rect()
                image_rect.x = x
                image_rect.y = self.y + y

                # store it
                self.singleton_buildings_images[b] = image_rect

                # blit it
                self.win.blit(image, image_rect)

                # building count
                value = self.parent.selected_planet.buildings.count(b)
                text = self.font.render(b + ": " + str(value) + "x", True, self.frame_color)
                self.win.blit(text, (x + self.spacing_x, self.y + y))

                y += self.spacing * 2

            self.y += y + self.spacing

            # PRODUCTION________________________________________________________________________________________________
            # production label
            self.planet_building_text = drawText(self.win, "production: ", source.Globals.colors.frame_color, (
                self.planet_surface_rect.x,
                self.y, self.getWidth(),
                self.planet_surface.get_height()), self.font, "center")

            # production images and texts
            x = self.planet_surface_rect.x + self.spacing
            # self.y = self.planet_surface_rect.y + self.spacing * 15
            self.y += self.spacing * 3

            resources = self.parent.resources

            for r in resources:
                image = pygame.transform.scale(
                    source.Globals.images[pictures_path]["resources"][r + "_25x25.png"], self.resource_image_size)
                self.win.blit(image, (x, self.y))
                value = getattr(self.parent.selected_planet, "production_" + r)
                text = self.font.render(r + ": " + str(value), True, self.frame_color)
                self.win.blit(text, (x + self.spacing_x, self.y))

                self.y += self.spacing * 2
            self.y += self.spacing * 2

            # GLOBAL PRODUCTION_________________________________________________________________________________________
            # global production label
            self.planet_building_text = drawText(self.win, "global production: ", source.Globals.colors.frame_color, (
                self.planet_surface_rect.x,
                self.y, self.getWidth(),
                self.planet_surface.get_height()), self.font, "center")

            self.y += self.spacing * 3

            for r in resources:
                image = pygame.transform.scale(
                    source.Globals.images[pictures_path]["resources"][r + "_25x25.png"], self.resource_image_size)
                self.win.blit(image, (x, self.y))

                value = self.parent.player.production[r]
                text = self.font.render(r + ": " + str(value), True, self.frame_color)
                self.win.blit(text, (x + self.spacing_x, self.y))

                self.y += self.spacing * 2

        # adjust frame size_y
        self.planet_surface_rect.__setattr__("height", self.y - self.spacing * 3)
