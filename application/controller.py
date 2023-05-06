"""
Author: Tushar Supe
Game: Pygame-Save The Pod
FileType: Python file
Details: This python file contains main game loop
"""

# -----------------------------------------  IMPORTS  -------------------------------------------

from .constants import *
from .utils import *
from .start_screen import Start
from .menu_screen import Menu

def main():
    """ Main Function with Game Loop """

    pygame.event.clear()

    start_screen = Start(WIN)
    if not start_screen.start():
        pygame.quit()
    else:
        menu_screen = Menu(WIN)
        if not menu_screen.start():
            pygame.quit()

    pygame.quit()

