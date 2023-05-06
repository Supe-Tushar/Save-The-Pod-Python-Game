"""
Author: Tushar Supe
Game: Pygame-Save The Pod
FileType: Python file
Details: This python file containts Starting screen class template.
"""

# -----------------------------------------  IMPORTS  -------------------------------------------

from .constants import *


# -----------------------------------------  Main Screen Class  -------------------------------------------
class Start:
    def __init__(self, win):
        self.game_title = game_title_font.render("Save The Pod", True, (81, 255, 17))
        self.text = general_text_font.render("Press Any Key to Continue", True, (81, 255, 17))
        self.win = win
        self.show_start_screen = True
        self.game_quit = False
        self.dt = 0
        self.prev_time = pygame.time.get_ticks()
        self.curr_time = 0
        self.angle = 0
        self.ang_vel = -270  # degree/sec

    def update_dt(self):
        self.curr_time = pygame.time.get_ticks()
        self.dt += self.curr_time - self.prev_time
        self.prev_time = self.curr_time

    def blink_text(self, millisec=1000):
        if self.dt > millisec:
            self.win.blit(self.text,
                          (self.win.get_width() / 2 - self.text.get_width() / 2,
                           self.win.get_height() / 2))
        if self.dt > millisec * 2:
            self.dt = 0

    def update_screen(self):
        draw(self.win, [(SPACE, (0, 0))], update=False)
        rotate_image_center(self.win,
                            SHUTTLE,
                            top_left=(self.win.get_width() / 2 - SHUTTLE.get_width() / 2, 450),
                            angle=self.angle)
        screen_width, screen_height = self.win.get_size()
        self.win.blit(self.game_title,
                      (screen_width / 2 - self.game_title.get_width() / 2,
                       screen_height / 4))
        self.blink_text(millisec=500)
        pygame.display.flip()

    def update_angle(self):
        self.angle += (self.ang_vel / FPS)

    def start(self):
        while self.show_start_screen:
            clock.tick(FPS)
            self.update_dt()
            self.update_angle()
            self.update_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.show_start_screen = False
                    self.game_quit = True
                    break

                if event.type == pygame.KEYDOWN:
                    self.show_start_screen = False
                    self.game_quit = False
                    break

        if self.game_quit:
            return False
        else:
            return True
