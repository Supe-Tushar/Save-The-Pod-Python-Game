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
class Star:
    def __init__(self, win, pos_x=0, pos_y=0, angle=0, ang_acc=0.17, direction="cw", rotate=True):
        self.win = win
        self.pos_x = pos_x  # position of centre of planet
        self.pos_y = pos_y
        self.angle = angle
        self.ang_acc = ang_acc
        self.rotate = rotate
        self.direction = direction
        self.STAR = scale_image(STAR, factor=1)
        self.is_draw = True

    def collision(self, shuttle_x, shuttle_y):
        # shuttle postions of its center
        is_collided = False
        if self.is_draw:
            dist_x = shuttle_x - self.pos_x
            dist_y = shuttle_y - self.pos_y
            dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
            if 50 >= dist:
                is_collided = True
        return is_collided

    def draw(self):
        x = self.pos_x - self.STAR.get_width() / 2
        y = self.pos_y - self.STAR.get_height() / 2
        if self.rotate:
            if self.direction == "cw":
                self.angle -= self.ang_acc
            if self.direction == "ccw":
                self.angle += self.ang_acc
        if self.is_draw:
            rotate_image_center(self.win, self.STAR, top_left=(x, y), angle=self.angle, update=False)
