"""
Author: Tushar Supe
Game: Pygame-Save The Pod
FileType: Python file
Details: This python file contains all classes required for Main Game screen (Shuttle, Asteroid).
"""

# -----------------------------------------  IMPORTS  -------------------------------------------

import math
import pygame.time
from .constants import *
from .shuttle import Shuttle
from .planet import Planet
from .star import Star
from .wormhole import Wormhole


# -----------------------------------------  Classes  -------------------------------------------
class Game:
    def __init__(self, win, level=1, gravity=True, fuel=True):
        self.general_text_font = general_text_font
        self.win = win
        self.level = level
        self.gravity = gravity
        self.fuel = fuel
        self.show_game_screen = True
        self.game_quit = False
        self.level_completed = False
        self.fuel_empty = False
        self.stars_collected = 0
        self.shuttle = None
        self.planets = []
        self.stars = []
        self.wormholes = []
        self.load_game()
        self.play_sound, self.play_music, _, _ = load_current_config_constants()


    def load_game(self):
        game_info = load_game_info()
        if game_info:
            params = game_info["levels"][self.level]["params"]
            shuttle = params["shuttle"]
            planets = params["planet"]
            stars = params["star"]
            wormholes = params["wormhole"]

            self.shuttle = Shuttle(self.win, start_x=shuttle["start_pos"][0], start_y=shuttle["start_pos"][1],
                                   use_gravity=self.gravity, use_fuel=self.fuel, use_ang_vel=False)

            for planet in planets:
                self.planets.append(Planet(self.win,
                                           pos_x=planet["start_pos"][0], pos_y=planet["start_pos"][1],
                                           angle=int(planet["angle"]), gravity=self.gravity,
                                           blackhole=True if planet["blackhole"] == 1 else False))
            for star in stars:
                self.stars.append(Star(self.win,
                                       pos_x=star["start_pos"][0], pos_y=star["start_pos"][1],
                                       angle=star["angle"], ang_acc=(star["ang_acc"] / FPS),
                                       direction=star["direction"],
                                       rotate=True if star["rotate"] == 1 else False))

            for wormhole in wormholes:
                self.wormholes.append(Wormhole(self.win,
                                               pos_x=wormhole["start_pos"][0], pos_y=wormhole["start_pos"][1],
                                               angle=wormhole["angle"],
                                               color=wormhole["color"]))



    def update_screen(self):
        draw(self.win, [(SPACE, (0, 0))], update=False)
        string = ""
        string += f"Vx: {round(self.shuttle.vel_x, 2)}".ljust(17, " ")
        string += f"Vy: {round(self.shuttle.vel_y, 2)}".ljust(17, " ")
        string += f"Angle: {round(self.shuttle.angle, 2)}".ljust(17, " ")
        string += f"Score: {self.stars_collected}".ljust(17, " ")
        string += f"Fuel: {round(self.shuttle.fuel, 1)}"
        velocities = self.general_text_font.render(string, True, (81, 255, 17))
        self.win.blit(velocities, (20, 5))

        for planet in self.planets:
            planet.draw()
        for star in self.stars:
            star.draw()
        for wormhole in self.wormholes:
            wormhole.draw()
        self.shuttle.draw()
        pygame.display.update()

    def game_controls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.shuttle.throttle_down()
        if keys[pygame.K_s]:
            self.shuttle.throttle_up()
        if keys[pygame.K_a]:
            self.shuttle.throttle_right()
        if keys[pygame.K_d]:
            self.shuttle.throttle_left()
        if keys[pygame.K_RIGHT]:
            self.shuttle.throttle_cw()
        if keys[pygame.K_LEFT]:
            self.shuttle.throttle_ccw()


    def start(self):

        first_time = True
        skip_frame = 30  # skip user control updates per second
        frame_count = 0
        while self.show_game_screen:
            clock.tick(FPS)
            for planet in self.planets:
                fx, fy, is_collided = planet.attraction_force(self.shuttle.pos_x + self.shuttle.SHUTTLE.get_width() / 2,
                                                              self.shuttle.pos_y + self.shuttle.SHUTTLE.get_height() / 2)
                self.shuttle.gravity_force(fx, fy, is_collided)

            for star in self.stars:
                is_collided = star.collision(self.shuttle.pos_x + self.shuttle.SHUTTLE.get_width() / 2,
                                             self.shuttle.pos_y + self.shuttle.SHUTTLE.get_height() / 2)
                if is_collided:
                    if self.play_sound: pygame.mixer.Sound.play(STAR_SOUND)
                    self.stars_collected += 1
                    star.is_draw = False

            for i in range(len(self.wormholes)):
                wormhole = self.wormholes[i]
                is_collided, dist, dist_angle = wormhole.collision(
                    self.shuttle.pos_x + self.shuttle.SHUTTLE.get_width() / 2,
                    self.shuttle.pos_y + self.shuttle.SHUTTLE.get_height() / 2)
                if is_collided:
                    if self.play_sound: pygame.mixer.Sound.play(WORMHOLE_SOUND)
                    i = 1 if i == 0 else 0
                    self.shuttle.wormhole_teleport(self.wormholes[i].pos_x, self.wormholes[i].pos_y, dist, dist_angle)

            self.update_screen()

            if first_time:
                text = menu_title_font.render(f"Level   -  {self.level+1}", True, (81, 255, 17))
                self.win.blit(text, (self.win.get_width() / 2 - text.get_width() / 2, self.win.get_height() / 2 - text.get_height() / 2))
                pygame.display.update()
                pygame.time.delay(2000)
                first_time = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.show_game_screen = False
                    self.game_quit = True
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.show_game_screen = False

            if self.stars_collected == 3:
                self.show_game_screen = False
                self.level_completed = True

            if self.shuttle.check_fuel() and self.fuel:
                # fuel is empty
                self.fuel_empty = True

            frame_count += 1
            if frame_count > (FPS / skip_frame):
                frame_count = 0
                if self.fuel_empty and self.fuel:
                    text = menu_content_font.render("Fuel Over !!!", True, (81, 255, 17))
                    self.win.blit(text, (self.win.get_width() / 2 - text.get_width() / 2,
                                         self.win.get_height() / 2 - text.get_height() / 2))
                    pygame.display.update()
                else:
                    self.game_controls()





        if self.level_completed:
            self.shuttle.stop()
            if self.play_sound: pygame.mixer.Sound.play(LEVEL_COMPLETE_SOUND)
            text = menu_content_font.render("Level Complete !!!", True, (81, 255, 17))
            self.win.blit(text, (self.win.get_width()/2 - text.get_width()/2, self.win.get_height()/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(3000)
            self.level_completed = False
            # save score
            game_info = load_game_info()
            game_info["levels"][self.level]["score"] = 3
            save_game_info(game_info)
            return True

        if self.game_quit:
            return False
        else:
            return True
