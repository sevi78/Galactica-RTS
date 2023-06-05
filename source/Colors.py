import pygame


class Colors:
    def __init__(self):
        # set the colors
        self.hover_color = pygame.color.THECOLORS["blue"]
        self.pressed_color = pygame.color.THECOLORS["cyan"]
        self.inactive_color = pygame.color.THECOLORS["red"]
        self.shadow_color = pygame.color.THECOLORS["orange"]
        self.text_color = pygame.color.THECOLORS["white"]
        self.border_color = pygame.color.THECOLORS["purple"]
        self.hoverBorderColour = pygame.color.THECOLORS["brown"]
        self.pressedBorderColour = pygame.color.THECOLORS["grey"]
        self.frame_color = (
        120, 204, 226)  # "#78cce2" #"#4E7988"  #("#38BFC6")# pygame.colordict.THECOLORS["darkslategray1"]"#d3f8ff"
        self.background_color = pygame.colordict.THECOLORS["black"]
        self.ui_white = (238, 253, 254)  # "#eefdfe"
        self.ui_dark = (55, 130, 157)  # "#37829d"

# class Colors:
#     def __init__(self):
#         # set the colors
#         self.hover_color = pygame.color.THECOLORS["blue"]
#         self.pressed_color = pygame.color.THECOLORS["cyan"]
#         self.inactive_color = pygame.color.THECOLORS["red"]
#         self.shadow_color = pygame.color.THECOLORS["orange"]
#         self.text_color = pygame.color.THECOLORS["white"]
#         self.border_color = pygame.color.THECOLORS["purple"]
#         self.hoverBorderColour = pygame.color.THECOLORS["brown"]
#         self.pressedBorderColour = pygame.color.THECOLORS["grey"]
#         self.frame_color = pygame.colordict.THECOLORS["darkslategray1"]
#         self.background_color = pygame.colordict.THECOLORS["black"]
#         self.ui_white = pygame.color.THECOLORS["cyan"]
#         self.ui_dark = pygame.color.THECOLORS["purple"]
