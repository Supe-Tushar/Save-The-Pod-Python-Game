"""
Author: Tushar Supe
Game: Pygame-Save The Pod
FileType: Python file
Details: This python file containts Main screen class template. (Its a Game Menu)
"""

# -----------------------------------------  IMPORTS  -------------------------------------------

from .constants import *


# -----------------------------------------  Main Screen Class  -------------------------------------------
class Option:
    def __init__(self, win):
        self.menu_title = menu_title_font.render("Options", True, (81, 255, 17))
        self.menu_content_font = menu_content_font
        self.general_text_font = general_text_font
        self.win = win
        self.SHUTTLE = scale_image(SHUTTLE, factor=0.8)
        self.show_option_screen = True
        self.game_quit = False
        self.menu_contents = ['Gravity', 'Fuel', 'Sound', 'Music']
        self.menu_content_pos_x = self.win.get_width() / 2 - 50
        self.menu_content_pos_y = [300 + (50 * i) for i in range(len(self.menu_contents))]
        self.current_option_id = 0
        self.shuttle_pos_x, self.shuttle_pos_y = 0, 0
        self.update_shuttle_position()
        self.dt = 0
        self.prev_time = pygame.time.get_ticks()
        self.curr_time = 0
        self.menu_contents_values = []
        config = load_config()
        if config:
            for cont in self.menu_contents:
                self.menu_contents_values.append("ON" if config[cont.lower()] == 1 else "OFF")
        self.play_sound, self.play_music, _, _ = load_current_config_constants()

    def update_shuttle_position(self):
        self.shuttle_pos_x = (self.win.get_width() / 2) - self.SHUTTLE.get_width() - 70
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

            general_text = self.general_text_font.render("Press ENTER to change value & BACKSPACE to go back",
                                                         True, (81, 255, 17))
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
        for i in range(len(self.menu_contents)):
            content = self.menu_contents[i]
            value = self.menu_contents_values[i]
            self.win.blit(self.menu_content_font.render(f"{content} : {value}", True, (81, 255, 17)),
                          (self.menu_content_pos_x, self.menu_content_pos_y[i]))
        pygame.display.flip()

    def start(self):
        while self.show_option_screen:
            clock.tick(FPS)
            self.update_dt()
            self.update_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.show_option_screen = False
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
                        # change value

                        if self.play_sound: pygame.mixer.Sound.play(VALUE_CHANGE_SOUND)
                        if self.menu_contents_values[self.current_option_id] == "ON":
                            self.menu_contents_values[self.current_option_id] = "OFF"
                            config = load_config()
                            if config:
                                config[self.menu_contents[self.current_option_id].lower()] = 0
                                save_config(config)

                        else:
                            self.menu_contents_values[self.current_option_id] = "ON"
                            config = load_config()
                            if config:
                                config[self.menu_contents[self.current_option_id].lower()] = 1
                                save_config(config)
                        self.play_sound, self.play_music, _, _ = load_current_config_constants()
                        if self.play_music:
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(MUSIC_VOLUME)
                        else:
                            pygame.mixer.music.stop()


                    if event.key == pygame.K_BACKSPACE:
                        self.show_option_screen = False


        if self.game_quit:
            return False
        else:
            return True
