import pygame
import pygame_widgets
from Planet import Planet, PlanetButtons
import source.Globals
from Globals import pictures_path
from Button import ImageButton
window = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
map = pygame.image.load("C:\\Users\\sever\\Documents\\Galactica2.8\\pictures\\textures\\bg.png")
maprect = map.get_rect(center=window.get_rect().center)
mapsurface = map

p = ImageButton(window,200,200,30,30, isSubWidget=False,image=pygame.image.load("C:\\Users\\sever\\Documents\\Galactica2.8\\pictures\\planets\\zork_50x50.png"), onClick=lambda :print ("OK"))
p1  = ImageButton(window,200,200,30,30, isSubWidget=False,image=pygame.image.load("C:\\Users\\sever\\Documents\\Galactica2.8\\pictures\\planets\\Helios 12_150x150.png"), onClick=lambda :print ("OK"))

objects = []
objects.append(p)
objects.append(p1)
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.VIDEORESIZE:
            window = pygame.display.set_mode(event.dict['size'], pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
            mapsurface = pygame.transform.smoothscale(map, maprect.size)

            mx, my = b.getX(), b.getY()
            left = mx + (maprect.left - mx)
            right = mx + (maprect.right - mx)
            top = my + (maprect.top - my)
            bottom = my + (maprect.bottom - my)

            b.setX(left)
            b.setY(top)
            b.setWidth(maprect.size[0])
            b.setHeight(maprect.size[1])

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 or event.button == 5:
                zoom = 2  if event.button == 4 else 0.5
                mx, my = event.pos
                left = mx + (maprect.left - mx) * zoom
                right = mx + (maprect.right - mx) * zoom
                top = my + (maprect.top - my) * zoom
                bottom = my + (maprect.bottom - my) * zoom
                maprect = pygame.Rect(left, top, right - left, bottom - top)
                mapsurface = pygame.transform.smoothscale(map, maprect.size)

                for b in objects:
                    bx = b.getX()
                    by = b.getY()
                    mx, my = event.pos
                    left =  mx + (maprect.left - mx) * zoom + (bx/zoom)
                    right =  mx + (maprect.right - mx) * zoom + (bx/zoom)
                    top =  my + (maprect.top - my) * zoom +(by/zoom)
                    bottom = my + (maprect.bottom - my) * zoom + (by/zoom)

                    b.setX(left)
                    b.setY(top)
                    b.setWidth(right - left)
                    b.setHeight(right - left)


    window.fill(0)
    window.blit(mapsurface, maprect)
    pygame_widgets.update(event)
    pygame.display.flip()


pygame.quit()
exit()



#version 2
# import pygame
#
# window = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
# map = pygame.image.load("C:\\Users\\sever\\Documents\\Galactica2.8\\pictures\\textures\\bg.png")
# maprect = map.get_rect(center=window.get_rect().center)
# mapsurface = map
#
# run = True
#
# def calculate_zoom(event,maprect):
#     zoom = 2 if event.button == 4 else 0.5
#     mx, my = event.pos
#     left = mx + (maprect.left - mx) * zoom
#     right = mx + (maprect.right - mx) * zoom
#     top = my + (maprect.top - my) * zoom
#     bottom = my + (maprect.bottom - my) * zoom
#     maprect = pygame.Rect(left, top, right - left, bottom - top)
#     mapsurface = pygame.transform.smoothscale(map, maprect.size)
#
#
#     return maprect, mapsurface
#
# def on_window_resize(event, maprect):
#     window = pygame.display.set_mode(event.dict['size'], pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
#     mapsurface = pygame.transform.smoothscale(map, maprect.size)
#     return mapsurface, window
#
# def draw_zoom(mapsurface, maprect):
#     window.blit(mapsurface, maprect)
# while run:
#     window.fill(0)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#
#         elif event.type == pygame.VIDEORESIZE:
#             mapsurface, window = on_window_resize(event, maprect)
#
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             if event.button == 4 or event.button == 5:
#                 maprect, mapsurface = calculate_zoom(event, maprect)
#
#
#
#     draw_zoom(mapsurface, maprect)
#     pygame.display.flip()
#
# pygame.quit()
# exit()

# import pygame
#
# window = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
# map = pygame.image.load("C:\\Users\\sever\\Documents\\Galactica2.8\\pictures\\textures\\bg.png")
# maprect = map.get_rect(center=window.get_rect().center)
# mapsurface = map
#
#
# class ZoomHandler:
#     def __init__(self, map, maprect, mapsurface, window):
#         self.window = window
#         self.map = map
#         self.maprect = maprect
#         self.mapsurface = mapsurface
#         self.zoom = None
#         self.my = None
#         self.mx = None
#         self.left = None
#         self.right = None
#         self.top = None
#         self.bottom = None
#         self.window = window
#
#         self.window.blit(self.mapsurface, self.maprect)
#
#     def calculate_zoom(self, event):
#         self.zoom = 2 if event.button == 4 else 0.5
#         self.mx, self.my = event.pos
#         self.left = self.mx + (maprect.left - self.mx) * self.zoom
#         self.right = self.mx + (maprect.right - self.mx) * self.zoom
#         self.top = self.my + (maprect.top - self.my) * self.zoom
#         self.bottom = self.my + (maprect.bottom - self.my) * self.zoom
#         self.maprect = pygame.Rect(self.left, self.top, self.right - self.left, self.bottom - self.top)
#         self.mapsurface = pygame.transform.smoothscale(self.map, self.maprect.size)
#         self.window.blit(self.mapsurface, self.maprect)
#
#
#
#     def on_window_resize(self, event):
#         self.window = pygame.display.set_mode(event.dict['size'], pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
#         self.mapsurface = pygame.transform.smoothscale(map, maprect.size)
#
#
#     def draw_zoom(self):
#
#         self.window.blit(self.mapsurface, self.maprect)
#
#     def udpate(self, event):
#
#
#         if event.type == pygame.VIDEORESIZE:
#             self.on_window_resize(event)
#             self.calculate_zoom(event)
#
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             if event.button == 4 or event.button == 5:
#                 self.calculate_zoom(event)
#
#
#
#
# zoomhandler = ZoomHandler(map, maprect, mapsurface, window)
#
# run = True
# while run:
#     window.fill(0)
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#
#         zoomhandler.udpate(event)
#
#     zoomhandler.draw_zoom()
#     pygame.display.flip()
#
# pygame.quit()
# exit()