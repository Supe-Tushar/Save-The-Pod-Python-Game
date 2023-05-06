"""
Author: Tushar Supe
Game: Pygame-Save The Pod
FileType: Python file
Details: This python file containts Help screen class.
"""

# -----------------------------------------  IMPORTS  -------------------------------------------
from .constants import *


# -----------------------------------------  Main Screen Class  -------------------------------------------
class Help:
    def __init__(self, win):
        self.menu_title = menu_title_font.render("Help", True, (81, 255, 17))
        self.general_text_font = general_text_font
        self.help_content_font = help_content_font
        self.win = win
        self.SHUTTLE = scale_image(SHUTTLE, factor=0.4)
        self.show_help_screen = True
        self.game_quit = False
        self.dt = 0
        self.prev_time = pygame.time.get_ticks()
        self.curr_time = 0

    def blit_help_text(self):
        help_strings = ["Rotate POD with Left/Right arrow keys",
                        "Move POD with W-A-S-D Keys",
                        "Do not crash into planets",
                        "Planets exerts gravitational pull",
                        "Collect all stars to complete the level",
                        "Black Holes have higher gravitational pull",
                        "Worm holes are portals from one location to other",
                        "Music/Sound can be turned on/off from Options",
                        "Gravity/Fuel can be turned on/off from Options"
                        ]

        pos_x, pos_y = 32, 130  # Positons hardcoded as per requirements
        for string in help_strings:
            help_content = self.help_content_font.render(string, True, (81, 255, 17))
            self.win.blit(help_content, (pos_x, pos_y))
            rotate_image_center(self.win,
                                self.SHUTTLE,
                                top_left=(pos_x - self.SHUTTLE.get_width(), pos_y),
                                angle=-90)
            pos_y += 50

    def update_dt(self):
        self.curr_time = pygame.time.get_ticks()
        self.dt += self.curr_time - self.prev_time
        self.prev_time = self.curr_time

    def blink_text(self, millisec=1000):
        if self.dt > millisec:
            general_text = self.general_text_font.render("Press BACKSPACE to Go Back", True, (81, 255, 17))
            self.win.blit(general_text, (self.win.get_width() / 2 - general_text.get_width() / 2, 80))
        if self.dt > millisec * 2:
            self.dt = 0

    def update_screen(self):
        draw(self.win, [(SPACE, (0, 0)),
                        (scale_image(SHUTTLE_HELP, factor=0.8),
                         ((self.win.get_width() - SHUTTLE_HELP.get_width() + 70), 100))
                        ],
             update=False)

        self.win.blit(self.menu_title,
                      (self.win.get_width() / 2 - self.menu_title.get_width() / 2, 20))

        self.blink_text(millisec=500)
        self.blit_help_text()
        pygame.display.flip()

    def start(self):
        while self.show_help_screen:
            clock.tick(FPS)
            self.update_dt()
            self.update_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.show_help_screen = False
                    self.game_quit = True
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.show_help_screen = False
                        self.game_quit = False
                        break


        if self.game_quit:
            return False
        else:
            return True
