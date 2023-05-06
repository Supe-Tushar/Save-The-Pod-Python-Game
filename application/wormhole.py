"""
Author: Tushar Supe
Game: Pygame-Save The Pod
FileType: Python file
Details: This python file contains all classes required for Wormhole portal
"""

# -----------------------------------------  IMPORTS  -------------------------------------------

import math
from .constants import *


# -----------------------------------------  Classes  -------------------------------------------
class Wormhole:
    def __init__(self, win, pos_x=0, pos_y=0, angle=0, color="blue"):
        self.win = win
        self.pos_x = pos_x  # position of centre of planet
        self.pos_y = pos_y
        self.angle = angle
        self.min_dist = 32
        if color == "blue":
            self.WORMHOLE = scale_image(WORMHOLE_B, factor=1.5)
        else:
            self.WORMHOLE = scale_image(WORMHOLE_R, factor=1.5)

    def collision(self, shuttle_x, shuttle_y):
        # shuttle postions of its center
        is_collided = False

        dist_x = shuttle_x - self.pos_x
        dist_y = shuttle_y - self.pos_y
        dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
        dist_angle = 0


        if self.min_dist >= dist:
            is_collided = True
            dist_angle = math.atan2(dist_y, dist_x)

        return is_collided, dist, dist_angle

    def draw(self):
        x = self.pos_x - self.WORMHOLE.get_width() / 2
        y = self.pos_y - self.WORMHOLE.get_height() / 2
        rotate_image_center(self.win, image=self.WORMHOLE, top_left=(x, y), angle=self.angle, update=False)
