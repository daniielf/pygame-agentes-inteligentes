import time

from functions import *
from loader import load_image

CENTER_X = -1
CENTER_Y = -1
NOTE_HALF_X = 211
NOTE_HALF_Y = 112
GRASS_GREEN = 75




class Chronometer:

    def __init__(self):
        self.seconds = 0.0
        self.font = pygame.font.SysFont("arial", 18)
        self.font.set_bold(True)
        self.font_height = self.font.get_linesize()
        self.stop = True
        self.started_now = False

    def start(self, seconds):
        self.seconds = seconds
        self.stop = False
        self.started_now = True

    def set_time(self):
        if self.started_now:
            self.time = time.time()

    def run(self):
        self.started_now = False
        if self.seconds > 0.:
            if self.stop == False:
                new_time = time.time()
                self.seconds -= new_time - self.time
                self.time = new_time

        else:
            self.seconds = 0.0

    def show(self):
        text = 'Tempo: %1.2f' % self.seconds
        #write_in_screen(text, (255, 255, 255), 20, (10, 10))

class Semaforo:

    def __init__(self, seconds):
        self.images = load_image2('semaforo.png', 2, [((x, 0), (94, 140)) \
                                                     for x in xrange(0, 188, 94)])
        self.image = load_image('semaforo.png')
        self.rect = self.image.get_rect()
        #self.image = self.images[0]
        self.pos = (400, 380)
        self.screen = pygame.display.get_surface()
        self.chron = Chronometer()
        self.chron.start(seconds + 1.5)
        self.chron.set_time()
        self.finished = False
        self.opened = False

    def abre_semaforo(self):
        self.chron.run()
        if self.chron.seconds < 2.5:
            self.opened = True
            #self.image = self.images
        if self.chron.seconds == 0.0:
            self.finished = True

    def show(self):
        if not self.finished:
            self.screen.blit(self.image, self.pos)





def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect




class CelularAlert(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('celular.png')
        self.screen = pygame.display.get_surface()
        self.rect = self.image.get_rect()
        self.x = 900
        self.y = 550
        self.rect.topleft = self.x, self.y
        self.chron = Chronometer()
        self.chron.start(10.0)
        self.chron.set_time()
        self.visibility = False
        self.score = True
        self.atender = False

    # Se o carro estiver em cima da grama o contador for maior q zero e pressionar Z  = score+5.
    def grass(self, value, speed):
        a = 0
        # self.chron.start(5.0)
        # self.chron.run()
        # if speed <= 0.02 and self.visibility is True and self.chron.seconds > 0.0:
        #     self.visibility = False
        #     self.atender = False
        #     self.score = True
        #
        #     if self.chron.seconds == 0:
        #         self.score = False
        #         self.visibility = False

    def startTimer(self):
        self.chron.start(10.0)
        self.chron.run()


    def cel_time(self):
        # self.chron.run()
        if self.chron.seconds > 0:
            return True
        else:
            return False

class StopAlert(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('stop.png')
        self.screen = pygame.display.get_surface()
        self.rect = self.image.get_rect()
        self.x = 550
        self.y = 550
        self.rect.topleft = self.x, self.y
        self.chron = Chronometer()

        self.start_time = 0
        self.current_time = 0
        self.startedCount = False

        self.chron.start(15.0)
        self.chron.set_time()
        self.visibility = False
        self.score = True

    # Se o Carro Atingir velocidade 0 score +2
    def stop_car(self, speed):
        # print 'Score:'+str(self.score)
        # print 'Seconds:'+str(self.chron.seconds)
        # print str(self.chron.seconds) + 'time pare'

        self.chron.run()
        if self.chron.seconds == 0.0:
        #     self.visibility = False
            self.score = True
        #
        # if self.chron.seconds == 0.0:
        #     self.score = False
        #     self.visibility = False
        #     self.chron.start(15.0)


    def stop_time(self):
        self.chron.run()
        if self.chron.seconds > 0:
            return True
        else:
            return False