"""
Author: Tushar Supe
Game: Pygame-Save The Pod
FileType: Python file
Details: This python file contains Shuttle class.
"""

# -----------------------------------------  IMPORTS  -------------------------------------------
import math
import pygame.time
from .constants import *



# -----------------------------------------  Classes  -------------------------------------------
class Shuttle:
    def __init__(self, win, start_x=0, start_y=0, use_ang_vel=False, use_gravity=True, use_fuel=True):
        self.win = win
        self.SHUTTLE = SHUTTLE
        self.SHUTTLE_EXPLODED = SHUTTLE_EXPLODED
        self.THRUST_TOP = scale_image(THRUST_TOP, factor=1)
        self.THRUST_SIDE = scale_image(THRUST_SIDE, factor=1)
        self.THRUST_BOTTOM = scale_image(THRUST_BOTTOM, factor=1)
        self.FLAME = scale_image(FLAME, factor=1)
        self.use_gravity = use_gravity
        self.use_fuel = use_fuel

        self.vel_max = 1.5
        self.ang_vel_max = 1.5
        self.acc = 0.05
        self.ang_acc = 600 * (1 / FPS)

        self.START_POS = (start_x, start_y)
        self.vel_x = 0
        self.vel_y = 0
        self.ang_vel = 0
        self.angle = 0
        self.pos_x = start_x
        self.pos_y = start_y
        self.use_ang_vel = use_ang_vel
        self.fuel = 100
        self.fuel_constant = 0.1
        if not self.use_ang_vel:
            self.ang_acc = 10
        self.play_sound, self.play_music, _, _ = load_current_config_constants()

    def velocity_max_min_adjust(self):
        self.vel_y = max(-self.vel_max, min(self.vel_max, self.vel_y))
        self.vel_x = max(-self.vel_max, min(self.vel_max, self.vel_x))

    def check_fuel(self):
        if self.fuel <= 0:
            return True
        return False

    def update_fuel(self):
        if self.use_fuel:
            self.fuel -= self.fuel_constant
            self.fuel = max(self.fuel, 0)

    def wormhole_teleport(self, x, y , dist, angle):
        """ x, y positions of red wormhole """
        dist += 10
        angle += math.pi
        self.pos_x = x - 32 + (dist * math.sin(angle))
        self.pos_y = y - 32 + (dist * math.cos(angle))
        # self.vel_x = 0
        # self.vel_y = 0



    def gravity_force(self, fx, fy, is_collided):
        # print(fx, fy, self.vel_x, self.vel_y, fx / SHUTTLE_MASS, fy / SHUTTLE_MASS)
        if not is_collided:
            self.vel_x -= fx / SHUTTLE_MASS
            self.vel_y += fy / SHUTTLE_MASS
            self.velocity_max_min_adjust()
        else:
            self.explosion()

    def explosion(self):
        if self.play_sound: pygame.mixer.Sound.play(EXPLOSION_SOUND)
        rotate_image_center(self.win, self.SHUTTLE_EXPLODED, top_left=(self.pos_x, self.pos_y), angle=self.angle,
                            update=True)
        pygame.time.delay(1000)
        self.reset()


    def stop(self):
        self.vel_x = 0
        self.vel_y = 0
        self.ang_vel = 0

    def reset(self):
        self.vel_x = 0
        self.vel_y = 0
        self.ang_vel = 0
        self.angle = 0
        self.pos_x, self.pos_y = self.START_POS


    def move(self):

        self.pos_x += self.vel_x
        self.pos_y -= self.vel_y
        self.angle -= self.ang_vel
        if abs(self.angle) >= 360:
            self.angle = 0
        if not self.use_ang_vel:
            self.ang_vel = 0
        if self.pos_x > 585:
            self.pos_x = 585
            self.vel_x = 0
        if self.pos_x < 1:
            self.pos_x = 1
            self.vel_x = 0
        if self.pos_y > 585:
            self.pos_y = 585
            self.vel_y = 0
        if self.pos_y < 1:
            self.pos_y = 1
            self.vel_y = 0


    def play_throttle_sound(self):
        if self.play_sound: pygame.mixer.Sound.play(THROTTLE_SOUND)

    def play_vent_sound(self):
        if self.play_sound: pygame.mixer.Sound.play(VENT_SOUND)

    def throttle_down(self):
        self.update_fuel()
        if self.play_sound: self.play_throttle_sound()
        radians = math.radians(self.angle)
        self.vel_y += (math.cos(radians) * self.acc)
        self.vel_x -= (math.sin(radians) * self.acc)
        self.velocity_max_min_adjust()
        dx = (self.pos_x + 32) + (35 * math.sin(radians)) - self.FLAME.get_width() / 2
        dy = (self.pos_y + 32) + (35 * math.cos(radians)) - self.FLAME.get_width() / 2
        rotate_image_center(self.win, self.FLAME, top_left=(dx, dy), angle=self.angle, update=True)

    def throttle_up(self):
        self.update_fuel()
        if self.play_sound: self.play_vent_sound()
        radians = math.radians(self.angle)
        self.vel_y -= (math.cos(radians) * self.acc)
        self.vel_x += (math.sin(radians) * self.acc)
        self.velocity_max_min_adjust()

    def throttle_left(self):
        self.update_fuel()
        if self.play_sound: self.play_vent_sound()
        radians = math.radians(self.angle + 90)
        self.vel_y -= (math.cos(radians) * self.acc)
        self.vel_x += (math.sin(radians) * self.acc)
        self.velocity_max_min_adjust()

    def throttle_right(self):
        self.update_fuel()
        if self.play_sound: self.play_vent_sound()
        radians = math.radians(self.angle + 90)
        self.vel_y += (math.cos(radians) * self.acc)
        self.vel_x -= (math.sin(radians) * self.acc)
        self.velocity_max_min_adjust()

    def throttle_cw(self):
        self.update_fuel()
        if self.play_sound: self.play_vent_sound()
        self.ang_vel += self.ang_acc
        self.ang_vel = max(-self.ang_vel_max, min(self.ang_vel_max, self.ang_vel))

    def throttle_ccw(self):
        self.update_fuel()
        if self.play_sound: self.play_vent_sound()
        self.ang_vel -= self.ang_acc
        self.ang_vel = max(-self.ang_vel_max, min(self.ang_vel_max, self.ang_vel))

    def draw(self):
        self.move()
        rotate_image_center(self.win, self.SHUTTLE, top_left=(self.pos_x, self.pos_y), angle=self.angle, update=False)
