class Navigation:
    def __init__(self, parent):
        self.parent = parent
        self.x = 0
        self.y = 0
        self.limit_x = source.Globals.scene_width - pygame.display.get_surface().get_width()
        self.limit_y = source.Globals.scene_height -pygame.display.get_surface().get_height()
        self.position_x = 0
        self.position_y = 0
        self.value = 0.0
        self.acceleration = 15.0
        self.acceleration_max = 5.0
        self.acceleration_min = 1.0
        self.moveables = WidgetHandler.layers[0] + WidgetHandler.layers[1] + WidgetHandler.layers[2] + WidgetHandler.layers[3]
        self.moving = False
        self.stopp = False
        self.key_pressed = False
        self.mouse_pressed = False
    def accelerate(self):
        if self.value + self.acceleration < self.acceleration_max:
            self.value += self.acceleration
        else:
            self.value = self.acceleration_max
    def slowdown(self):
        if self.value - self.acceleration > self.acceleration_min:
            self.value -= self.acceleration
        else:
            self.value = self.acceleration_min
    def calculate_distance_to_center(self):
        mp = pygame.mouse.get_pos()
        mp_x = mp[0]
        mp_y = mp[1]
        win = pygame.display.get_surface()
        win_width = win.get_width()
        win_height = win.get_height()
        center_x = win_width / 2
        center_y = win_height / 2
        dist_x = center_x - mp_x
        dist_y = center_y - mp_y
        return dist_x, dist_y

    def drag(self, events):
        if not source.Globals.navigation:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == 1073742048:# ctrl:
                    self.key_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == 1073742048:
                    self.key_pressed = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False
        if self.key_pressed == True and self.mouse_pressed == True:
            dist_x, dist_y = self.calculate_distance_to_center()
            self.x = dist_x / self.acceleration
            self.y = dist_y / self.acceleration
            self.move_objects()
        self.debug_position()
    def limit_position(self):
        zero_x = self.limit_x * -1
        zero_y = self.limit_y * -1
        self.stopp = False
        if self.position_x < zero_x:
            self.position_x = zero_x +10
            self.stopp = True
        elif self.position_x > float(self.limit_x):
            self.position_x = self.limit_x-10
            self.stopp = True
        elif self.position_y < zero_y:
            self.position_y = zero_y +10
            self.stopp = True
        elif self.position_y > float(self.limit_y):
            self.position_y = self.limit_y-10
            self.stopp = True
        else:
            self.stopp = False
        return self.stopp
    def move_objects(self):
        if not self.limit_position():
            self.position_x -= self.x
            self.position_y -= self.y
        else:
            source.Globals.app.event_text = "you have reached the end of the universe!!"
        if not self.stopp:
            for i in self.moveables:
                i._x -= self.x * -1
                i._y -= self.y * -1
                if hasattr(i, "set_center"):
                    if callable(i.set_center):
                        i.set_center()
                limit_positions(i)
        pygame.draw.line (source.Globals.app.background_image.surface, source.Globals.colors.frame_color, pygame.mouse.get_pos(), (self.position_x, self.position_y))
        source.Globals.win.blit (source.Globals.app.background_image.surface, (0,0))
    def navigate_to(self, obj):
        ship = [i for i in source.Globals.app.ships if i.name == obj][0]
        print("navigate_to: ", ship)
        self.position_x = ship.getX()
        self.position_y = ship.getY()
        for i in self.moveables:
            i._x -= self.x * -1
            i._y -= self.y * -1
            if hasattr(i, "set_center"):
                if callable(i.set_center):
                    i.set_center()
            limit_positions(i)