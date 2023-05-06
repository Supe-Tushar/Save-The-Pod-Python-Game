"""
Author: Tushar Supe
Game: Pygame-Save The Pod
FileType: Python file
Details: This python file containts Levels screen class template.
"""

# -----------------------------------------  IMPORTS  -------------------------------------------
from .game_screen import Game
from .constants import *


# -----------------------------------------  Main Screen Class  -------------------------------------------


class Level:
    def __init__(self, win):
        self.win = win
        self.menu_title_font = menu_title_font
        self.menu_content_font = menu_content_font
        self.help_content_font = help_content_font
        self.general_text_font = general_text_font
        self.menu_title = menu_title_font.render("Levels", True, (81, 255, 17))

        self.show_level_screen = True
        self.game_quit = False
        self.dt = 0
        self.prev_time = pygame.time.get_ticks()
        self.curr_time = 0
        self.levels = []

        self.current_level_id = 0
        self.load_levels()
        self.play_sound, self.play_music, _, _ = load_current_config_constants()

    def load_levels(self):
        self.levels = []
        game_info = load_game_info()
        hori_max_num = 4
        width = 130  # fixed width. Dont change
        gap = (self.win.get_width() - (hori_max_num * width)) / (hori_max_num + 1)
        if game_info:
            count = 0
            j = 0
            i = 0
            for level in game_info["levels"]:
                level_box = LevelBox(self.win, level_id=level["id"], score=level["score"],
                                     pos_x=(i * width + (i + 1) * gap), pos_y=(j * width + (j + 1) * gap + 100))

                count += 1
                i += 1
                if count >= hori_max_num:
                    count = 0
                    j += 1
                    i = 0
                self.levels.append(level_box)
            self.levels[self.current_level_id].is_selected = True

    def blit_level_text(self):
        for level in self.levels:
            level.draw()

    def update_dt(self):
        self.curr_time = pygame.time.get_ticks()
        self.dt += self.curr_time - self.prev_time
        self.prev_time = self.curr_time

    def blink_text(self, millisec=1000):
        if self.dt > millisec:
            general_text = self.general_text_font.render("Use arrow keys to move, press ENTER to select and BACKSPACE "
                                                         "to go back",
                                                         True, (81, 255, 17))
            self.win.blit(general_text,
                          (self.win.get_width() / 2 - general_text.get_width() / 2,
                           self.menu_title.get_height() + 10))
        if self.dt > millisec * 2:
            self.dt = 0

    def update_screen(self):
        draw(self.win, [(SPACE, (0, 0))], update=False)

        self.win.blit(self.menu_title,
                      (self.win.get_width() / 2 - self.menu_title.get_width() / 2, 10))

        self.blink_text(millisec=1000)
        self.blit_level_text()
        pygame.display.flip()

    def start(self):
        while self.show_level_screen:
            clock.tick(FPS)
            self.update_dt()
            self.update_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.show_level_screen = False
                    self.game_quit = True
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if self.play_sound: pygame.mixer.Sound.play(VALUE_CHANGE_SOUND)
                        self.show_level_screen = False
                        self.game_quit = False
                        break

                    if event.key == pygame.K_LEFT:
                        if self.play_sound: pygame.mixer.Sound.play(TAB_CHANGE_SOUND)
                        self.current_level_id = max(0, self.current_level_id - 1)
                        self.levels[self.current_level_id+1].is_selected = False
                        self.levels[self.current_level_id].is_selected = True

                    if event.key == pygame.K_RIGHT:
                        if self.play_sound: pygame.mixer.Sound.play(TAB_CHANGE_SOUND)
                        self.current_level_id = min(len(self.levels)-1, self.current_level_id + 1)
                        self.levels[self.current_level_id-1].is_selected = False
                        self.levels[self.current_level_id].is_selected = True

                    if event.key == pygame.K_KP_ENTER:
                        # if self.current_level_id == 2:  # Help
                        if self.play_sound: pygame.mixer.Sound.play(VALUE_CHANGE_SOUND)
                        SOUND_ON, MUSIC_ON, GRAVITY_ON, FUEL_ON = load_current_config_constants()
                        game_screen = Game(self.win, level=self.current_level_id, gravity=GRAVITY_ON, fuel=FUEL_ON)
                        if not game_screen.start():
                            self.show_level_screen = False
                            self.game_quit = True
                            break
                        else:
                            self.load_levels()
                            self.update_screen()


        if self.game_quit:
            return False
        else:
            return True


class LevelBox:
    """ pos_x, pos_y are starting position of rectangle """

    def __init__(self, win, level_id=1, score=0, pos_x=0, pos_y=0):
        self.win = win
        self.level_id = level_id
        self.score = score
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.is_selected = False
        self.width = 130
        self.height = self.width
        self.SHUTTLE = scale_image(SHUTTLE, factor=1)

    def draw(self):
        pygame.draw.rect(self.win, color=WHITE,
                         rect=(self.pos_x, self.pos_y, self.width, self.height),
                         width=2, border_radius=5)

        self.win.blit(menu_title_font.render(str(self.level_id), True, (81, 255, 17)),
                      (self.pos_x + self.width / 3, self.pos_y + self.width / 8))
        self.win.blit(help_content_font.render("Score:", True, (81, 255, 17)),
                      (self.pos_x + 5, self.pos_y + 70))
        self.win.blit(help_content_font.render(f"    {self.score}", True, (81, 255, 17)),
                      (self.pos_x + 5, self.pos_y + 100))
        if self.is_selected:
            self.win.blit(self.SHUTTLE, (self.pos_x + 65, self.pos_y + 65))
