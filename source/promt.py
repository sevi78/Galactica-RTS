def calculate_new_position__(self):
    # set target and calc new position
    self.set_center()
    target = self.target
    if hasattr(target, "x"):
        x1 = target.imageRect.center[0]
        y1 = target.imageRect.center[1]

    elif hasattr(target, "crew"):
        x1 = target.imageRect.center[0]
        y1 = target.imageRect.center[1]
    else:
        x1 = self.target[0]
        y1 = self.target[1]
    x = self.getX()
    y = self.getY()
    dist_x = (x1 - x)
    dist_y = (y1 - y)
    distance = math.dist((x, y), (x1, y1))
    return dist_x, dist_y, distance, target, x, y


def world_2_screen(self, world_x, world_y):
    screen_x = (world_x - self.world_offset_x) * self.zoom
    screen_y = (world_y - self.world_offset_y) * self.zoom
    return [screen_x, screen_y]


def screen_2_world(self, screen_x, screen_y):
    world_x = (screen_x / self.zoom) + self.world_offset_x
    world_y = (screen_y / self.zoom) + self.world_offset_y
    return [world_x, world_y]


def pan_and_zoom(self):
    for zoomable_object in self.parent.ships:
        x, y = self.world_2_screen(zoomable_object.x, zoomable_object.y)
        zoomable_object.setX(x - zoomable_object.getWidth() / 2)
        zoomable_object.setY(y - zoomable_object.getHeight() / 2)
        zoomable_object.setWidth(zoomable_object.size_x * self.zoom)
        zoomable_object.setHeight(zoomable_object.size_y * self.zoom)
        zoomable_object.image_rot = pygame.transform.scale(zoomable_object.image_raw, (
            zoomable_object.getWidth() * self.zoom, zoomable_object.getHeight() * self.zoom))
