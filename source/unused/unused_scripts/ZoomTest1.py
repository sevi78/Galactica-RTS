import pygame
import sys
import pygame_widgets
from Button import ImageButton

pygame.init()
WIDTH = 1000
HEIGHT = 1000
pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
win = pygame.display.get_surface()

# create test array
buttons = []
spacing = 100
for x in range(10):
    for y in range(10):
        b = ImageButton(win,x*spacing,y*spacing,30,30, isSubWidget=False,image=pygame.image.load("C:\\Users\\sever\\Documents\\Galactica2.8\\pictures\\planets\\zork_50x50.png"), onClick=lambda :print ("OK"))
        buttons.append(b)

class Zoom___:
    def __init__(self,width, height, zoomobjects):
        self.width = WIDTH
        self.height = HEIGHT
        self.zoomfactor = 1.0
        self.zoom_factor_scale = 0.01
        self.zoom_direction = 1
        self.zoomobjects = zoomobjects

    def update(self,events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.zoomfactor = 1.0
                    self.zoomfactor += self.zoom_factor_scale

                elif event.button == 5:
                    self.zoomfactor = 1.0
                    self.zoomfactor -= self.zoom_factor_scale

                if event.button == 4 or 5:
                    for i in buttons:
                        self.set_postition_and_scale(i)
                if event.button == 1:
                    self.zoomfactor = 1.0

    def set_postition__(self, obj):
        mp = pygame.mouse.get_pos()
        mx = mp[0]-self.width/2
        my = mp[1]-self.height/2

        x,y = obj.getX(), obj.getY()
        relx,rely = 1/self.width-mx*x, 1/self.height-my*y

        new_width = self.width*self.zoomfactor
        new_height = self.height*self.zoomfactor

        newx = mx-relx*new_width
        newy = my-rely*new_height

        obj.setX(newx)
        obj.setY(newy)

    def set_postition__(self, obj):
        mp = pygame.mouse.get_pos()
        mx = mp[0]-self.width/2
        my = mp[1]-self.height/2

        x,y = obj.getX(), obj.getY()
        relx,rely = 1/self.width-mx*x, 1/self.height-my*y

        new_width = self.width*self.zoomfactor
        new_height = self.height*self.zoomfactor

        newx = mx-relx*new_width
        newy = my-rely*new_height

        obj.setX(newx)
        obj.setY(newy)

    def set_postition_and_scale(self, obj):
        # get mouse position
        mp = pygame.mouse.get_pos()

        # set x,y from mp minus half the screen to ensure the mouse position is the center of the screen
        mx = mp[0] - (self.width / 2)
        my = mp[1] - (self.height / 2)
        mxr = mp[0]/self.width
        myr = mp[1]/self.height

        # convert mouse position to relative position
        relmx = 1/self.width * mx
        relmy = 1/self.height * my

        # get the objects absolute position
        x, y = obj.getX()  , obj.getY()

        # convert to relative position
        relx, rely = 1 / (self.width) * x, 1 / (self.height) * y

        # calculate new_width/height based on the zoom factor
        new_width = self.width * self.zoomfactor
        new_height = self.height * self.zoomfactor

        newx = (x-mx) * self.zoomfactor
        newy = (y-my) * self.zoomfactor
        # # calculate new x,y positions
        # newx = ((relx-) * new_width)
        # newy = ((rely) * new_height)
        #
        # # set the position to the object
        obj.setX((newx-mx))
        obj.setY((newy-my))

        # set objects scaling
    def set_postition_and_scale____(self, obj):
        # get mouse position
        mp = pygame.mouse.get_pos()

        # set x,y from mp minus half the screen to ensure the mouse position is the center of the screen
        mx = mp[0] - self.width / 2
        my = mp[1] - self.height / 2
        mxr = mp[0]
        myr = mp[1]
        # convert mouse position to relative position
        relmx = 1/self.width * mx
        relmy = 1/self.height * my

        # get the objects absolute position
        x, y = obj.getX()  , obj.getY()

        # convert to relative position
        relx, rely = 1 / (self.width) * x, 1 / (self.height) * y

        # calculate new_width/height based on the zoom factor
        new_width = self.width * self.zoomfactor
        new_height = self.height * self.zoomfactor

        newx = (x-mx) * self.zoomfactor
        newy = (y-my) * self.zoomfactor
        # # calculate new x,y positions
        # newx = ((relx-) * new_width)
        # newy = ((rely) * new_height)
        #
        # # set the position to the object
        obj.setX((newx-mx))
        obj.setY((newy-my))

        # set objects scaling
    def set_postition_and_scale__(self, obj):
        # get mouse position
        mp = pygame.mouse.get_pos()

        # set x,y from mp minus half the screen to ensure the mouse position is the center of the screen
        mx = mp[0] - self.width / 2
        my = mp[1] - self.height / 2

        # convert mouse position to relative position
        relmx = 1/self.width * mx
        relmy = 1/self.height * my

        # get the objects absolute position
        x, y = obj.getX()  , obj.getY()

        # convert to relative position
        #relx, rely = 1 / (self.width) * (x-mx), 1 / (self.height) * (y-my)
        relx, rely = 1 / (self.width) * x, 1 / (self.height) * y

        # include mouse position =

        # calculate new_width/height based on the zoom factor
        new_width = self.width * self.zoomfactor
        new_height = self.height * self.zoomfactor

        # calculate new x,y positions
        newx = ((relx) * new_width)
        newy = ((rely) * new_height)
        # newx =  ((relx-relmx) * new_width)
        # newy =  ((rely-relmy) * new_height)

        # this works like dragging :)
        # newx =  ((relx-relmx) * new_width/self.zoomfactor)
        # newy =  ((rely-relmy) * new_height/self.zoomfactor)


        # set the position to the object
        obj.setX((newx-mx))
        obj.setY((newy-my))

        # set objects scaling
        # width, height  = obj.getWidth(), obj.getHeight()
        # rel_width, rel_height = 1/self.width*width,1/self.height*height
        # new_obj_width = rel_width*self.zoomfactor
        # new_obj_height = rel_height*self.zoomfactor
        # obj.setWidth(new_obj_width)
        # obj.setHeight(new_obj_height)
        # obj.image = pygame.transform.scale(obj.image, (obj.getWidth(), obj.getHeight()))
class Zoom:
    def __init__(self,width, height, zoomobjects):
        self.width = WIDTH
        self.height = HEIGHT
        self.zoomfactor = 1.0
        self.zoom_factor_scale = 0.1
        self.zoom_direction = 1
        self.zoomobjects = zoomobjects
        self.zerox = 0
        self.zeroy = 0

    def update(self,events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.zoomfactor = 1.0
                    self.zoomfactor += self.zoom_factor_scale

                elif event.button == 5:
                    self.zoomfactor = 1.0
                    self.zoomfactor -= self.zoom_factor_scale

                if event.button == 4 or 5:
                    if not event.button == 1:
                        print ("n")
                        for i in buttons:
                            self.set_position(i)
                if event.button == 1:
                    return
                    self.zoomfactor = 1.0

    def zoom_drag(self,mouse_pos, obj_x, obj_y, width, height):
        # Get the mouse wheel delta
        zoom = pygame.mouse.get_rel()[1]

        # Calculate the new width and height based on the zoom factor
        zoom_factor = 1 + zoom * 0.1
        new_width = int(width * zoom_factor)
        new_height = int(height * zoom_factor)

        # Calculate the new x and y positions based on the mouse position
        mouse_x, mouse_y = mouse_pos
        new_x = obj_x - (new_width - width) * (mouse_x / width)
        new_y = obj_y - (new_height - height) * (mouse_y / height)

        # Return the new x, y, width, and height values
        return new_x, new_y, new_width, new_height

    def set_position__(self, obj):
        # Get the mouse wheel delta
        zoom = pygame.mouse.get_rel()[1]

        # Calculate the new width and height based on the zoom factor
        zoom_factor = self.zoomfactor + zoom * 0.1
        new_width = int(obj.getWidth() * zoom_factor)
        new_height = int(obj.getHeight() * zoom_factor)

        # Calculate the new x and y positions based on the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        new_x = mouse_x - new_width / 2
        new_y = mouse_y - new_height / 2

        # Set the new x, y, width, and height values for the object
        obj.setX(new_x)
        obj.setY(new_y)
        obj.setWidth(new_width)
        obj.setHeight(new_height)
    def set_position_(self, obj):
        # Get the mouse position
        mp = pygame.mouse.get_pos()

        # Calculate the new x, y, width, and height values using the zoom_drag function
        new_x, new_y, new_width, new_height = self.zoom_drag(mp, obj.getX(), obj.getY(), obj.getWidth(), obj.getHeight())

        # Set the new x, y, width, and height values for the object
        obj.setX(new_x)
        obj.setY(new_y)
        obj.setWidth(new_width)
        obj.setHeight(new_height)

        # Set the object's scaling
        self.zerox = new_width / 2
        self.zeroy = new_height / 2

    def set_position_last(self, obj):
        w = self.width
        h = self.height
        x = obj.getX()
        y = obj.getY()

        w1 = w*self.zoomfactor
        h1 = w*self.zoomfactor

        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]


        rx = 1 / w * x
        rx1 = (rx * w1) - (mx - w1) / 2 * self.zoomfactor

        ry = 1 / h * y
        ry1 = (ry * h1) - (my - h1) / 2 * self.zoomfactor

        obj.setX(rx1)
        obj.setY(ry1)

    def set_position_perpl1(self, obj):
        w = self.width
        h = self.height
        x = obj.getX()
        y = obj.getY()
        w1 = w * self.zoomfactor
        h1 = h * self.zoomfactor
        mx, my = pygame.mouse.get_pos()
        rx = x / w
        rx1 = (rx * w1) - (mx - w1 / 2) * self.zoomfactor
        ry = y / h
        ry1 = (ry * h1) - (my - h1 / 2) * self.zoomfactor
        obj.setX(rx1)
        obj.setY(ry1)

    def zoom(self,surface, zoom_factor, player_rect):
        # Calculate the new width and height of the surface after zooming
        w = surface.get_width()
        h = surface.get_height()
        w1 = w * zoom_factor
        h1 = h * zoom_factor

        # Calculate the new x and y coordinates of the object based on the new width and height of the surface
        x = player_rect.x
        y = player_rect.y
        mx, my = pygame.mouse.get_pos()
        rx = x / w
        ry = y / h
        rx1 = (rx * w1) - (mx - w / 2) * zoom_factor
        ry1 = (ry * h1) - (my - h / 2) * zoom_factor

        # Adjust the calculation of the new x and y coordinates of the object to zoom towards the center of the screen
        player_rect.x = rx1
        player_rect.y = ry1

        # Scale the surface to the desired size
        zoomed_surface = pygame.transform.scale(surface, (int(w1), int(h1)))

        # Draw the zoomed surface onto the screen
        self.win.blit(zoomed_surface, (0, 0))

        return player_rect
    def set_position(self, obj):
        w = self.width
        h = self.height
        x = obj.getX()
        y = obj.getY()
        # new width, height
        w1 = w * self.zoomfactor
        h1 = h * self.zoomfactor
        # mouse position
        mx, my = pygame.mouse.get_pos()
        rx = x / w# relative mouse position
        ry = y / h
        # new x,y
        rx1 = (rx * w1) - (mx - w / 2) * self.zoomfactor
        ry1 = (ry * h1) - (my - h / 2) * self.zoomfactor
        obj.setX(rx1)
        obj.setY(ry1)
        # obj.setWidth(obj.getWidth()  * self.zoomfactor)
        # obj.setHeight(obj.getHeight() * self.zoomfactor)
        image = pygame.transform.scale(obj.image,(obj.getWidth() * self.zoomfactor, obj.getHeight() * self.zoomfactor))
        obj.setImage(image = image)

    def set_position_gpt(self, obj):
        w = self.width
        h = self.height
        x = obj.getX()
        y = obj.getY()
        w1 = w * self.zoomfactor
        h1 = h * self.zoomfactor
        mx, my = pygame.mouse.get_pos()
        rx = x / w
        rx1 = (rx * w1) - (mx - w1 / 2) * self.zoomfactor
        ry = y / h
        ry1 = (ry * h1) - (my - h1 / 2) * self.zoomfactor
        obj.setX(rx1)
        obj.setY(ry1)

        # w = self.width
        # h = self.height
        # x = obj.getX()
        # y = obj.getY()
        # w1 = w * self.zoomfactor
        # h1 = h * self.zoomfactor
        # mx, my = pygame.mouse.get_pos()
        # rx = x / w
        # ry = y / h
        # rx1 = (rx * w1) - (mx - (w1 / 2)) * self.zoomfactor
        # ry1 = (ry * h1) - (my - (h1 / 2) )* self.zoomfactor
        # obj.setX(rx1)
        # obj.setY(ry1)
    def set_position_(self, obj):
        # get mouse position
        zero = (0,0)

        mp = pygame.mouse.get_pos()
        mx = mp[0]
        my = mp[1]

        # screen center
        cx =  self.width/2
        cy =  self.height/2

        ncx = cx-mx
        ncy = cy-my
        # get the objects absolute position
        x, y = obj.getX()  , obj.getY()
        pos = (x,y)


        newx = x+ncx
        newy = y+ncy

        obj.setX((newx-mx))
        obj.setY((newy-my))
        self.zerox = ncx
        self.zeroy = ncy

        # set objects scaling

zoom = Zoom(WIDTH, HEIGHT, buttons)
def quit_game(events):
    # quit the game with quit icon or esc
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

run = True
while run:
    # get events, only do this once!! and exactly here. otherwise performance is very bad
    events = pygame.event.get()

    # call functions, don't mess up the order :)

    win.fill((123,23,32))

    pygame_widgets.update(events)
    zoom.update(events)
    quit_game(events)
    pygame.display.update()