"""
Author: Tushar Supe
Game: Pygame-Save The Pod
FileType: Python file
Details: This python file containts Main screen class template. (Its a Game Menu)
"""

# -----------------------------------------  IMPORTS  -------------------------------------------

from .help_screen import Help
from .constants import *
from .level_screen import Level
from .option_screen import Option


# -----------------------------------------  Main Screen Class  -------------------------------------------
class Menu:
    def __init__(self, win):
        self.menu_title = menu_title_font.render("Menu", True, (81, 255, 17))
        self.menu_content_font = menu_content_font
        self.general_text_font = general_text_font
        self.win = win
        self.SHUTTLE = scale_image(SHUTTLE, factor=0.8)
        self.show_menu_screen = True
        self.game_quit = False
        self.menu_contents = ['Levels', 'Options', 'Help', 'Exit']
        self.menu_content_pos_x = self.win.get_width() / 2
        self.menu_content_pos_y = [300 + (50 * i) for i in range(len(self.menu_contents))]
        self.current_option_id = 0
        self.shuttle_pos_x, self.shuttle_pos_y = 0, 0
        self.update_shuttle_position()
        self.dt = 0
        self.prev_time = pygame.time.get_ticks()
        self.curr_time = 0
        self.play_sound, self.play_music, _, _ = load_current_config_constants()

    def update_shuttle_position(self):
        self.shuttle_pos_x = (self.win.get_width() / 2) - self.SHUTTLE.get_width() - 20
        self.shuttle_pos_y = (self.menu_content_pos_y[self.current_option_id]) - (self.SHUTTLE.get_width() / 2) + 10

    def update_dt(self):
        self.curr_time = pygame.time.get_ticks()
        self.dt += self.curr_time - self.prev_time
        self.prev_time = self.curr_time

    def blink_text(self, millisec=1000):
        if self.dt > millisec:
            general_text = self.general_text_font.render("Use keyboard arrow keys to move UP or DOWN",
                                                         True, (81, 255, 17))
            self.win.blit(general_text,
                          (self.win.get_width() / 2 - general_text.get_width() / 2,
                           self.win.get_height() / 4 + self.menu_title.get_height() / 2))

            general_text = self.general_text_font.render("Press ENTER to Select", True, (81, 255, 17))
            self.win.blit(general_text,
                          (self.win.get_width() / 2 - general_text.get_width() / 2,
                           self.win.get_height() / 4 + self.menu_title.get_height()))
        if self.dt > millisec * 2:
            self.dt = 0

    def update_screen(self):
        draw(self.win, [(SPACE, (0, 0))], update=False)
        rotate_image_center(self.win,
                            self.SHUTTLE,
                            top_left=(self.shuttle_pos_x, self.shuttle_pos_y),
                            angle=-90)
        self.win.blit(self.menu_title,
                      (self.win.get_width() / 2 - self.menu_title.get_width() / 2,
                       self.win.get_height() / 4 - self.menu_title.get_height()))
        self.blink_text(millisec=500)
        for i, content in enumerate(self.menu_contents):
            self.win.blit(self.menu_content_font.render(content, True, (81, 255, 17)),
                          (self.menu_content_pos_x, self.menu_content_pos_y[i]))
        pygame.display.flip()

    def start(self):
        while self.show_menu_screen:
            clock.tick(FPS)
            self.update_dt()
            self.update_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.show_menu_screen = False
                    self.game_quit = True
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.current_option_id = max(0, self.current_option_id - 1)
                        if self.play_sound: pygame.mixer.Sound.play(TAB_CHANGE_SOUND)
                        self.update_shuttle_position()

                    if event.key == pygame.K_DOWN:
                        self.current_option_id = min(3, self.current_option_id + 1)
                        if self.play_sound: pygame.mixer.Sound.play(TAB_CHANGE_SOUND)
                        self.update_shuttle_position()

                    if event.key == pygame.K_KP_ENTER:
                        if self.play_sound: pygame.mixer.Sound.play(VALUE_CHANGE_SOUND)
                        if self.current_option_id == 3:  # Exit
                            self.show_menu_screen = False
                            self.game_quit = True
                            break

                        if self.current_option_id == 2:  # Help
                            help_screen = Help(WIN)
                            if not help_screen.start():
                                self.show_menu_screen = False
                                self.game_quit = True
                                break


                        if self.current_option_id == 0:  # Levels
                            level_screen = Level(WIN)
                            if not level_screen.start():
                                self.show_menu_screen = False
                                self.game_quit = True
                                break


                        if self.current_option_id == 1:  # Options
                            option_screen = Option(WIN)
                            if not option_screen.start():
                                self.show_menu_screen = False
                                self.game_quit = True
                                break
                            self.play_sound, self.play_music, _, _ = load_current_config_constants()

        if self.game_quit:
            return False
        else:
            return True
