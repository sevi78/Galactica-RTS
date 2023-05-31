import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from pygame_widgets.mouse import Mouse, MouseState

import source.Globals
from source.WidgetHandler import WidgetBase
from source.__init__ import update


class Moveable:
    def __init__(self,x,y,width,height, kwargs):
        self.ui_parent = kwargs.get("ui_parent", None)
        self.ui_parent_offset_x = 0
        self.ui_parent_offset_y = 0
        if self.ui_parent:
            try:
                self.ui_parent_offset_x = self.ui_parent.getX() - x
                self.ui_parent_offset_y = self.ui_parent.getY() - y
            except AttributeError:
                self.ui_parent_offset_x = self.ui_parent.get_rect().x - x
                self.ui_parent_offset_y = self.ui_parent.get_rect().y - y

    def update_position(self):
        """
        this sets the new position if object is moved.
        """
        if self.ui_parent != None:
            try:
                self.setX(self.ui_parent.getX() - self.ui_parent_offset_x)
                self.setY(self.ui_parent.getY() - self.ui_parent_offset_y)
            except AttributeError:
                self.setX(self.ui_parent.get_rect().x - self.ui_parent_offset_x)
                self.setY(self.ui_parent.get_rect().y - self.ui_parent_offset_y)


class ImageButton(WidgetBase, Moveable):
    """ A customisable button for Pygame

            :param win: Surface on which to draw
            :type win: pygame.Surface
            :param x: X-coordinate of top left
            :type x: int
            :param y: Y-coordinate of top left
            :type y: int
            :param width: Width of button
            :type width: int
            :param height: Height of button
            :type height: int
            :param kwargs: Optional parameters:
            """

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        Moveable.__init__(self,x,y,width,height, kwargs)
        self.layer = kwargs.get("layer", 3)
        self.parent = kwargs.get("parent")
        self.center = (self.getX() + self.getWidth() / 2, self.getY() + self.getHeight() / 2)
        self.name = kwargs.get("name")
        self.info_text = kwargs.get("info_text")

        self.on_hover = False
        self.on_hover_release = False

        # Function
        self.onClick = kwargs.get('onClick', lambda *args: None)
        self.onRelease = kwargs.get('onRelease', lambda *args: None)
        self.onClickParams = kwargs.get('onClickParams', ())
        self.onReleaseParams = kwargs.get('onReleaseParams', ())
        self.clicked = False
        self.moveable = kwargs.get("moveable", False)
        self.moving = False
        self.property = kwargs.get("property")

        # Text (Remove if using PyInstaller)
        self.textColour = kwargs.get('textColour', (0, 0, 0))
        self.fontSize = kwargs.get('fontSize', 20)
        self.string = kwargs.get('text', '')
        self.font = kwargs.get('font', pygame.font.SysFont('sans-serif', self.fontSize))
        self.text = self.font.render(self.string, True, self.textColour)
        self.textHAlign = kwargs.get('textHAlign', 'centre')
        self.textVAlign = kwargs.get('textVAlign', 'centre')
        self.margin = kwargs.get('margin', 20)
        self.textRect = self.text.get_rect()
        self.alignTextRect()

        # Image
        self.transparent = kwargs.get('transparent', False)
        self.image = kwargs.get('image', None)
        self.image_root = self.image
        self.imageHAlign = kwargs.get('imageHAlign', 'centre')
        self.imageVAlign = kwargs.get('imageVAlign', 'centre')

        if self.image:
            self.imageRect = self.image.get_rect()
            self.alignImageRect()

        # ToolTip
        self.tooltip = kwargs.get("tooltip", "")

        # info_panel
        self.infopanel = kwargs.get("infopanel", "")

    def alignImageRect(self):
        self.imageRect.center = (self._x + self._width // 2, self._y + self._height // 2)

        if self.imageHAlign == 'left':
            self.imageRect.left = self._x + self.margin - (self.radius_extension / 2)
        elif self.imageHAlign == 'right':
            self.imageRect.right = self._x + self._width - self.margin + (self.radius_extension / 2)

        if self.imageVAlign == 'top':
            self.imageRect.top = self._y + self.margin - (self.radius_extension / 2)
        elif self.imageVAlign == 'bottom':
            self.imageRect.bottom = self._y + self._height - self.margin + - (self.radius_extension / 2)

    def alignTextRect(self):
        self.textRect.center = (self._x + self._width // 2, self._y + self._height // 2)

        if self.textHAlign == 'left':
            self.textRect.left = self._x + self.margin
        elif self.textHAlign == 'right':
            self.textRect.right = self._x + self._width - self.margin

        if self.textVAlign == 'top':
            self.textRect.top = self._y + self.margin
        elif self.textVAlign == 'bottom':
            self.textRect.bottom = self._y + self._height - self.margin

        elif self.textVAlign == 'over_the_top':
            self.textRect.bottom = self._y - self.margin // 2
        elif self.textVAlign == 'below_the_bottom':
            self.textRect.bottom = self._y + self.margin // 2

    def on_hover_release_callback(self, x, y):
        if self.contains(x, y):
            self.on_hover = True
            self.on_hover_release = False
        else:
            self.on_hover_release = True

        if self.on_hover and self.on_hover_release:
            self.on_hover = False

            return True

        return False

    def reset_tooltip(self):
        if not self._hidden:
            x, y = Mouse.getMousePos()
            if self.on_hover_release_callback(x, y):
                # print ("reseting tooltip: " ,self, self.name)
                source.Globals.tooltip_text = ""

    def listen(self, events):
        """ Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        self.reset_tooltip()
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                # print("Button.listen")
                if mouseState == MouseState.RELEASE and self.clicked:
                    self.clicked = False
                    self.onRelease(*self.onReleaseParams)

                elif mouseState == MouseState.CLICK:
                    self.clicked = True
                    self.onClick(*self.onClickParams)

                    # this is used for build .... dirty hack, but leave it !
                    if self.string:
                        source.Globals.app.build(self.string)

                elif mouseState == MouseState.DRAG and self.clicked:
                    pass

                elif mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                    pass

                    # set tooltip
                    if self.tooltip:
                        if self.tooltip != "":
                            source.Globals.tooltip_text = self.tooltip

                    # set info_panel
                    if self.info_text:
                        if self.info_text != "":
                            source.Globals.app.info_panel.text = self.info_text
                            source.Globals.app.info_panel.set_planet_image(self.image, size=(85, 85), align="topright")
            else:
                self.clicked = False

    def execute(self, code):
        exec(code)

    def draw(self):
        """ Display to surface """
        self.update_position()
        if not self._hidden:
            if self.image:
                self.imageRect = self.image.get_rect()
                self.alignImageRect()
                self.win.blit(self.image, self.imageRect)

            self.textRect = self.text.get_rect()
            self.alignTextRect()
            self.win.blit(self.text, self.textRect)
        else:
            pass

    def set_center(self):
        #self.center = (self.getX() + self.getWidth() / 2, self.getY() + self.getHeight() / 2)
        self.center = self.imageRect.center

    def setImage(self, image):
        image = pygame.transform.scale(image, (self.getWidth(), self.getHeight()))
        self.image = image
        self.alignImageRect()
        self.win.blit(image, self.image.get_rect())

    def setOnClick(self, onClick, params=()):
        self.onClick = onClick
        self.onClickParams = params

    def setOnRelease(self, onRelease, params=()):
        self.onRelease = onRelease
        self.onReleaseParams = params

    def setInactiveColour(self, colour):
        self.inactiveColour = colour

    def setPressedColour(self, colour):
        self.pressedColour = colour

    def setHoverColour(self, colour):
        self.hoverColour = colour

    def get(self, attr):
        parent = super().get(attr)
        if parent is not None:
            return parent

        if attr == 'colour':
            return self.colour

    def set(self, attr, value):
        super().set(attr, value)

        if attr == 'colour':
            self.inactiveColour = value


class Button(WidgetBase, Moveable):
    """ A customisable button for Pygame

            :param win: Surface on which to draw
            :type win: pygame.Surface
            :param x: X-coordinate of top left
            :type x: int
            :param y: Y-coordinate of top left
            :type y: int
            :param width: Width of button
            :type width: int
            :param height: Height of button
            :type height: int
            :param kwargs: Optional parameters:

            to make button execute:
            overgive:  self.onClick = lambda: self.execute(kwargs)  to the class that inherits from Button,
            then implement: def execute(self, kwargs): in this class
            """

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):

        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        Moveable.__init__(self, x, y, width, height, kwargs)
        self.kwargs = kwargs
        self.parent = kwargs.get("parent")
        self.layer = kwargs.get("layer", 3)
        # self.ui_parent = kwargs.get("ui_parent", None)
        # if self.ui_parent:
        #     self.ui_parent_offset_x = self.ui_parent.getX() - x  # kwargs.get("ui_parent_offset_x", None)
        #     self.ui_parent_offset_y = self.ui_parent.getY() - y  # kwargs.get("ui_parent_offset_y", None)

        # self.selected = False
        self.center = (self.getX() + self.getWidth() / 2, self.getY() + self.getHeight() / 2)
        self.name = kwargs.get("name")
        self.info_text = kwargs.get("info_text")
        self.target = None
        self.on_hover = False
        self.on_hover_release = False

        # Colour
        self.inactiveColour = kwargs.get('inactiveColour', (150, 150, 150))
        self.hoverColour = kwargs.get('hoverColour', (125, 125, 125))
        self.pressedColour = kwargs.get('pressedColour', (100, 100, 100))
        self.colour = kwargs.get('colour', self.inactiveColour)  # Allows colour to override inactiveColour
        self.inactiveColour = self.colour
        self.shadowDistance = kwargs.get('shadowDistance', 0)
        self.shadowColour = kwargs.get('shadowColour', (210, 210, 180))
        self.hiddenColour = kwargs.get('hiddenColour', self.inactiveColour)

        # Function
        self.onClick = kwargs.get('onClick', lambda *args: None)
        self.onRelease = kwargs.get('onRelease', lambda *args: None)
        self.onClickParams = kwargs.get('onClickParams', ())
        self.onReleaseParams = kwargs.get('onReleaseParams', ())
        self.clicked = False
        self.moveable = kwargs.get("moveable", False)
        self.moving = False
        self.property = kwargs.get("property")

        # Text (Remove if using PyInstaller)
        self.textColour = kwargs.get('textColour', (0, 0, 0))
        self.fontSize = kwargs.get('fontSize', 20)
        self.string = kwargs.get('text', '')
        self.font = kwargs.get('font', pygame.font.SysFont('sans-serif', self.fontSize))
        self.text = self.font.render(self.string, True, self.textColour)
        self.textHAlign = kwargs.get('textHAlign', 'centre')
        self.textVAlign = kwargs.get('textVAlign', 'centre')
        self.margin = kwargs.get('margin', 20)
        self.textRect = self.text.get_rect()
        self.alignTextRect()

        # Image
        self.radius_extension = kwargs.get('radius_extension', 0)
        self.transparent = kwargs.get('transparent', False)

        # self.image_hover_surface = pygame.surface.Surface((self.width, self.height), 0, self.win)
        self.image_hover_surface = pygame.surface.Surface((
        width + self.radius_extension, height + self.radius_extension), 0, self.win)
        self.image_hover_surface.set_alpha(kwargs.get("image_hover_surface_alpha", 0))

        self.image = kwargs.get('image', None)
        self.imageHAlign = kwargs.get('imageHAlign', 'centre')
        self.imageVAlign = kwargs.get('imageVAlign', 'centre')

        if self.image:
            self.imageRect = self.image.get_rect()
            self.alignImageRect()

            # self.circle = pygame.draw.circle(surface=self.image_hover_surface, color=self.inactiveColour,
            #                                  center=(self.image.get_size()[0] / 2, self.image.get_size()[1] / 2),
            #                                  radius=(self.image.get_size()[0] / 2) + self.radius_extension)

        # Border
        self.borderThickness = kwargs.get('borderThickness', 0)
        self.inactiveBorderColour = kwargs.get('inactiveBorderColour', (0, 0, 0))
        self.hoverBorderColour = kwargs.get('hoverBorderColour', (80, 80, 80))
        self.pressedBorderColour = kwargs.get('pressedBorderColour', (100, 100, 100))
        self.borderColour = kwargs.get('borderColour', self.inactiveBorderColour)
        self.inactiveBorderColour = self.borderColour
        self.radius = kwargs.get('radius', 0)

        # ToolTip
        self.tooltip = kwargs.get("tooltip", "")

        # info_panel
        self.infopanel = kwargs.get("infopanel", "")

    def alignImageRect(self):
        self.imageRect.center = (self._x + self._width // 2, self._y + self._height // 2)

        if self.imageHAlign == 'left':
            self.imageRect.left = self._x + self.margin - (self.radius_extension / 2)
        elif self.imageHAlign == 'right':
            self.imageRect.right = self._x + self._width - self.margin + (self.radius_extension / 2)

        if self.imageVAlign == 'top':
            self.imageRect.top = self._y + self.margin - (self.radius_extension / 2)
        elif self.imageVAlign == 'bottom':
            self.imageRect.bottom = self._y + self._height - self.margin + - (self.radius_extension / 2)

    def alignTextRect(self):
        self.textRect.center = (self._x + self._width // 2, self._y + self._height // 2)

        if self.textHAlign == 'left':
            self.textRect.left = self._x + self.margin
        elif self.textHAlign == 'right':
            self.textRect.right = self._x + self._width - self.margin

        if self.textVAlign == 'top':
            self.textRect.top = self._y + self.margin
        elif self.textVAlign == 'bottom':
            self.textRect.bottom = self._y + self._height - self.margin
        elif self.textVAlign == 'over_the_top':
            self.textRect.bottom = self._y - self.margin // 2
        elif self.textVAlign == 'below_the_bottom':
            self.textRect.bottom = self._y + self.getHeight() + (self.margin // 2)

    def drawCircle_old(self, color, alpha):
        if self.transparent:
            # self.circle = pygame.draw.circle(surface=self.image_hover_surface, color=color,
            #                                  center=((self.image.get_size()[0] / 2) + (self.radius_extension/2), (self.image.get_size()[1] / 2) + - (self.radius_extension/2)),
            #                                  radius=(self.image.get_size()[0] / 2) + self.radius_extension)
            # self.image_hover_surface.set_alpha(alpha)

            self.circle = pygame.draw.circle(surface=self.win, color=color,
                center=((self.image.get_size()[0] / 2) + (self.radius_extension / 2),
                        (self.image.get_size()[1] / 2) + - (self.radius_extension / 2)),
                radius=(self.image.get_size()[0] / 2) + self.radius_extension)
            self.image_hover_surface.set_alpha(alpha)

    def drawCircle(self, color, alpha):
        if self.transparent:
            # self.circle = pygame.draw.circle(surface=self.image_hover_surface, color=color,
            #                                  center=((self.image.get_size()[0] / 2) + (self.radius_extension/2), (self.image.get_size()[1] / 2) + - (self.radius_extension/2)),
            #                                  radius=(self.image.get_size()[0] / 2) + self.radius_extension)
            # self.image_hover_surface.set_alpha(alpha)

            self.circle = pygame.surface.Surface((self.getWidth(), self.getHeight()), 0, self.win)
            self.circle.set_alpha(0)
            circle = pygame.draw.circle(surface=self.circle, color=color,
                center=self.imageRect.center,
                radius=(self.getWidth() * 1.5))

            self.win.blit(self.circle, self.imageRect)
            # self.image_hover_surface.set_alpha(alpha)

    def on_hover_release_callback(self, x, y):
        if self.contains(x, y):
            self.on_hover = True
            self.on_hover_release = False
        else:
            self.on_hover_release = True

        if self.on_hover and self.on_hover_release:
            self.on_hover = False

            return True

        return False

    def reset_tooltip(self):
        if not self._hidden:
            x, y = Mouse.getMousePos()
            if self.on_hover_release_callback(x, y):
                # print ("reseting tooltip: " ,self, self.name)
                source.Globals.tooltip_text = ""

    def listen(self, events):
        """ Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if self.moveable:
            self.move(events)
        self.reset_tooltip()
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                if mouseState == MouseState.RELEASE and self.clicked:
                    self.clicked = False
                    self.onRelease(*self.onReleaseParams)

                elif mouseState == MouseState.CLICK:
                    self.clicked = True
                    self.onClick(*self.onClickParams)
                    self.colour = self.pressedColour
                    self.borderColour = self.pressedBorderColour

                    self.drawCircle(self.pressedColour, 128)

                    # set planet on click of the building slot buttons
                    if self.parent:
                        if hasattr(self.parent,"property"):
                            if self.parent.property == "planet":
                                source.Globals.app.set_selected_planet(self.parent)
                                self.parent.set_info_text()
                    if self.string:
                        source.Globals.app.build(self.string)

                elif mouseState == MouseState.DRAG and self.clicked:
                    self.colour = self.pressedColour
                    self.borderColour = self.pressedBorderColour

                    self.drawCircle(self.pressedColour, 128)

                elif mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                    self.colour = self.hoverColour
                    self.borderColour = self.hoverBorderColour

                    self.drawCircle(self.hoverColour, 128)

                    # set tooltip
                    if self.tooltip:
                        if self.tooltip != "":
                            source.Globals.tooltip_text = self.tooltip

                    # set info_panel
                    if self.info_text:
                        if self.info_text != "":
                            source.Globals.app.info_panel.text = self.info_text
                            source.Globals.app.info_panel.set_planet_image(self.image, size=(85, 85), align="topright")
            else:
                self.clicked = False
                self.colour = self.inactiveColour
                self.borderColour = self.inactiveBorderColour

                self.drawCircle(self.inactiveColour, 0)

    def execute(self, code):
        exec(code)

    def draw(self):
        """ Display to surface """
        self.update_position()
        if not self._hidden:
            if not self.transparent:
                pygame.draw.rect(
                    self.win, self.shadowColour,
                    (self._x + self.shadowDistance, self._y + self.shadowDistance, self._width, self._height),
                    border_radius=self.radius
                    )

                pygame.draw.rect(
                    self.win, self.borderColour, (self._x, self._y, self._width, self._height),
                    border_radius=self.radius
                    )

                pygame.draw.rect(
                    self.win, self.colour, (self._x + self.borderThickness, self._y + self.borderThickness,
                                            self._width - self.borderThickness * 2,
                                            self._height - self.borderThickness * 2),
                    border_radius=self.radius
                    )
            else:
                if self.target:
                    self.trackTo(self.target)
                    #self.win.blit(self.image_hover_surface, self.imageRect)
                else:

                    self.imageRect = self.image.get_rect()
                    self.alignImageRect()
                    self.win.blit(self.image, self.imageRect)

            if self.image:
                if self.target:
                    self.trackTo(self.target)
                else:
                    self.imageRect = self.image.get_rect()
                    self.alignImageRect()
                    self.win.blit(self.image, self.imageRect)

            self.textRect = self.text.get_rect()
            self.alignTextRect()
            self.win.blit(self.text, self.textRect)
        else:
            pass
            """ pygame.draw.rect(
                    self.win, self.hiddenColour, (self._x, self._y, self._width, self._height),
                    border_radius=self.radius) """

    def set_center(self):
        self.center = (self.getX() + self.getWidth() / 2, self.getY() + self.getHeight() / 2)

    def setImage(self, image):
        surface = pygame.surface.Surface((self.getWidth(), self.getHeight()))
        surface_rect = surface.get_rect()
        surface_rect.x = self._x
        surface_rect.y = self._y
        surface.set_alpha(0)
        #self.win.blit(surface, surface.get_rect())

        self.image = image
        # self.image.set_alpha(0)
        self.win.blit(image, self.image.get_rect())
        # self.win.blit(self.parent.fog_of_war, self.parent.fog_of_war.get_rect())
        self.alignImageRect()

    def setOnClick(self, onClick, params=()):
        self.onClick = onClick
        self.onClickParams = params

    def setOnRelease(self, onRelease, params=()):
        self.onRelease = onRelease
        self.onReleaseParams = params

    def setInactiveColour(self, colour):
        self.inactiveColour = colour

    def setPressedColour(self, colour):
        self.pressedColour = colour

    def setHoverColour(self, colour):
        self.hoverColour = colour

    def get(self, attr):
        parent = super().get(attr)
        if parent is not None:
            return parent

        if attr == 'colour':
            return self.colour

    def set(self, attr, value):
        super().set(attr, value)

        if attr == 'colour':
            self.inactiveColour = value

    def move(self, events, child):
        if not self.moveable:   return
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if self.imageRect.collidepoint(event.pos):
                    self.moving = True

            elif event.type == MOUSEBUTTONUP:
                self.moving = False

            elif event.type == MOUSEMOTION and self.moving:
                self.moveX(event.rel[0])
                self.moveY(event.rel[1])
                self.update_position()
                self.set_center()


class ButtonArray(WidgetBase):
    def __init__(self, win, x, y, width, height, shape, **kwargs):
        """ A collection of buttons

        :param win: Surface on which to draw
        :type win: pygame.Surface
        :param x: X-coordinate of top left
        :type x: int
        :param y: Y-coordinate of top left
        :type y: int
        :param width: Width of button
        :type width: int
        :param height: Height of button
        :type height: int
        :param shape: The 2d shape of the array (columns, rows)
        :type shape: tuple of int
        :param kwargs: Optional parameters
        """
        super().__init__(win, x, y, width, height, **kwargs)
        self.layers = kwargs.get("layers")[0]
        self.layer = kwargs.get("layers")[0]
        self.shape = shape
        self.numButtons = shape[0] * shape[1]

        # Array
        self.colour = kwargs.get('colour', (210, 210, 180))
        self.border = kwargs.get('border', 10)
        self.topBorder = kwargs.get('topBorder', self.border)
        self.bottomBorder = kwargs.get('bottomBorder', self.border)
        self.leftBorder = kwargs.get('leftBorder', self.border)
        self.rightBorder = kwargs.get('rightBorder', self.border)
        self.borderRadius = kwargs.get('borderRadius', 0)
        self.separationThickness = kwargs.get('separationThickness', self.border)

        self.buttonAttributes = {
            # # Colour
            # 'inactiveColour': kwargs.get('inactiveColours', source.Globals.colors.ui_dark),
            # 'hoverColour': kwargs.get('hoverColours', source.Globals.colors.ui_white),
            # 'pressedColour': kwargs.get('pressedColours', source.Globals.colors.frame_color),
            # 'shadowDistance': kwargs.get('shadowDistances', None),
            # 'shadowColour': kwargs.get('shadowColours', source.Globals.colors.shadow_color),
            # "borderColour":kwargs.get('borderColours', source.Globals.colors.border_color),
            # "inactiveBorderColour":kwargs.get('inactiveBorderColours', source.Globals.colors.inactive_color),
            # "hiddenColour": kwargs.get('hiddenColours', None),

            # Colour
            'inactiveColour': kwargs.get('inactiveColours', None),
            'hoverColour': kwargs.get('hoverColours', None),
            'pressedColour': kwargs.get('pressedColours', None),
            'shadowDistance': kwargs.get('shadowDistances', None),
            'shadowColour': kwargs.get('shadowColours', None),
            "borderColour": kwargs.get('borderColours', None),
            "inactiveBorderColour": kwargs.get('inactiveBorderColours', None),
            "hiddenColour": kwargs.get('hiddenColours', None),

            # Function
            'onClick': kwargs.get('onClicks', None),
            'onRelease': kwargs.get('onReleases', None),
            'onClickParams': kwargs.get('onClickParams', None),
            'onReleaseParams': kwargs.get('onReleaseParams', None),
            "property": kwargs.get('propertys', None),
            'layer': kwargs.get('layers', 4),

            # Text
            'textColour': kwargs.get('textColours', None),
            'fontSize': kwargs.get('fontSizes', None),
            'text': kwargs.get('texts', None),
            'font': kwargs.get('fonts', None),
            'textHAlign': kwargs.get('textHAligns', None),
            'textVAlign': kwargs.get('textVAligns', None),
            'margin': kwargs.get('margins', None),
            'tooltip': kwargs.get('tooltips', None),
            'parent': kwargs.get('parents', None),
            "ui_parent": kwargs.get('ui_parents', None),
            "name": kwargs.get('names', None),
            "info_text": kwargs.get('info_texts', None),

            # Image
            'image': kwargs.get('images', None),
            'imageHAlign': kwargs.get('imageHAligns', None),
            'imageVAlign': kwargs.get('imageVAligns', None),
            'imageRotation': kwargs.get('imageRotations', None),
            'imageFill': kwargs.get('imageFills', None),
            'imageZoom': kwargs.get('imageZooms', None),
            'radius': kwargs.get('radii', None)
            }

        self.buttons = []
        self.createButtons()

    def createButtons(self):
        across, down = self.shape
        width = (self._width - self.separationThickness * (across - 1) - self.leftBorder - self.rightBorder) // across
        height = (self._height - self.separationThickness * (down - 1) - self.topBorder - self.bottomBorder) // down

        count = 0
        for i in range(across):
            for j in range(down):
                x = self._x + i * (width + self.separationThickness) + self.leftBorder
                y = self._y + j * (height + self.separationThickness) + self.topBorder
                kwargs = {k: v[count] for k, v in self.buttonAttributes.items() if v is not None}
                #print ("Button: kwargs:", kwargs)
                self.buttons.append(Button(self.win, x, y, width, height, isSubWidget=True,
                    **kwargs)
                    )


                count += 1


    def listen(self, events):
        pass

    def draw(self):
        """ Display to surface """
        if not self._hidden:
            rects = [
                (self._x + self.borderRadius, self._y, self._width - self.borderRadius * 2, self._height),
                (self._x, self._y + self.borderRadius, self._width, self._height - self.borderRadius * 2)
                ]

            circles = [
                (self._x + self.borderRadius, self._y + self.borderRadius),
                (self._x + self.borderRadius, self._y + self._height - self.borderRadius),
                (self._x + self._width - self.borderRadius, self._y + self.borderRadius),
                (self._x + self._width - self.borderRadius, self._y + self._height - self.borderRadius)
                ]

            for rect in rects:
                pass
                #pygame.draw.rect(self.win, self.colour, rect)
                # this draws the annoying background

            for circle in circles:
                pygame.draw.circle(self.win, self.colour, circle, self.borderRadius)

            for button in self.buttons:
                button.draw()

    def getButtons(self):
        return self.buttons


if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode((600, 600))

    button = Button(win, 100, 100, 300, 150, text='Hello', fontSize=50, margin=20,
        inactiveColour=(255, 0, 0), pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: print('Click'), font=pygame.font.SysFont('calibri', 10),
        textVAlign='bottom', imageHAlign='centre', imageVAlign='centre', borderThickness=3,
        onRelease=lambda: print('Release'), shadowDistance=5, borderColour=(0, 0, 0))

    buttonArray = ButtonArray(win, 50, 50, 500, 500, (2, 2), border=100, texts=('1', '2', '3', '4'),
        onClicks=(lambda: print(1), lambda: print(2), lambda: print(3), lambda: print(4)))
    button.hide()
    buttonArray.hide()

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        win.fill((255, 255, 255))

        update(events)
        pygame.display.update()
