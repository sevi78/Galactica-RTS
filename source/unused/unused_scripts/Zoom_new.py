import pygame
import sys

# Window size
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 1300
WINDOW_SURFACE = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE
image_filename = None

PAN_BOX_WIDTH = 640
PAN_BOX_HEIGHT = 640
PAN_STEP = 5


def errorExit(message, code=1):
    """ Write an error message to the console, then exit with an error code """
    sys.stderr.write(message + "\n")
    sys.exit(code)


# The first argument is either the image filename
# or a "--help" request for help

# Did we get any arguments?


### PyGame initialisation
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW_SURFACE)
pygame.display.set_caption("Image Pan")

### Can we load the user's image OK?
try:
    base_image = pygame.image.load("C:\\Users\\sever\\Documents\\Galactica2.8\\pictures\\planets\\zork_150x150.png")
except:
    errorExit("Failed to open [%s]" % (image_filename))

### Pan-position
background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))  # zoomed section is copied here
zoom_image = None
pan_box = pygame.Rect(0, 0, PAN_BOX_WIDTH, PAN_BOX_HEIGHT)  # curent pan "cursor position"
last_box = pygame.Rect(0, 0, 1, 1)

### Main Loop
clock = pygame.time.Clock()
done = False
while not done:

    # Handle user-input
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            done = True

    # Movement keys
    # Pan-box moves up/down/left/right, Zooms with + and -
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP]):
        pan_box.y -= PAN_STEP
    if (keys[pygame.K_DOWN]):
        pan_box.y += PAN_STEP
    if (keys[pygame.K_LEFT]):
        pan_box.x -= PAN_STEP
    if (keys[pygame.K_RIGHT]):
        pan_box.x += PAN_STEP
    if (keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]):
        pan_box.width += PAN_STEP
        pan_box.height += PAN_STEP
        if (pan_box.width > WINDOW_WIDTH):  # Ensure size is sane
            pan_box.width = WINDOW_WIDTH
        if (pan_box.height > WINDOW_HEIGHT):
            pan_box.height = WINDOW_HEIGHT
    if (keys[pygame.K_MINUS]):
        pan_box.width -= PAN_STEP
        pan_box.height -= PAN_STEP
        if (pan_box.width < PAN_STEP):  # Ensure size is sane
            pan_box.width = PAN_STEP
        if (pan_box.height < PAN_STEP):
            pan_box.height = PAN_STEP

    # Ensure the pan-box stays within image
    PAN_BOX_WIDTH = min(PAN_BOX_WIDTH, base_image.get_width())
    PAN_BOX_HEIGHT = min(PAN_BOX_HEIGHT, base_image.get_height())
    if (pan_box.x < 0):
        pan_box.x = 0
    elif (pan_box.x + pan_box.width >= base_image.get_width()):
        pan_box.x = base_image.get_width() - pan_box.width - 1
    if (pan_box.y < 0):
        pan_box.y = 0
    elif (pan_box.y + pan_box.height >= base_image.get_height()):
        pan_box.y = base_image.get_height() - pan_box.height - 1

    # Re-do the zoom, but only if the pan box has changed since last time
    if (pan_box != last_box):
        # Create a new sub-image but only if the size changed
        # otherwise we can just re-use it
        if (pan_box.width != last_box.width or pan_box.height != last_box.height):
            zoom_image = pygame.Surface((pan_box.width, pan_box.height))

        zoom_image.blit(base_image, (0, 0), pan_box)  # copy base image
        window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        pygame.transform.scale(zoom_image, window_size, background)  # scale into thebackground
        last_box = pan_box.copy()  # copy current position

    window.blit(background, (0, 0))
    pygame.display.flip()

    # Clamp FPS
    clock.tick_busy_loop(60)

pygame.quit()