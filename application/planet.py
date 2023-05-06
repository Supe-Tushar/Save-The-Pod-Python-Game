"""
Author: Tushar Supe
Game: Pygame-Save The Pod
FileType: Python file
Details: This python file contains all classes required for Main Game screen (Shuttle, Asteroid).
"""

# -----------------------------------------  IMPORTS  -------------------------------------------

import math
from .constants import *


# -----------------------------------------  Classes  -------------------------------------------
class Planet:
    def __init__(self, win, pos_x=0, pos_y=0, angle=0, gravity=True, blackhole=False):
        self.win = win
        self.pos_x = pos_x  # position of centre of planet
        self.pos_y = pos_y
        self.angle = angle
        self.use_gravity = gravity
        self.PLANET = scale_image(PLANET, factor=1)
        self.BLACKHOLE = scale_image(BLACKHOLE, factor=1)
        self.min_dist = 50
        self.max_dist = 150
        self.is_blackhole = blackhole
        if self.is_blackhole:
            self.max_dist = 250

    def attraction_force(self, shuttle_x, shuttle_y):
        # shuttle postions of its center
        force_x, force_y = 0, 0
        is_collided = False

        dist_x = shuttle_x - self.pos_x
        dist_y = shuttle_y - self.pos_y
        dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
        dist_angle = math.atan2(dist_y, dist_x)


        if self.use_gravity:
            if self.min_dist < dist < self.max_dist:
                force = (G * SHUTTLE_MASS * PLANET_MASS) / (dist ** 2)
                if self.is_blackhole:
                    force *= BLACKHOLE_CONSTANT
                force_x = math.cos(dist_angle) * force
                force_y = math.sin(dist_angle) * force

        if self.min_dist >= dist:
            is_collided = True

        return force_x, force_y, is_collided

    def draw(self):
        x = self.pos_x - self.PLANET.get_width() / 2
        y = self.pos_y - self.PLANET.get_height() / 2
        image = self.PLANET
        if self.is_blackhole:
            self.angle = 0
            image = self.BLACKHOLE
        rotate_image_center(self.win, image=image, top_left=(x, y), angle=self.angle, update=False)
        radius_range = self.max_dist - self.min_dist
        num_rings = 3
        for i in range(num_rings):  # draw 3 circles
            radius = self.min_dist + radius_range
            radius_range /= 2
            pygame.draw.circle(self.win, LIGHT_GRAY, (self.pos_x, self.pos_y), radius, width=1)
