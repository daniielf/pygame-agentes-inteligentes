from sys import exit
import pygame
from pygame.locals import *
import os
from math import *
from random import randint
import time
from functions import *
from game import *

pygame.init()

class Menu:
    def __init__(self):
        self.background = load_image('menu_background.bmp')
        #test agora
        self.display_width = 1024
        self.display_height = 768
        self.gameDisplay = pygame.display.set_mode((1024, 768), pygame.FULLSCREEN)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (200, 0, 0)
        self.green = (0, 200, 0)
        self.block_color = (53,115,255)
        self.bright_red = (255, 0, 0)
        self.bright_green = (0, 255, 0)
        self.track_selected = None
        #test agora

        self.game_level = None

        self.car_type = 1

        self.help_buttons = load_image('ajuda.png', 2, [((x,0),(26,118))\
                                             for x in xrange(0, 78, 26)])
        self.help_button = self.help_buttons[0]
        self.help_size = self.help_button.get_size()
        self.help_pos = (678, 40)

        self.exit_buttons = load_image('sair.png', 2, [((x,0),(111,74))\
                                             for x in xrange(0, 333, 111)])
        self.exit_button = self.exit_buttons[0]
        self.exit_size = self.exit_button.get_size()
        self.exit_pos = (228, 125)

        self.back_buttons = load_image('voltar.png', 2, [((0,y),(134,36))\
                                             for y in xrange(0, 108, 36)])
        self.back_button = self.exit_buttons[0]
        self.back_size = self.exit_button.get_size()
        self.back_pos = (50, 720)

        self.pressed = False

        self.fullscreen = True

    def set_fullscreen(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LALT] and pressed_keys[K_RETURN]:
            self.fullscreen = not self.fullscreen

            if self.fullscreen: screen = pygame.display.set_mode((pygame.display.Info().current_w,
                                  pygame.display.Info().current_h),
                                  pygame.FULLSCREEN)
            else: screen = pygame.display.set_mode((1024,768), 0, 32)

    #defs inseridas para teste
    def text_objects(self,text, font):
        textSurface = font.render(text, True, self.black)
        return textSurface, textSurface.get_rect()

    def button(self,msg, x, y, w, h, ic, ac, action=None, action2=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.gameDisplay, ac, (x, y, w, h))

            if click[0] == 1 and action != None:
                action()
            if click[0] == 1 and action2 != None:
                action2()
        else:
            pygame.draw.rect(self.gameDisplay, ic, (x, y, w, h))





        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.gameDisplay.blit(textSurf, textRect)
    #fim defs

    def main_menu(self):
        #pygame.mixer.music.stop()
        #pygame.mixer.music.load('sounds' + os.sep + 'game_music.mp3')
        #pygame.mixer.music.play()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            
            self.set_fullscreen()

            self.gameDisplay.fill(self.white)
            largeText = pygame.font.Font('freesansbold.ttf', 115)
            TextSurf, TextRect = self.text_objects("Test Drive", largeText)
            TextRect.center = ((self.display_width / 2), (self.display_height / 2))
            self.gameDisplay.blit(TextSurf, TextRect)
            # -Novo jogo
            self.button("Novo Jogo", 250, 450, 100, 50, self.green, self.bright_green,self.select_fase)
            self.button("Ajuda", 450, 450, 100, 50, self.green, self.bright_green, self.help_menu)
            self.button("Sair", 650, 450, 100, 50, self.green, self.bright_green, exit)
            pygame.display.update()

    def help_menu(self):
        self.background = load_image('menu_background_2.bmp')
        self.text = load_image('menu_ajuda.bmp', 2)

        while True:
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

            self.set_fullscreen()

            screen.blit(self.background, (0, 0))

            mouse_pos = pygame.mouse.get_pos()
            mouse_press = pygame.mouse.get_pressed()

            if self.back_pos[0] <= mouse_pos[0] <= self.back_pos[0] + self.back_size[0]\
            and self.back_pos[1] <= mouse_pos[1] <= self.back_pos[1] + self.back_size[1]:
                self.back_button = self.back_buttons[1]

                if mouse_press[0]:
                    self.back_button = self.back_buttons[2]
                    self.pressed = True

                if self.pressed and not mouse_press[0]:
                    self.back_button = self.back_buttons[1]
                    return

            else: self.back_button = self.back_buttons[0]

            if not mouse_press[0]:
                self.pressed = False

            screen.blit(self.text, (0, 0))
            screen.blit(self.back_button, self.back_pos)

            pygame.display.flip()


    def select_fase(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.gameDisplay.fill(self.white)
            largeText = pygame.font.Font('freesansbold.ttf', 115)
            TextSurf, TextRect = self.text_objects("Test Drive", largeText)
            TextRect.center = ((self.display_width / 2), (self.display_height / 2))
            self.gameDisplay.blit(TextSurf, TextRect)

            self.button("Baliza", 150, 450, 100, 50, self.green, self.bright_green, self.define_fase(1),self.select_level_menu)
            self.button("Trajeto", 350, 450, 100, 50 , self.green, self.bright_green, self.define_fase(2),self.select_level_menu)
            self.button("Transito", 550, 450, 100, 50, self.green, self.bright_green, self.define_fase(3),self.select_level_menu)
            self.button("Sair", 750, 450, 100, 50, self.green, self.bright_green, exit)

            pygame.display.update()
            #clock.tick(15)

    def define_fase(self,track):
        self.track_selected = track


    def define_nivel(self, dificuldade):
        self.level_selected = dificuldade
        if self.level_selected is not None:
            pygame.mixer.music.stop()
            print 'track:'+  str(self.track_selected)
            if main(screen, self.car_type, self.level_selected, self.track_selected) == False:
                self.main_menu()

    def select_level_menu(self):

        self.level_selected = None

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

            self.set_fullscreen()

            self.gameDisplay.fill(self.white)
            largeText = pygame.font.Font('freesansbold.ttf', 40)
            TextSurf, TextRect = self.text_objects("Selecionar Dificuldade", largeText)
            TextRect.center = ((self.display_width / 2), (self.display_height / 2))
            self.gameDisplay.blit(TextSurf, TextRect)

            # -Novo jogo
            self.button("Facil", 250, 450, 100, 50, self.green, self.bright_green, self.define_nivel(1))
            self.button("Medio", 450, 450, 100, 50, self.green, self.bright_green, self.define_nivel(2))
            self.button("Dificil", 650, 450, 100, 50, self.green, self.bright_green, self.define_nivel(3))
            pygame.display.update()




screen = pygame.display.set_mode((pygame.display.Info().current_w,
                                  pygame.display.Info().current_h),
                                  pygame.FULLSCREEN)

pygame.display.set_caption("Test Drive")


if __name__ == "__main__":
    menu = Menu()
    menu.main_menu()

