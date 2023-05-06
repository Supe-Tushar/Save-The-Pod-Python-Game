"""
Author: Tushar Supe
Game: Pygame-Save The Pod
FileType: Python file
Details: This python file contains helper function and classes required for game
"""

# -----------------------------------------  IMPORTS  -------------------------------------------
import pygame
import json
import os

MAIN_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -----------------------------------------  Functions  -------------------------------------------
def scale_image(img, *size, factor=None):
    if factor is not None:
        size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def rotate_image_center(win, image, top_left, angle, update=False):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)
    if update:
        pygame.display.update()


def draw(win, images, update=False):
    for img, pos in images:
        win.blit(img, pos)
    if update:
        pygame.display.update()


def load_game_info():
    game_info = {}
    try:
        with open(os.path.join(MAIN_PATH, "data/game_info.json"), "r") as jsn:
            game_info = json.load(jsn)
    except Exception as e:
        print(f"Error occured while opening json file: {e}")
    return game_info

def save_game_info(game_info):
    try:
        with open(os.path.join(MAIN_PATH, "data/game_info.json"), "w+") as jsn:
            json.dump(game_info, jsn, indent=4)
    except Exception as e:
        print(f"Error occured while saving json file: {e}")

def load_config():
    config = {}
    try:
        with open(os.path.join(MAIN_PATH, "data/config.json"), "r") as jsn:
            config = json.load(jsn)
    except Exception as e:
        print(f"Error occured while opening json file: {e}")
    return config

def save_config(config):
    try:
        with open(os.path.join(MAIN_PATH, "data/config.json"), "w+") as jsn:
            json.dump(config, jsn, indent=4)
    except Exception as e:
        print(f"Error occured while saving json file: {e}")


def load_current_config_constants():
    config = load_config()
    s = True if config["sound"] == 1 else False
    m = True if config["music"] == 1 else False
    g = True if config["gravity"] == 1 else False
    f = True if config["fuel"] == 1 else False
    return s,m,g,f


