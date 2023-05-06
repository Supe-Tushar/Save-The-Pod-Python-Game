"""
Author: Tushar Supe
Game: Pygame-Save The Pod
FileType: Python file
Details: This python file containts required constants like images
"""

# -----------------------------------------  IMPORTS  -------------------------------------------
from .utils import *
import os
# -----------------------------------------  CONSTANTS  -------------------------------------------

MAIN_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SOUND_ON = True
MUSIC_ON = True
GRAVITY_ON = True
FUEL_ON = True



config = load_config()
SOUND_ON = True if config["sound"] == 1 else False
MUSIC_ON = True if config["music"] == 1 else False
GRAVITY_ON = True if config["gravity"] == 1 else False
FUEL_ON = True if config["fuel"] == 1 else False


FPS = 60
clock = pygame.time.Clock()

WIDTH, HEIGHT = 650, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

SHUTTLE = pygame.image.load(os.path.join(MAIN_PATH, "images/shuttle.png"))
SHUTTLE_HELP = pygame.image.load(os.path.join(MAIN_PATH, "images/shuttleHelp.png"))
THRUST_TOP = pygame.image.load(os.path.join(MAIN_PATH, "images/topThruster.png"))
THRUST_SIDE = pygame.image.load(os.path.join(MAIN_PATH, "images/sideThruster.png"))
THRUST_BOTTOM = pygame.image.load(os.path.join(MAIN_PATH, "images/bottomThruster.png"))
FLAME = pygame.image.load(os.path.join(MAIN_PATH, "images/flame.png"))
SPACE = scale_image(pygame.image.load(os.path.join(MAIN_PATH, "images/space_background.png")), WIDTH, HEIGHT)
PLANET = pygame.image.load(os.path.join(MAIN_PATH, "images/planet.png"))
SHUTTLE_EXPLODED = pygame.image.load(os.path.join(MAIN_PATH, "images/shuttleExplosion.png"))
STAR = pygame.image.load(os.path.join(MAIN_PATH, "images/star.png"))
WORMHOLE_B = pygame.image.load(os.path.join(MAIN_PATH, "images/worm_hole_blue.png"))
WORMHOLE_R = pygame.image.load(os.path.join(MAIN_PATH, "images/worm_hole_red.png"))
BLACKHOLE = pygame.image.load(os.path.join(MAIN_PATH, "images/black_hole.png"))

# G = 6.67e-11  # Gravitational constant m3 kg-1 s-2
# SHUTTLE_MASS = 1.98e30 # kg
# PLANET_MASS = 5.97e24  # kg
G = 0.1  # 0.1 Gravitational constant m3 kg-1 s-2
SHUTTLE_MASS = 1  # 1 kg
PLANET_MASS = 1000  # 1000 kg
BLACKHOLE_CONSTANT = 5

pygame.display.set_caption("Save The Pod")
pygame.display.set_icon(scale_image(SHUTTLE, factor=0.5))

game_title_font = pygame.font.SysFont("CASTELLAR", 60)
general_text_font = pygame.font.SysFont("verdana", 15)
help_content_font = pygame.font.SysFont("verdana", 20, bold=False, italic=False)
menu_title_font = pygame.font.SysFont("ENGRAVERS", 50)
menu_content_font = pygame.font.SysFont("PERPETUATI", 40)

LIGHT_GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (81, 255, 17)
LIGHT_GREEN = (200, 255, 50)

LEVEL_COMPLETE_SOUND = pygame.mixer.Sound(os.path.join(MAIN_PATH, "sounds/level_complete.wav"))
STAR_SOUND = pygame.mixer.Sound(os.path.join(MAIN_PATH, "sounds/star.wav"))
TAB_CHANGE_SOUND = pygame.mixer.Sound(os.path.join(MAIN_PATH, "sounds/tab_change.wav"))
VALUE_CHANGE_SOUND = pygame.mixer.Sound(os.path.join(MAIN_PATH, "sounds/value_change.wav"))
WORMHOLE_SOUND = pygame.mixer.Sound(os.path.join(MAIN_PATH, "sounds/wormhole.wav"))
THROTTLE_SOUND = pygame.mixer.Sound(os.path.join(MAIN_PATH, "sounds/throttle.mp3"))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join(MAIN_PATH, "sounds/explosion.mp3"))
VENT_SOUND = pygame.mixer.Sound(os.path.join(MAIN_PATH, "sounds/vent.mp3"))
pygame.mixer.music.load(os.path.join(MAIN_PATH, "sounds/music.mp3"))
MUSIC_VOLUME = 0.1

if MUSIC_ON:
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(MUSIC_VOLUME)

print("Constants loaded")
