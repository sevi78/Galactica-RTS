import math
import random

from pygame.math import Vector2
from pygame_widgets.mouse import Mouse, MouseState

import source.Globals
from source.AppHelper import debug_positions, check_function_execution
from source.Globals import *
import source.WidgetHandler
from source.Button import Moveable, ImageButton
from source.Images import pictures_path
from source.ProgressBar import ProgressBar
from source.Sounds import sounds
from source.WidgetHandler import WidgetBase


class ShipRanking:
    """
    all functions and variables needed to ranke the ship
    params: experience
            rank
            ranks
            rank_images

    functions:
            set_experience
            set_rank
            draw_rank_image

    possible ranks:
            {0: "Cadet", 1: "Ensign", 2: "Lieutenant", 3: "Commander", 4: "Commodore", 5: "Captain", 6: "Vice Admiral", 7: "Admiral", 8: "Fleet Admiral"}

    """

    def __init__(self):

        # ranking
        self.experience = 0
        self.experience_factor = 3000
        self.rank = "Cadet"
        self.ranks = {0: "Cadet", 1: "Ensign", 2: "Lieutenant", 3: "Commander", 4: "Commodore", 5: "Captain", 6: "Vice Admiral", 7: "Admiral", 8: "Fleet Admiral"}

        # rank image
        self.rank_images = {
            "Cadet": source.Globals.images[pictures_path]["icons"]["badge1_30x30.png"],
            "Ensign": source.Globals.images[pictures_path]["icons"]["badge2_30x30.png"],
            "Lieutenant": source.Globals.images[pictures_path]["icons"]["badge3_30x30.png"],
            "Commander": source.Globals.images[pictures_path]["icons"]["badge4_48x30.png"],
            "Commodore": source.Globals.images[pictures_path]["icons"]["badge5_48x30.png"],
            "Captain": source.Globals.images[pictures_path]["icons"]["badge6_48x30.png"],
            "Vice Admiral": source.Globals.images[pictures_path]["icons"]["badge7_43x30.png"],
            "Admiral": source.Globals.images[pictures_path]["icons"]["badge8_43x30.png"],
            "Fleet Admiral": source.Globals.images[pictures_path]["icons"]["badge9_44x30.png"]
            }
        # resize rank images
        for key, image in self.rank_images.items():
            self.rank_images[key] = pygame.transform.scale(image, (image.get_width() / 2, image.get_height() / 2))

    def set_experience(self, value):
        self.experience += value
        self.set_rank()
        # print ("self.experience", self.experience)

    def set_rank_old(self):
        self.ranks = {0: "Cadet", 1: "Ensign", 2: "Lieutenant", 3: "Commander", 4: "Commodore", 5: "Captain", 6: "Vice Admiral", 7: "Admiral", 8: "Fleet Admiral"}
        rank_value = int(self.experience / self.experience_factor)
        if rank_value < 0:
            rank_value = 0
        elif rank_value > 8:
            rank_value = 8


        self.rank = self.ranks[rank_value]

    def set_rank(self):
        rank_value = int(self.experience / self.experience_factor)
        if rank_value < 0:
            rank_value = 0
        elif rank_value > 8:
            rank_value = 8
        prev_rank = self.rank
        self.rank = self.ranks[rank_value]
        prev_key = next((key for key, value in self.ranks.items() if value == prev_rank), None)
        curr_key = next((key for key, value in self.ranks.items() if value == self.rank), None)
        if curr_key > prev_key:
            self.parent.event_text = "Congratulations !!! Rank increased from {} to {} !!!".format(prev_rank, self.rank)
            sounds.play_sound(sounds.rank_up)
        elif curr_key < prev_key:
            self.parent.event_text = "Shame on you !!! Rank decreased from {} to {} !!!".format(prev_rank, self.rank)
            sounds.play_sound(sounds.rank_down)





    def draw_rank_image(self):
        if not source.Globals.app.build_menu_visible:
            image = self.rank_images[self.rank]
            self.win.blit(image, (
            self.getX() + self.getWidth() / 2 - image.get_width() / 2, self.getY() + self.rank_image_y))


class ShipMoving:
    """
    holds the fuctions and variables to move the ship:
    params:
            desired_orbit_radius
            offset
            orbit_angle (used for the orbit position)
            target (target to track or move to)
            moving
            orbiting
            orbit_speed
            orbit_object
            offset ( distance to orbit object)
            orbit_point ( the point to get for orbiting)

    functions:
            set_orbit_object (obj=any Planet, mouseposition, any Ship)
            orbit
            show_connections (draws lines between target and ship)
            move_to_connection
            set_energy_reloader
            set_progressbar_position (updates the progressbar position)
            low_energy_warning
            track_to
            set_position



    """

    def __init__(self):
        self.desired_orbit_radius = 100
        self.offset = None
        self.orbit_angle = 0.0
        self.target = None
        self.moving = False
        self.orbiting = False
        self.orbit_speed = 0.5
        self.orbit_object = None
        self.offset = Vector2(100, 0)
        self.orbit_point = None
        self.target_point = None

    def set_orbit_object(self, obj):
        self.orbit_object = obj
        self.orbit_distance = source.AppHelper.get_distance(self.pos, obj.pos)
        self.offset.x = self.orbit_object.getX() - self.getX()
        self.offset.y = self.orbit_object.getY() - self.getY()
        self.orbit_speed = self.offset.x #/ self.orbit_distance

    def orbit_od(self):
        self.orbit_object = self.energy_reloader
        self.offset = Vector2(self.orbit_object.getWidth(), self.orbit_object.getHeight())
        target_point = self.orbit_object.imageRect.center + self.offset.rotate(self.orbit_angle)

        # Calculate distance between object and orbit point
        distance = math.sqrt((self._x - target_point[0]) ** 2 + (self._y - target_point[1]) ** 2)

        if distance > self.desired_orbit_radius * 0.01:
            if self.energy > 0:
                # Move towards the orbit point
                direction = Vector2(target_point[0] - self._x, target_point[1] - self._y)
                direction.normalize_ip()
                direction *= self.orbit_speed
                self._x += direction.x
                self._y += direction.y
        else:
            # Calculate new orbit point
            self.orbit_angle -= self.orbit_speed
            self.orbit_point = self.orbit_object.imageRect.center + self.offset.rotate(self.orbit_angle)
            self._x = self.orbit_point[0]
            self._y = self.orbit_point[1]


        self.x = self._x
        self.y = self._y
        self.set_center()

    def orbit(self):
        self.orbit_object = self.energy_reloader
        self.offset = Vector2(self.orbit_object.getWidth(), self.orbit_object.getHeight())
        self.target_point = self.orbit_object.imageRect.center + self.offset.rotate(self.orbit_angle)

        # Calculate distance between object and orbit point
        distance = math.sqrt((self._x - self.target_point[0]) ** 2 + (self._y - self.target_point[1]) ** 2)

        if distance > self.desired_orbit_radius * 0.01:
            if self.energy > 0:
                # Move towards the orbit point
                direction = Vector2(self.target_point[0] - self._x, self.target_point[1] - self._y)
                direction.normalize_ip()
                direction *= self.orbit_speed #* distance  # Adjust the direction vector to be proportional to orbit_speed
                self._x += direction.x
                self._y += direction.y
        else:
            # Calculate new orbit point
            self.orbit_angle -= self.orbit_speed * distance
            self.orbit_point = self.orbit_object.imageRect.center + self.offset.rotate(self.orbit_angle)
            self._x = self.orbit_point[0]
            self._y = self.orbit_point[1]

        self.x = self._x
        self.y = self._y
        self.set_center()


    def show_connections(self):
        if self.target:
            if hasattr(self.target, "x"):
                pygame.draw.line(surface=self.win,
                    start_pos=self.center,
                    end_pos=self.target.center,
                    color=source.Globals.colors.frame_color,
                    width=5)

    def move_to_connection_(self):
        self.moving = True
        # if stopped for any reason, no travel
        if self.move_stop > 0:
            self.moving = False
            self.set_experience(-1)
            return

        # low energy warning
        # self.low_energy_warning()

        # if everyting fine, undock and travel!(reset energy loader)
        # if not self.energy <= 1:
        #     self.set_energy_reloader(None)

        # dist_x, dist_y, distance, target, x, y = self.calculate_new_position()
        #
        # try:
        #     new_x = x + (self.speed * dist_x)/distance*source.Globals.time_factor
        #     new_y = y + (self.speed * dist_y)/distance*source.Globals.time_factor
        # except ZeroDivisionError:
        #     return
        # dx, dy, distance, target, new_screen_x, new_screen_y = self.calculate_new_position()

        # self.setX((new_screen_x * dx)/distance*source.Globals.time_factor)
        # self.setY((new_screen_y* dy)/distance*source.Globals.time_factor)
        # set new position
        # self.setX(new_x)
        # self.setY(new_y)
        dx, dy, distance, target, new_screen_x, new_screen_y = self.calculate_new_position()
        self.setX(new_screen_x)
        self.setY(new_screen_y)
        # rotate image to target
        self.track_to(target)

        self.play_travel_sound()

        self.reach_goal(distance, target)

        self.calculate_travel_cost(distance)

        self.things_to_be_done_while_traveling()

        # self.x = self._x
        # self.y = self._y

        return True

    def move_to_connection(self):
        self.moving = True
        # if stopped for any reason, no travel
        if self.move_stop > 0:
            self.moving = False
            self.set_experience(-1)
            return
        pan_handler = self.parent.pan_zoom_handler

        # low energy warning
        self.low_energy_warning()

        # if everyting fine, undock and travel!(reset energy loader)
        # if not self.energy <= 1:
        #     self.set_energy_reloader(None)

        dist_x, dist_y, distance, target, x, y, new_x, new_y = self.calculate_new_position()

        self.calculate_new_position_1()

        debug_positions(x, y, "blue", "x,y:", 18)
        # debug_positions( , y, "blue", "x,y:", 18)

        # distance, target, new_x, new_y = self.calculate_new_position()

        # dx, dy, distance, target, new_screen_x, new_screen_y = self.calculate_new_position()

        # self.setX((new_screen_x * dx)/distance*source.Globals.time_factor)
        # self.setY((new_screen_y* dy)/distance*source.Globals.time_factor)
        # set new position

        # dx, dy, distance, target, new_screen_x, new_screen_y = self.calculate_new_position()
        # self.setX(new_screen_x)
        # self.setY(new_screen_y)

        # self.x = self._x
        # self.y = self._y

        # rotate image to target

        self.track_to(target)

        self.play_travel_sound()

        self.reach_goal(distance, target)

        self.calculate_travel_cost(distance)

        self.things_to_be_done_while_traveling()

        return True

    def calculate_new_position_2(self):
        # set target and calc new position
        self.set_center()
        target = self.target
        if hasattr(target, "x"):
            x1 = target.x
            y1 = target.y
        elif hasattr(target, "crew"):
            x1 = target.x
            y1 = target.y
        else:
            x1 = self.target[0]
            y1 = self.target[1]
        x = self.getX()
        y = self.getY()
        screen_x, screen_y = self.parent.pan_zoom_handler.world_2_screen(x, y)
        screen_x1, screen_y1 = self.parent.pan_zoom_handler.world_2_screen(x1, y1)
        world_x, world_y = self.parent.pan_zoom_handler.screen_2_world(screen_x, screen_y)
        world_x1, world_y1 = self.parent.pan_zoom_handler.screen_2_world(screen_x1, screen_y1)
        zoom = self.parent.pan_zoom_handler.zoom
        dist_x = (world_x1 - world_x) / zoom
        dist_y = (world_y1 - world_y) / zoom
        distance = math.dist((world_x, world_y), (world_x1, world_y1)) / zoom
        return dist_x, dist_y, distance, target, world_x, world_y

    def calculate_new_position_1(self):
        # set target and calc new position
        self.set_center()
        target = self.target
        if hasattr(target, "x"):
            x1 = target.x
            y1 = target.y
        elif hasattr(target, "crew"):
            x1 = target.x
            y1 = target.y
        else:
            x1 = self.target[0]
            y1 = self.target[1]
        x = self.getX()
        y = self.getY()
        screen_x, screen_y = self.parent.pan_zoom_handler.world_2_screen(x, y)
        screen_x1, screen_y1 = self.parent.pan_zoom_handler.world_2_screen(x1, y1)
        world_x, world_y = self.parent.pan_zoom_handler.screen_2_world(screen_x, screen_y)
        world_x1, world_y1 = self.parent.pan_zoom_handler.screen_2_world(screen_x1, screen_y1)
        dist_x = (world_x1 - world_x)
        dist_y = (world_y1 - world_y)
        distance = math.dist((world_x, world_y), (world_x1, world_y1))
        debug_positions(screen_x, screen_y, "yellow", "calculate_new_position_1: screen_x, screen_y: ", 20)
        debug_positions(world_x, world_y, "purple", "calculate_new_position_1: world_x, world_y: ", 22)

        # return dist_x, dist_y, distance, target, world_x, world_y

    def calculate_new_position(self):
        # set target and calc new position
        self.set_center()
        target, x1, y1 = self.get_target_position()
        pan_handler = self.parent.pan_zoom_handler
        zoom = self.parent.pan_zoom_handler.zoom
        x = self.getX()
        y = self.getY()
        dist_x = (x1 - x)
        dist_y = (y1 - y)
        distance = math.dist((x, y), (x1, y1))
        try:
            new_x = x + (self.speed * dist_x) / distance * source.Globals.time_factor
            new_y = y + (self.speed * dist_y) / distance * source.Globals.time_factor
        except ZeroDivisionError:
            new_x = x
            new_y = y

        # if pan_handler.tab == 2:
        #     new_x -=  pan_handler.world_offset_x * zoom
        #     new_y -= pan_handler.world_offset_y * zoom

        self.setX(new_x)
        self.setY(new_y)

        self.x = self._x
        self.y = self._y

        return dist_x, dist_y, distance, target, x, y, new_x, new_y

    def calculate_new_position__(self):
        # set target and calc new position
        self.set_center()
        target, x1, y1 = self.get_target_position()
        x, y = self.getX(), self.getY()
        screen_x, screen_y = self.parent.pan_zoom_handler.world_2_screen(x, y)
        world_x, world_y = self.parent.pan_zoom_handler.screen_2_world(screen_x, screen_y)
        screen_x1, screen_y1 = self.parent.pan_zoom_handler.world_2_screen(x1, y1)
        world_x1, world_y1 = self.parent.pan_zoom_handler.screen_2_world(screen_x1, screen_y1)
        dx, dy = world_x1 - world_x, world_y1 - world_y
        zoom = self.parent.pan_zoom_handler.zoom
        dx /= zoom
        dy /= zoom
        distance = math.dist((world_x, world_y), (world_x1, world_y1))
        try:
            new_x = x + (self.speed * dx) / distance * source.Globals.time_factor
            new_y = y + (self.speed * dy) / distance * source.Globals.time_factor
        except ZeroDivisionError:
            new_x = x
            new_y = y

        self.x = self._x
        self.y = self._y
        return distance, target, new_x, new_y

    def calculate_new_position_need_to_rewriet_zoom_hanlder(self):
        # set target and calc new position
        self.set_center()
        target, x1, y1 = self.get_target_position()
        x, y = self.getX(), self.getY()
        screen_x, screen_y = self.parent.pan_zoom_handler.world_2_screen(x, y)
        world_x, world_y = self.parent.pan_zoom_handler.screen_2_world(screen_x, screen_y)
        screen_x1, screen_y1 = self.parent.pan_zoom_handler.world_2_screen(x1, y1)
        world_x1, world_y1 = self.parent.pan_zoom_handler.screen_2_world(screen_x1, screen_y1)
        dx, dy = world_x1 - world_x, world_y1 - world_y
        zoom = self.parent.pan_zoom_handler.zoom
        dx /= zoom
        dy /= zoom
        distance = math.dist((world_x, world_y), (world_x1, world_y1))
        try:
            new_x = x + (self.speed * dx) / distance * source.Globals.time_factor
            new_y = y + (self.speed * dy) / distance * source.Globals.time_factor
        except ZeroDivisionError:
            new_x = x
            new_y = y
        # adjust position for change in zoom level
        old_zoom = self.parent.pan_zoom_handler.old_zoom
        if old_zoom != zoom:
            zoom_point = self.parent.pan_zoom_handler.zoom_point
            screen_zoom_point = self.parent.pan_zoom_handler.world_2_screen(*zoom_point)
            old_screen_x, old_screen_y = screen_x - screen_zoom_point[0], screen_y - screen_zoom_point[1]
            new_screen_x, new_screen_y = self.parent.pan_zoom_handler.world_2_screen(new_x, new_y)
            new_screen_x += screen_zoom_point[0]
            new_screen_y += screen_zoom_point[1]
            new_world_x, new_world_y = self.parent.pan_zoom_handler.screen_2_world(new_screen_x - old_screen_x, new_screen_y - old_screen_y)
            new_x, new_y = new_world_x, new_world_y
        # update object position
        new_screen_x, new_screen_y = self.parent.pan_zoom_handler.world_2_screen(new_x, new_y)
        self.setX(new_screen_x)
        self.setY(new_screen_y)
        self.x = self._x
        self.y = self._y
        # update old zoom and zoom point
        self.parent.pan_zoom_handler.old_zoom = zoom
        self.parent.pan_zoom_handler.zoom_point = self.parent.pan_zoom_handler.screen_2_world(*self.parent.pan_zoom_handler.zoom_point_screen)
        return distance, target, new_x, new_y

    def calculate_new_position_with_mouse_bug(self):
        # set target and calc new position
        self.set_center()
        target, x1, y1 = self.get_target_position()
        x, y = self.getX(), self.getY()
        screen_x, screen_y = self.parent.pan_zoom_handler.world_2_screen(x, y)
        world_x, world_y = self.parent.pan_zoom_handler.screen_2_world(screen_x, screen_y)
        screen_x1, screen_y1 = self.parent.pan_zoom_handler.world_2_screen(x1, y1)
        world_x1, world_y1 = self.parent.pan_zoom_handler.screen_2_world(screen_x1, screen_y1)
        dx, dy = world_x1 - world_x, world_y1 - world_y
        zoom = self.parent.pan_zoom_handler.zoom
        dx /= zoom
        dy /= zoom
        distance = math.dist((world_x, world_y), (world_x1, world_y1))
        try:
            new_x = x + (self.speed * dx) / distance * source.Globals.time_factor
            new_y = y + (self.speed * dy) / distance * source.Globals.time_factor
        except ZeroDivisionError:
            new_x = x
            new_y = y
        # adjust position for change in zoom level
        mouse_x, mouse_y = pygame.mouse.get_pos()
        old_screen_x, old_screen_y = self.parent.pan_zoom_handler.world_2_screen(mouse_x, mouse_y)
        new_screen_x, new_screen_y = self.parent.pan_zoom_handler.world_2_screen(new_x, new_y)
        new_screen_x += old_screen_x - mouse_x
        new_screen_y += old_screen_y - mouse_y
        new_world_x, new_world_y = self.parent.pan_zoom_handler.screen_2_world(new_screen_x, new_screen_y)
        new_x, new_y = new_world_x, new_world_y
        # update object position
        new_screen_x, new_screen_y = self.parent.pan_zoom_handler.world_2_screen(new_x, new_y)
        self.setX(new_screen_x)
        self.setY(new_screen_y)
        self.x = self._x
        self.y = self._y
        return distance, target, new_x, new_y

    def calculate_new_position__perpl(self):
        # set target and calc new position
        self.set_center()
        target, x1, y1 = self.get_target_position()
        x, y = self.getX(), self.getY()
        screen_x, screen_y = self.parent.pan_zoom_handler.world_2_screen(x, y)
        world_x, world_y = self.parent.pan_zoom_handler.screen_2_world(screen_x, screen_y)
        screen_x1, screen_y1 = self.parent.pan_zoom_handler.world_2_screen(x1, y1)
        world_x1, world_y1 = self.parent.pan_zoom_handler.screen_2_world(screen_x1, screen_y1)
        dx, dy = world_x1 - world_x, world_y1 - world_y
        zoom = self.parent.pan_zoom_handler.zoom
        dx /= zoom
        dy /= zoom
        distance = math.dist((world_x, world_y), (world_x1, world_y1))
        try:
            new_x = x + (self.speed * dx) / distance * source.Globals.time_factor
            new_y = y + (self.speed * dy) / distance * source.Globals.time_factor
        except ZeroDivisionError:
            new_x = x
            new_y = y
        # adjust position for change in zoom level
        zoom_point = self.parent.pan_zoom_handler.pan_start_pos
        old_screen_x, old_screen_y = self.parent.pan_zoom_handler.world_2_screen(*zoom_point)
        new_screen_x, new_screen_y = self.parent.pan_zoom_handler.world_2_screen(new_x, new_y)
        new_screen_x += old_screen_x - zoom_point[0]
        new_screen_y += old_screen_y - zoom_point[1]
        new_world_x, new_world_y = self.parent.pan_zoom_handler.screen_2_world(new_screen_x, new_screen_y)
        new_x, new_y = new_world_x, new_world_y
        # update object position
        new_screen_x, new_screen_y = self.parent.pan_zoom_handler.world_2_screen(new_x, new_y)
        self.setX(new_screen_x)
        self.setY(new_screen_y)
        self.x = self._x
        self.y = self._y
        return distance, target, new_x, new_y

    def calculate_new_position_trash(self):
        # set target and calc new position
        self.set_center()
        target, x1, y1 = self.get_target_position()
        x, y = self.getX(), self.getY()
        screen_x, screen_y = self.parent.pan_zoom_handler.world_2_screen(x, y)
        world_x, world_y = self.parent.pan_zoom_handler.screen_2_world(screen_x, screen_y)
        screen_x1, screen_y1 = self.parent.pan_zoom_handler.world_2_screen(x1, y1)
        world_x1, world_y1 = self.parent.pan_zoom_handler.screen_2_world(screen_x1, screen_y1)
        dx, dy = world_x1 - world_x, world_y1 - world_y
        zoom = self.parent.pan_zoom_handler.zoom
        dx /= zoom
        dy /= zoom
        distance = math.dist((world_x, world_y), (world_x1, world_y1))
        try:
            new_x = x + (self.speed * dx) / distance * source.Globals.time_factor
            new_y = y + (self.speed * dy) / distance * source.Globals.time_factor
        except ZeroDivisionError:
            new_x = x
            new_y = y
        # adjust position for change in zoom level
        zoom_point = self.parent.pan_zoom_handler.pan_start_pos
        old_screen_x, old_screen_y = self.parent.pan_zoom_handler.world_2_screen(*zoom_point)
        new_screen_x, new_screen_y = self.parent.pan_zoom_handler.world_2_screen(new_x, new_y)
        self.mouseworld_x_before, self.mouseworld_y_before = self.parent.pan_zoom_handler.screen_2_world(*zoom_point)
        self.mouseworld_x_after, self.mouseworld_y_after = self.parent.pan_zoom_handler.screen_2_world(new_screen_x, new_screen_y)
        new_screen_x += old_screen_x - zoom_point[0]
        new_screen_y += old_screen_y - zoom_point[1]
        new_world_x, new_world_y = self.parent.pan_zoom_handler.screen_2_world(new_screen_x, new_screen_y)
        new_x, new_y = new_world_x, new_world_y
        # update object position
        new_screen_x, new_screen_y = self.parent.pan_zoom_handler.world_2_screen(new_x, new_y)
        self.setX(new_screen_x)
        self.setY(new_screen_y)
        self.x = self._x
        self.y = self._y
        return distance, target, new_x, new_y

    def get_target_position(self):
        target = self.target
        if hasattr(target, "x") or hasattr(target, "crew"):
            x1 = target.imageRect.center[0]
            y1 = target.imageRect.center[1]
        else:
            x1 = self.target[0]
            y1 = self.target[1]
        return target, x1, y1

    def calculate_new_position_3(self):
        # set target and calc new position
        self.set_center()
        target = self.target
        if hasattr(target, "x"):
            x1 = target.x
            y1 = target.y
        elif hasattr(target, "crew"):
            x1 = target.x
            y1 = target.y
        else:
            x1 = self.target[0]
            y1 = self.target[1]
        x, y = self.getX(), self.getY()
        screen_x, screen_y = self.parent.pan_zoom_handler.world_2_screen(x, y)
        world_x, world_y = self.parent.pan_zoom_handler.screen_2_world(screen_x, screen_y)
        screen_x1, screen_y1 = self.parent.pan_zoom_handler.world_2_screen(x1, y1)
        world_x1, world_y1 = self.parent.pan_zoom_handler.screen_2_world(screen_x1, screen_y1)
        dx, dy = world_x1 - world_x, world_y1 - world_y
        zoom = self.parent.pan_zoom_handler.zoom
        dx /= zoom
        dy /= zoom
        new_x, new_y = world_x + dx, world_y + dy
        new_screen_x, new_screen_y = self.parent.pan_zoom_handler.world_2_screen(new_x, new_y)
        return new_screen_x, new_screen_y, target

    def calculate_new_position_4(self):
        # set target and calc new position
        self.set_center()
        target = self.target
        if hasattr(target, "x"):
            x1 = target.x
            y1 = target.y
        elif hasattr(target, "crew"):
            x1 = target.x
            y1 = target.y
        else:
            x1 = self.target[0]
            y1 = self.target[1]
        x, y = self.getX(), self.getY()
        screen_x, screen_y = self.parent.pan_zoom_handler.world_2_screen(x, y)
        world_x, world_y = self.parent.pan_zoom_handler.screen_2_world(screen_x, screen_y)
        screen_x1, screen_y1 = self.parent.pan_zoom_handler.world_2_screen(x1, y1)
        world_x1, world_y1 = self.parent.pan_zoom_handler.screen_2_world(screen_x1, screen_y1)
        dx, dy = world_x1 - world_x, world_y1 - world_y
        zoom = self.parent.pan_zoom_handler.zoom
        dx /= zoom
        dy /= zoom
        distance = math.dist((world_x, world_y), (world_x1, world_y1))
        try:
            new_x = x + (self.speed * dx) / distance * source.Globals.time_factor
            new_y = y + (self.speed * dy) / distance * source.Globals.time_factor
        except ZeroDivisionError:
            return dx, dy, distance, target, screen_x1, screen_y1
        new_screen_x, new_screen_y = self.parent.pan_zoom_handler.world_2_screen(new_x, new_y)
        return dx, dy, distance, target, new_screen_x, new_screen_y

    def calculate_new_position_5(self):
        speed = self.speed
        # set target and calc new position
        self.set_center()
        target = self.target
        if hasattr(target, "x"):
            x1 = target.x
            y1 = target.y
        elif hasattr(target, "crew"):
            x1 = target.x
            y1 = target.y
        else:
            x1 = self.target[0]
            y1 = self.target[1]
        x, y = self.getX(), self.getY()
        screen_x, screen_y = self.parent.pan_zoom_handler.world_2_screen(x, y)
        world_x, world_y = self.parent.pan_zoom_handler.screen_2_world(screen_x, screen_y)
        screen_x1, screen_y1 = self.parent.pan_zoom_handler.world_2_screen(x1, y1)
        world_x1, world_y1 = self.parent.pan_zoom_handler.screen_2_world(screen_x1, screen_y1)
        dx, dy = world_x1 - world_x, world_y1 - world_y
        zoom = self.parent.pan_zoom_handler.zoom
        dx /= zoom
        dy /= zoom
        distance = math.dist((world_x, world_y), (world_x1, world_y1))
        try:
            new_x = x + (speed * dx) / distance * source.Globals.time_factor
            new_y = y + (speed * dy) / distance * source.Globals.time_factor
        except ZeroDivisionError:
            return dx, dy, distance, target, screen_x1, screen_y1
        new_screen_x, new_screen_y = self.parent.pan_zoom_handler.world_2_screen(new_x, new_y)
        return dx, dy, distance, target, new_screen_x, new_screen_y

    def play_travel_sound(self):
        # plays sound
        if not self.hum_playing:
            sounds.play_sound(self.hum, channel=self.sound_channel, loops=1000, fade_ms=500)
            # pygame.mixer.Sound.play(self.hum)
            self.hum_playing = True

    def reach_goal(self, distance, target):
        # if goal reached (planet)
        if hasattr(self.target, "x"):
            if distance <= target.getWidth():
                self.target.explored = True

                # set event_text
                self.parent.event_text = "WELL DONE! your ship has just reached a habitable planet! : " + self.target.name

                # self.parent.draw()
                self.parent.fog_of_war.draw_fog_of_war(self.target)

                # unload_cargo goods
                self.unload_cargo()

                # reset selection/target
                self.set_energy_reloader(self.target)
                self.target = None
                self.select(False)

                # whats this for ?!???
                # self.rect = self.imageRect
                sounds.stop_sound(self.sound_channel)
                # pygame.mixer.Sound.stop(self.hum)
                self.hum_playing = False
                # sounds.stop_sound(self.sound_channel)
                self.moving = False




        elif hasattr(self.target, "crew"):
            if distance <= target.getWidth():
                # set event_text
                self.parent.event_text = "your ship has just reached a another ship: " + self.target.name + "reloading ship: " + self.name + "from : " + self.target.name

                # reset selection/target
                self.set_energy_reloader(self.target)
                self.target = None
                self.select(False)

                # whats this for ?!???
                self.rect = self.imageRect
                sounds.stop_sound(self.sound_channel)
                # pygame.mixer.Sound.stop(self.hum)
                self.hum_playing = False
                # sounds.stop_sound(self.sound_channel)
                self.moving = False


        else:
            if distance <= 5:
                self.target = None
                self.select(False)
                sounds.stop_sound(self.sound_channel)
                # pygame.mixer.Sound.stop(self.hum)
                self.hum_playing = False
                # sounds.stop_sound(self.sound_channel)

                # whats this for ?!???
                self.rect = self.imageRect
                self.moving = False

    def things_to_be_done_while_traveling(self):
        # set progress bar position
        self.set_progressbar_position()
        # self.parent.draw()
        self.parent.fog_of_war.draw_fog_of_war(self)
        # develop planet if distance is near enough
        self.develop_planet()
        # get experience
        self.set_experience(1)

    def calculate_travel_cost(self, distance):
        # calculate travelcosts
        self.energy -= distance * self.energy_use * source.Globals.time_factor
        self.energy = int(self.energy)

    def set_energy_reloader(self, obj):
        # print ("setting energy reloader to  :", obj)
        self.energy_reloader = obj

    def set_progressbar_position(self):
        # set progress bar position
        self.progress_bar.setX(self.getX())
        self.progress_bar.setY(self.getY() + self.getHeight() + +self.getHeight() / 5)

    def low_energy_warning(self):
        return
        """
        bloody chatbot fuction, if energy is running out
        :return:
        """
        # low energy warning
        if self.energy < self.energy_warning_level:
            self.parent.event_text = "LOW ENERGY WARNING!!! your ship is running out of energy! find a planet to land soon!!"

        if self.energy <= 0:
            self.parent.event_text = "DAMMIT!!! your ship has run out of energy! you all gonna die !!!"
            self.move_stop += 1

        # if ship energy is empty
        if self.energy <= 0 and self.move_stop > 1000:
            self.parent.event_text = "NO ENERGY DUDE! you cant move with this ship! "
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 2000:
            self.parent.event_text = "..mhhh--- there might be a solution -- let me think about it a few seconds.."
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 3000:
            self.parent.event_text = "the board engineer and i, have worked hard on a solution to this problem:"
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 4000:
            self.parent.event_text = "how about this: we sacrifice john the cook, i mean do we really need him?" \
                                     " put him into the plasma reactor of our spaceship and get some energy out of him !"
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 5000:
            self.parent.event_text = "type 'yes' or 'no' if you want to burn the last cook from earth for surviving"
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 6000:
            self.parent.event_text = "haha!! that was just a joke! funny istn it ??"
            self.move_stop += 1

        if self.energy <= 0 and self.move_stop > 7000:
            self.parent.event_text = "i mean, we will definitely cook the cook in the plasma engine, but I will decide for you :)"
            self.crew -= 1
            self.energy = 500
            self.move_stop = 0

        if self.energy > 0:
            self.move_stop = 0
        # print (self.move_stop)

    def track_to(self, target):
        """
        rotated the image to the target
        :param target: Planet, Ship or mouse position
        :return:
        """
        #   0 - image is looking to the right
        #  90 - image is looking up
        # 180 - image is looking to the left
        # 270 - image is looking down

        correction_angle = 90

        if hasattr(target, "x"):
            mx, my = target.getX(), target.getY()
        elif not self.target:
            mx, my = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        elif hasattr(target, "crew"):
            mx, my = target.getX(), target.getY()
        else:
            mx, my = target[0], target[1]

        dx, dy = mx - self.imageRect.centerx, my - self.imageRect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - correction_angle

        self.image_rot = pygame.transform.rotate(self.image, angle)
        self.image_rect_rot = self.image_rot.get_rect(center=self.center)
        self.imageRect = self.image_rect_rot

    def set_position(self):
        self.set_center()
        self.image_rect_rot = self.image_rot.get_rect(center=self.center)
        self.image_rect_rot.x = self._x
        self.image_rect_rot.y = self._y
        self.imageRect = self.image_rect_rot


class ShipButtons:
    """
    all UI elements of the ship, WIP
    """

    def __init__(self):
        self.visible = False
        self.speed_up_button = ImageButton(source.Globals.win, self.getX(), self.getY() + self.getHeight(), 32, 32,
            isSubWidget=False, image=source.Globals.images[pictures_path]["icons"]["speed_up.png"],
            onClick=lambda: print("Ok"))
        self.radius_button = ImageButton(source.Globals.win, self.getX() + self.getWidth(), self.getY() + self.getHeight(),
            32, 32, isSubWidget=False, image=source.Globals.images[pictures_path]["icons"]["radius.png"],
            onClick=lambda: print("Ok"))

    def reposition_buttons(self):
        self.spacing = 15
        self.speed_up_button.setX(self.getX() + self.getWidth() + self.spacing)
        self.speed_up_button.setY(self.getY() + self.getHeight())
        self.radius_button.setX(self.getX() + self.getWidth() + self.spacing)
        self.radius_button.setY(self.getY() + self.getHeight() - self.spacing * 3)

    def hide_buttons(self):
        self.speed_up_button.hide()
        self.radius_button.hide()

    def show_buttons(self):
        return
        self.speed_up_button.show()
        self.radius_button.show()


class ShipParams:
    """
    holds variables for the ship and functions aswell
    """

    def __init__(self, **kwargs):

        self.reload_max_distance = 100
        self.debug = True
        self.name = kwargs.get("name")
        self.parent = kwargs.get("parent")
        self.layer = kwargs.get("layer", 3)

        # setup Game variables
        self.food = kwargs.get("food", 0)
        self.food_max = 0
        self.minerals = kwargs.get("minerals", 0)
        self.minerals_max = 0
        self.water = kwargs.get("water", 0)
        self.water_max = 0
        self.population = kwargs.get("population", 0)
        self.population_max = 0
        self.technology = kwargs.get("technology", 0)
        self.technology_max = 0

        self.resources = {"minerals": self.minerals,
                          "food": self.food,
                          "population": self.population,
                          "water": self.water,
                          "technology": self.technology
                          }

        self.speed = 0.1
        self.energy_max = 10000
        self.energy = 10000
        self.energy_reloader = None
        self.move_stop = 0
        self.crew = 7
        self.crew_members = ["john the cook", "jim the board engineer", "stella the nurse", "sam the souvenir dealer",
                             "jean-jaques the artist", "Nguyen thon ma, the captain", "dr. Hoffmann the chemist"]

        # fog of war
        self.fog_of_war_radius = 100
        self.parent.fog_of_war.draw_fog_of_war(self)

        # orbit
        self.offset = Vector2(100, 0)
        self.angle = 0

        # energy progress bar
        self.progress_bar = ProgressBar(win=self.win,
            x=self.getX(),
            y=self.getY() + self.getHeight() + self.getHeight() / 5,
            width=self.getWidth(),
            height=5,
            progress=lambda: 1 / self.energy_max * self.energy,
            curved=True,
            completedColour=source.Globals.colors.frame_color,
            layer=self.layer,
            parent=self
            )
        # upgrade
        self.upgrade_factor = 1.5

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
                source.Globals.tooltip_text = ""

    def set_resources(self):
        self.resources = {"minerals": self.minerals,
                          "food": self.food,
                          "population": self.population,
                          "water": self.water,
                          "technology": self.technology
                          }

    def set_info_text(self):

        text = self.name + ":\n\n"
        text += "experience: " + str(self.experience) + "\n"
        text += "rank: " + self.rank + "\n\n"
        text += "resources loaded: " + "\n\n"
        text += "water: " + str(self.water) + "/" + str(self.water_max) + "\n"
        text += "energy: " + str(self.energy) + "/" + str(self.energy_max) + "\n"
        text += "food: " + str(self.food) + "/" + str(self.food_max) + "\n"
        text += "minerals: " + str(self.minerals) + "/" + str(self.minerals_max) + "\n"
        text += "technology: " + str(self.technology) + "/" + str(self.technology_max) + "\n\n"

        text += "speed: " + str(self.speed) + "\n"
        text += "scanner range: " + str(self.fog_of_war_radius) + "\n"
        text += "crew: " + str(self.crew) + "\n"

        if self.debug:
            text += "\n\ndebug:\n"
            text += "\ntarget: " + str(self.target) + "\n"

            text += "selected: " + str(self.selected) + "\n"
            text += "reloader: " + str(self.energy_reloader) + "\n"
            text += "move_stop: " + str(self.move_stop) + "\n"
            text += "moving: " + str(self.moving)

            # text += str(dir(self))

        self.parent.info_panel.set_text(text)
        self.parent.info_panel.set_planet_image(self.image)

    def develop_planet(self):
        for i in source.WidgetHandler.WidgetHandler.layers[3]:
            if "Planet" in str(i):
                if i.name == "Sun": return
                if int(self.get_distance_to(i)) <= i.fog_of_war_radius:
                    if not i.explored:
                        self.set_experience(1000)
                        self.parent.event_text = f"WELL DONE! your {self.name} has just reached a habitable planet! : " + i.name
                        i.show()
                        self.parent.set_selected_planet(i)
                        self.parent.fog_of_war.draw_fog_of_war(i)
                        self.set_info_text()
                        i.explored = True

    def get_distance_to(self, obj):
        x = self.getX()
        y = self.getY()

        if hasattr(obj, "x"):
            try:
                x1 = obj.getX()
                y1 = obj.getY()
            except AttributeError:
                x1 = obj[0]
                y1 = obj[1]
        else:
            x1 = obj[0]
            y1 = obj[1]

        distance = math.dist((x, y), (x1, y1))

        return distance

    def flickering(self):
        # make flickering relaod stream :))
        r0 = random.randint(-4, 5)
        r = random.randint(-3, 4)
        r1 = random.randint(0, 17)
        r2 = random.randint(0, 9)

        startpos = (self.imageRect.center[0] + r, self.imageRect.center[1] + r)
        endpos = (self.energy_reloader.imageRect.center[0] + r0, self.energy_reloader.imageRect.center[1] + r0)

        if r0 == 0:
            return

        if r == 3:
            pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
                color=pygame.color.THECOLORS["yellow"], width=r2)

        if r == 7:
            pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
                color=pygame.color.THECOLORS["red"], width=r1)

        if r == 2:
            pygame.draw.line(surface=self.win, start_pos=startpos, end_pos=endpos,
                color=pygame.color.THECOLORS["white"], width=r * 2)

        # pygame.mixer.Channel(2).play (source.Globals.sounds.electricity2)
        # sounds.play_sound(sounds.electricity2, channel=self.sound_channel)
        self.parent.event_text = "reloading spaceship: --- needs a lot of energy!"

    def reload_ship(self):
        if self.energy_reloader:
            if self.get_distance_to(self.energy_reloader) > self.reload_max_distance:
                return

            # if reloader is a planet
            if hasattr(self.energy_reloader, "production"):
                if self.energy_reloader.production["energy"] > 0:
                    if self.parent.player.energy - self.energy_reload_rate * self.energy_reloader.production["energy"] > 0:
                        if self.energy < self.energy_max:
                            self.energy += self.energy_reload_rate * self.energy_reloader.production["energy"]
                            self.parent.player.energy -= self.energy_reload_rate * self.energy_reloader.production[
                                "energy"]
                            self.flickering()
                        else:
                            self.parent.event_text = "Ship reloaded sucessfully!!!"
                            sounds.stop_sound(self.sound_channel)

            # if relaoder is a ship
            elif hasattr(self.energy_reloader, "crew"):
                if self.energy_reloader.energy > 0:
                    if self.energy_reloader.energy - self.energy_reload_rate > 0:
                        if self.energy < self.energy_max:
                            self.energy += self.energy_reload_rate
                            self.energy_reloader.energy -= self.energy_reload_rate
                            self.flickering()
                        else:
                            self.parent.event_text = "Ship reloaded sucessfully!!!"
                            sounds.stop_sound(self.sound_channel)
        else:
            sounds.stop_sound(self.sound_channel)

    def upgrade(self, key):
        setattr(self, key, getattr(self, key) * self.upgrade_factor)

    def unload_cargo(self):
        text = ""
        for key, value in self.resources.items():
            if value > 0:
                text += key + ": " + str(value)
                setattr(self.parent.player, key, getattr(self.parent.player, key) + value)
                self.resources[key] = 0
                setattr(self, key, 0)

                self.parent.event_text = "unloading ship: " + text
                sounds.play_sound(sounds.unload_ship)


class Ship(WidgetBase, ShipParams, ShipMoving, Moveable, ShipRanking, ShipButtons):
    """ this is the Ship class"""

    def __init__(self, win, x, y, width, height, isSubWidget=False, *args, **kwargs):
        WidgetBase.__init__(self, win, x, y, width, height, isSubWidget, **kwargs)
        ShipParams.__init__(self, **kwargs)
        ShipMoving.__init__(self)
        Moveable.__init__(self, x, y, width, height, kwargs)
        ShipRanking.__init__(self)
        ShipButtons.__init__(self)

        # display

        self.layer = kwargs.get("layer", 3)
        self.image_initial = kwargs.get("image")
        self.image = pygame.transform.scale(self.image_initial, (self.getWidth(), self.getHeight()))
        self.imageRect = self.image.get_rect()
        self.imageRect.left = self.getX()
        self.imageRect.top = self.getY()
        self.center = None
        self.set_center()

        # selection image
        self.selection_image = pygame.transform.scale(kwargs.get("selection_image"), (
        self.getWidth(), self.getHeight()))
        self.selection_image.set_alpha(200)

        # no energy image
        self.noenergy_image = source.Globals.images[pictures_path]["resources"]["noenergy_25x25.png"]

        # this is used for rotating, we will blitt mostly this.
        # TODO: use image instead of rot image and get source from image initial
        self.image_rot = pygame.transform.rotate(self.image, 90)
        self.image_rect_rot = self.image_rot.get_rect(center=self.center)

        # sound
        self.hum_playing = False

        # functionality
        self.on_hover = False
        self.on_hover_release = False
        self.selected = False
        self.target = None

        # register
        self.parent.ships.append(self)

    def get_hit_object(self):
        for obj in self.parent.planets:
            if obj.imageRect.collidepoint(pygame.mouse.get_pos()):
                return obj

        for obj in self.parent.ships:
            if obj.imageRect.collidepoint(pygame.mouse.get_pos()):
                return obj
        return None

    def listen(self, events):
        self.reset_tooltip()

        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                # print("ship.listen:", mouseState)
                if mouseState == MouseState.RIGHT_CLICK:
                    if self.parent.ship == self:
                        if self.selected:
                            self.select(False)
                        else:
                            self.select(True)

                if mouseState == MouseState.RELEASE and self.clicked:
                    self.clicked = False

                elif mouseState == MouseState.CLICK:
                    self.clicked = True
                    self.select(True)
                    self.parent.ship = self

                elif mouseState == MouseState.DRAG and self.clicked:
                    pass

                elif mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                    self.submit_tooltip()
            else:
                self.clicked = False

                if mouseState == MouseState.CLICK:
                    self.select(False)
                    if self.parent.ship == self:
                        self.parent.ship = None

                if mouseState == MouseState.RIGHT_CLICK:
                    if self.parent.ship == self:

                        self.set_target()
                        if self.get_hit_object():
                            self.set_energy_reloader(self.get_hit_object())

    def set_target(self):
        target = self.get_hit_object()
        if target == self:
            return
        if target:
            self.target = target
            self.energy_reloader = target

            # this resets the orbit angle to make shure start point is always the same
            self.angle = 0
        else:
            self.target = pygame.mouse.get_pos()
            self.set_energy_reloader(None)

        self.select(False)

    def set_tooltip(self):
        text = "selected: " + str(self.selected)
        self.tooltip = self.name + ": " + " speed: " + str(self.speed) + "e, scanner range: " + str(self.fog_of_war_radius) + text

    def submit_tooltip(self):
        if self.tooltip:
            if self.tooltip != "":
                source.Globals.tooltip_text = self.tooltip

    # draw functions
    def draw(self):

        self.set_position()
        self.set_progressbar_position()
        # if self._hidden:
        #     return
        self.draw_image_rot()
        self.draw_rank_image()

        # print("ship state: ", self.rank)

        if self.selected:
            self.show_selection()
            self.draw_line()
            # self.track_to(pygame.mouse.get_pos())
            self.set_info_text()

        # travel
        if self.target:
            if self.energy > 0:
                self.move_to_connection()
                self.show_connections()

        if self.energy_reloader:
            # self.draw_dict()
            # reload ship
            self.reload_ship()
            # orbit around the planet

            self.orbit()
            self.orbiting = True
        else:
            self.orbiting = False

        # move stopp reset
        if self.energy > 0:
            self.move_stop = 0

        # move stopp
        if self.energy <= 0:
            self.move_stop += 1

            sounds.stop_sound(self.sound_channel)
            self.draw_noenergy_image()
            self.set_experience(-1)

        self.low_energy_warning()

        # self.update_position()
        debug_positions(x=self.x, y=self.y, color=colors.frame_color, size=10, text="self.x, self.y: ")
        debug_positions(x=self._x, y=self._y, color="red", size=12, text="self._x, self._y: ")


    def draw_image_rot(self):
        if not source.Globals.app.build_menu_visible:
            self.win.blit(self.image_rot, self.image_rect_rot)

    def draw_line(self):
        """
        draws line to mouse position and draws the scope

        """
        # draw line from selected object to mouse cursor
        if self.selected:
            pygame.draw.line(surface=self.win, start_pos=self.center, end_pos=pygame.mouse.get_pos(), color=source.Globals.colors.frame_color)

            # scope
            pos = pygame.mouse.get_pos()
            size_x = 30
            size_y = 30
            arrow = pygame.draw.arc(self.win, source.Globals.colors.frame_color, (
            (pos[0] - size_x / 2, pos[1] - size_y / 2), (size_x, size_y)), 2, 10, 2)
            arrow = pygame.draw.arc(self.win, source.Globals.colors.frame_color, (
            (pos[0] - size_x, pos[1] - size_y), (size_x * 2, size_y * 2)), 2, 10, 2)

            # horizontal line
            factor = size_x / 12
            x = pos[0] - size_x * factor / 2
            y = pos[1]
            x1 = x + size_x * factor
            y1 = y
            pygame.draw.line(surface=self.win, start_pos=(x, y), end_pos=(
            x1, y1), color=source.Globals.colors.frame_color)

            # vertical line
            x = pos[0]
            y = pos[1] - size_x * factor / 2
            x1 = x
            y1 = y + size_x * factor
            pygame.draw.line(surface=self.win, start_pos=(x, y), end_pos=(
            x1, y1), color=source.Globals.colors.frame_color)

    def set_center(self):
        self.center = (self.getX() + self.getWidth() / 2, self.getY() + self.getHeight() / 2)

    def show_selection(self):
        self.win.blit(self.selection_image, (self.getX(), self.getY()))

    def select(self, value):
        self.selected = value
        if value:
            sounds.play_sound("click", channel=7)

    def update(self):
        self.reposition_buttons()
        if self.selected:
            self.show_buttons()
        else:
            self.hide_buttons()

    def draw_noenergy_image(self):
        if not self._disabled:
            self.win.blit(self.noenergy_image, (
            self.getX() + self.noenergy_image_x, self.getY() + self.noenergy_image_y))
