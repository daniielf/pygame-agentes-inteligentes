# The MIT License (MIT)

# Copyright (c) 2012 Robin Duda, (chilimannen)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Camera module will keep track of sprite offset.

import sys

import pygame
from pygame.locals import *

import bounds
import camera
import direction
import gamemode
import leis_transito
import maps
import menu
import player
import timeout
import tracks
import traffic


import time
# Import game modules.
from loader import load_image

CENTER_W = -1
CENTER_H = -1

## AGENTES IMPORT
from agentes3 import aiinstances as AI_INSTANCES
from agentes3 import aiconfig as AI_CONFIG

class Game():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 32)
        self.car = player.Player()
        self.cam = camera.Camera()
        self.target = gamemode.Finish()
        self.bound_alert = bounds.Alert()
        self.time_alert = timeout.Alert()
        self.celular_alert = leis_transito.CelularAlert()
        self.stop_alert = leis_transito.StopAlert()
        self.info = menu.Alert()
        self.pointer = direction.Tracker(int(CENTER_W * 2), int(CENTER_H * 2))

        self.hardmodeOn = False
        self.extraTimeValue = AI_CONFIG._L3_tempo_extra_facil
        self.quantidadeVeiculos = AI_CONFIG._L3_quantidade_veiculos_facil

        # create sprite groups.
        self.map_s = pygame.sprite.Group()
        self.player_s = pygame.sprite.Group()
        self.celular_s = pygame.sprite.Group()
        self.stop_s = pygame.sprite.Group()
        self.traffic_s = pygame.sprite.Group()
        self.tracks_s = pygame.sprite.Group()
        self.target_s = pygame.sprite.Group()
        self.pointer_s = pygame.sprite.Group()
        self.timer_alert_s = pygame.sprite.Group()
        self.bound_alert_s = pygame.sprite.Group()
        self.menu_alert_s = pygame.sprite.Group()

        self.CENTER_W = int(1024 / 2)
        self.CENTER_H = int(768 / 2)

    # Main function.
    def run(self):

        # generate tiles
        for tile_num in range(0, len(maps.map_tile)):
            maps.map_files.append(load_image(maps.map_tile[tile_num], False))
        for x in range(0, 10):
            for y in range(0, 10):
                self.map_s.add(maps.Map(maps.map_1[x][y], x * 1000, y * 1000, maps.map_1_rot[x][y]))

        # load tracks
        tracks.initialize()
        # load finish
        self.target_s.add(self.target)
        # load direction
        self.pointer_s.add(self.pointer)
        # load alerts
        self.timer_alert_s.add(self.time_alert)
        self.bound_alert_s.add(self.bound_alert)
        self.celular_s.add(self.celular_alert)
        self.stop_s.add(self.stop_alert)

        self.menu_alert_s.add(self.info)
        # load traffic
        traffic.initialize(CENTER_W, CENTER_H)
        for count in range(0, self.quantidadeVeiculos):
            self.traffic_s.add(traffic.Traffic())

        self.player_s.add(self.car)

        self.cam.set_pos(self.car.x, self.car.y)

        while self.running:
            # Render loop.
            # Check for menu/reset, (keyup event - trigger ONCE)
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if keys[K_m]:
                        if (self.info.visibility == True):
                            self.info.visibility = False
                        else:
                            self.info.visibility = True
                    if (keys[K_p]):
                        self.car.reset()
                        self.target.reset()
                    if (keys[K_q]):
                        pygame.quit()
                        sys.exit(0)
                    if (keys[K_z]):  # atende ligacao
                        self.celular_alert.atender = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    from source.menu import Menu as menu2
                    aux = menu2()
                    aux.main_menu()
                    running = False
                    break

            # Check for key input. (KEYDOWN, trigger often)
            keys = pygame.key.get_pressed()
            if (self.target.timeleft > 0):
                if keys[K_LEFT]:
                    self.car.steerleft()
                if keys[K_RIGHT]:
                    self.car.steerright()
                if keys[K_UP]:
                    self.car.accelerate()
                else:
                    self.car.soften()
                if keys[K_DOWN]:
                    self.car.deaccelerate()

                self.cam.set_pos(self.car.x, self.car.y)

            # Show text data.

            text_fps = self.font.render('', 1, (224, 16, 16))
            textpos_fps = text_fps.get_rect(centery=25, centerx=60)

            text_score = self.font.render('Pontuacao: ' + str(self.target.score), 1, (224, 16, 16))
            textpos_score = text_fps.get_rect(centery=45, centerx=60)

            text_timer = self.font.render(
                'Tempo: ' + str(int((self.target.timeleft / 60) / 60)) + ":" + str(int((self.target.timeleft / 60) % 60)), 1,
                (224, 16, 16))
            textpos_timer = text_fps.get_rect(centery=65, centerx=60)

            # Render Scene.
            self.screen.blit(self.background, (0, 0))

            # cam.set_pos(car.x, car.y)

            self.map_s.update(self.cam.x, self.cam.y)
            self.map_s.draw(self.screen)

            # Conditional renders/effects
            self.car.grass(self.screen.get_at(((int(self.CENTER_W - 5), int(self.CENTER_H - 5)))).g)
            if self.car.tracks:
                self.tracks_s.add(tracks.Track(self.cam.x + self.CENTER_W, self.cam.y + self.CENTER_H, self.car.dir))

            # Just render..
            self.tracks_s.update(self.cam.x, self.cam.y)
            self.tracks_s.draw(self.screen)

            self.player_s.update(self.cam.x, self.cam.y)
            self.player_s.draw(self.screen)

            self.traffic_s.update(self.cam.x, self.cam.y)
            self.traffic_s.draw(self.screen)

            self.target_s.update(self.cam.x, self.cam.y)
            self.target_s.draw(self.screen)

            self.pointer_s.update(self.car.x + self.CENTER_W, self.car.y + self.CENTER_H, self.target.x, self.target.y)
            self.pointer_s.draw(self.screen)

            # stop_alert.updateTimer(time.time())
            # Conditional renders.
            if (bounds.breaking(self.car.x + self.CENTER_W, self.car.y + self.CENTER_H) == True):
                self.bound_alert_s.update()
                self.bound_alert_s.draw(self.screen)

            if (self.target.timeleft == 0):
                self.timer_alert_s.draw(self.screen)
                self.car.speed = 0
                text_score = self.font.render('Pontuacao Final: ' + str(self.target.score), 1, (224, 16, 16))
                textpos_score = text_fps.get_rect(centery=self.CENTER_H + 56, centerx=self.CENTER_W - 20)

                self.celular_alert.grass(self.screen.get_at(((int(self.CENTER_W - 5), int(self.CENTER_H - 5)))).g, self.car.speed)
            if (int((self.target.timeleft / 60) % 60) % 20 == 0):
                self.celular_alert.visibility = True
                self.celular_alert.startTimer()
            if (self.celular_alert.tocando):
                self.celular_alert.chron.run()

            if (self.target.timeleft > 0 and self.celular_alert.visibility is True):
                self.celular_s.draw(self.screen)
                keys = pygame.key.get_pressed()
                if (keys[K_c] and self.car.speed > 0.4):
                    self.target.score -= 50
                    self.celular_alert.tocando = False
                    self.celular_alert.visibility = False
                if (keys[K_c] and self.car.speed <= 0.4):
                    self.target.score += 200
                    self.celular_alert.tocando = False
                    self.celular_alert.visibility = False
                if (not self.celular_alert.cel_time()):
                    self.target.score -= 100
                    self.celular_alert.tocando = False
                    self.celular_alert.visibility = False

                self.stop_alert.stop_car(self.car.speed)
            if (int((self.target.timeleft / 60) % 60) % 15 == 0 and self.car.speed >= 0.1):
                self.stop_alert.visibility = True

            if (self.target.timeleft > 0 and self.stop_alert.visibility is True):
                self.stop_s.draw(self.screen)
                if (self.car.speed < 0.1):
                    self.target.score += 200
                    self.stop_alert.visibility = False
                else:
                    self.target.score -= 1

            if (self.info.visibility == True):
                self.menu_alert_s.draw(self.screen)

            # Blit Blit..
            pygame.draw.rect(self.screen, (216, 216, 216), [40, 30, 200, 55])
            self.screen.blit(text_fps, textpos_fps)
            self.screen.blit(text_score, textpos_score)
            self.screen.blit(text_timer, textpos_timer)
            pygame.display.flip()

            # Check collision!!!
            if pygame.sprite.spritecollide(self.car, self.traffic_s, False):
                self.car.impact()
                self.target.car_crash()
                self.target.score -= 5

            if pygame.sprite.spritecollide(self.car, self.target_s, True):
                self.target.claim_flag()
                self.target.score += 50
                self.target.generate_finish()
                self.target_s.add(self.target)

            self.clock.tick(64)

    # cria semaforo

    # initialization
        pygame.init()
        print pygame.display.Info().current_w
        print pygame.display.Info().current_h
        '''
        screen = pygame.display.set_mode((pygame.display.Info().current_w,
                                          pygame.display.Info().current_h),
                                          pygame.FULLSCREEN)
        '''
        self.screen = pygame.display.set_mode((1024, 768), pygame.FULLSCREEN)

        pygame.display.set_caption('Race of Math.')
        pygame.mouse.set_visible(True)
        self.font = pygame.font.Font(None, 24)
        # CENTER_W = int(1024 / 2)
        # CENTER_H = int(768 / 2)
        '''
        CENTER_W =  int(pygame.display.Info().current_w /2)
        CENTER_H =  int(pygame.display.Info().current_h /2)
        '''

        # new background surface
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert_alpha()
        self.background.fill((26, 26, 26))

        # Enter the mainloop.
        # main()

        # pygame.quit()
        # sys.exit(0)