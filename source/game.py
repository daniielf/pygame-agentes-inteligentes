from sys import exit
import pygame
from pygame.locals import *
import os
import fase3.MAIN as main3
from math import *
from random import randint
from functions import *
import time

def main(screen, car_type, level, track):

        class Car:

                def __init__(self, game):
                        self.track = game.track
                        self.x, self.y = game.car_x, game.car_y

                        # Carregando as imagens do carro
                        size_1 = load_image('carros'+str(game.car_type)+'-1.png').get_size()
                        size_2 = load_image('carros'+str(game.car_type)+'-2.png').get_size()
                        
                        self.images = load_image('carros'+str(game.car_type)+'-1.png', 2, [((x,0),(size_1[0]/3,size_1[1]))\
                                                                                for x in xrange(0, size_1[0], size_1[0]/3)])

                        self.images2 = load_image('carros'+str(game.car_type)+'-2.png', 2, [((x,0),(size_2[0]/3,size_2[1]))\
                                                                                for x in xrange(0, size_2[0], size_2[0]/3)])

                        self.map_images = {'carro_normal': (self.images[0], self.images2[0]),\
                                           'carro_freiando': (self.images[1], self.images2[1]),\
                                           'carro_re': (self.images[2], self.images2[2])}
                        if game.track != 3:
                            print game.track - 1
                            self.image = self.map_images['carro_normal'][game.track - 1]
                            print self.image
                            self.rect = self.image.get_rect()
                            self.rect.center = self.x, self.y
                            self.height, self.width = self.rect.height, self.rect.width
                        

                            self.chocks = 0
                            self.chock_up_key = False
                            self.chock_down_key = False
                            self.chock_lado_key = False

                            self.clock = pygame.time.Clock()

                            # Criando as variaveis para a movimentacao do carro

                            self.rotation_angule = 0.
                            self.rotation_direction, self.movement_direction = 0, -1

                            self.car_atributes = {'max_speed': (360, 240, 300), 're_speed': (-100, -70, -90),\
                                                  'rotation': (100, 90, 140), 'accel': (2, 1, 3)}

                            self.movement_speed = 0
                            self.rotation_speed = 0
                            self.max_speed = self.car_atributes['max_speed'][game.car_type - 1]
                            self.max_speed_reward = self.car_atributes['re_speed'][game.car_type - 1]
                            self.max_rotation = self.car_atributes['rotation'][game.car_type - 1]
                            self.accel = self.car_atributes['accel'][game.car_type - 1]

                            self.translacoes = [(0, (- self.height / 2)), ((+ self.width / 2),\
                            (- self.height / 2)), ((- self.width / 2), (- self.height / 2)),\
                            (0, (+ self.height / 2)), ((+ self.width / 2), (+ self.height / 2)),\
                            ((- self.width / 2), (+ self.height / 2)), ((-self.width / 2), (-self.height / 6)),\
                            ((-self.width / 2), (+self.height / 6)), ((+self.width / 2), (-self.height / 6)),\
                                            ((+self.width / 2), (+self.height / 6))]

                            self.points = []

                        self.sound = pygame.mixer.Sound('sounds' + os.sep + 'batida.wav')

                def move(self, pressed_keys):
                        self.rotation_direction = 0

                        if self.movement_speed > 10:
                                if pressed_keys[K_LEFT]:
                                        self.rotation_direction = 0.8
                                elif pressed_keys[K_RIGHT]:
                                        self.rotation_direction = -0.8

                        if self.movement_speed < -10:
                                if pressed_keys[K_LEFT]:
                                        self.rotation_direction = -0.8
                                elif pressed_keys[K_RIGHT]:
                                        self.rotation_direction = 0.8

                def accelerate(self, pressed_keys):
                        if pressed_keys[K_UP]:
                                self.image = self.map_images['carro_normal'][self.track - 1]
                                if 0 <= self.movement_speed < self.max_speed: # Carro se movendo para frente.
                                        self.movement_speed += self.accel
                                        if self.rotation_speed < self.max_rotation:
                                                self.rotation_speed += 5

                                if self.movement_speed < 0:
                                        self.movement_speed += 5
                                        self.rotation_speed = 0

                        if pressed_keys[K_DOWN]:
                                if self.max_speed_reward < self.movement_speed <= 0: # Carro se movendo de re.
                                        self.movement_speed -= self.accel
                                        self.image = self.map_images['carro_re'][self.track - 1]
                                        if self.rotation_speed < self.max_rotation:
                                                self.rotation_speed += 5

                                if self.movement_speed > 0:
                                        self.movement_speed -= 5
                                        self.rotation_speed = 0
                                        self.image = self.map_images['carro_freiando'][self.track - 1]

                        if not pressed_keys[K_UP] and not pressed_keys[K_DOWN]:
                                self.image = self.map_images['carro_normal'][self.track - 1]
                                if self.movement_speed > 0:
                                        self.movement_speed -= 1
                                if self.movement_speed < 0:
                                        self.movement_speed += 1
                                        
                def diminui_velocidade(self):
                        if self.movement_speed > self.max_speed/5:
                                self.movement_speed -= 10 * self.accel
                        if self.max_speed_reward <= self.movement_speed < self.max_speed_reward/2:
                                self.movement_speed += 10 * self.accel

                def rotaciona_imagem(self):
                        # Movomento de rotacao na tela
                        rotationed_car = pygame.transform.rotate(self.image, self.rotation_angule)
                        w, h = rotationed_car.get_size()
                        screen.blit(rotationed_car, (self.x-w/2, self.y-h/2))

                        self.rect = rotationed_car.get_rect()
                        self.rect.center = self.x, self.y

                def rotaciona_ponto(self, ponto):
                        novo_x = ponto[0] * (cos(self.rotation_angule * pi/180))\
                        - ponto[1] * (-sin(self.rotation_angule * pi/180)) + self.x

                        novo_y = ponto[0] * (-sin(self.rotation_angule * pi/180))\
                        + ponto[1] * (cos(self.rotation_angule * pi/180)) + self.y

                        return novo_x, novo_y

                def reinit_speed(self):
                        self.movement_speed = 0
                        self.rotation_speed = 0

                def clocked_movementation(self, fps):
                        time_passed = self.clock.tick(fps)
                        seconds = time_passed / 1000.0
                        # Movimento em pixels
                        return  self.rotation_speed*seconds, self.movement_speed*seconds

                def collide_screen(self, resolution):
                        if self.x <= self.width / 2:
                                self.x = (self.width / 2 )
                                self.reinit_speed()

                        if self.x >= resolution[0] - self.width / 2:
                                self.x = (resolution[0] - self.width / 2)
                                self.reinit_speed()

                        if self.y <= self.height / 2:
                                self.y = (self.height / 2)
                                self.reinit_speed()

                        if self.y >= resolution[1] - self.height / 2:
                                self.y = (resolution[1] - self.height / 2)
                                self.reinit_speed()

                def collid(self, other, type = None):
                        self.points = []
                        for point in self.translacoes:
                                self.points.append(self.rotaciona_ponto(point))

                        if type == 'car':
                                if other.rect.collidepoint(self.points[0]) or other.rect.collidepoint(self.points[1])\
                                   or other.rect.collidepoint(self.points[2]):
                                        if not self.chock_up_key:
                                                self.movement_speed = -(self.max_speed/8 + self.movement_speed/5)
                                                self.chocks += 1
                                                car.sound.play()
                                                self.chock_up_key = True
                                                self.chock_down_key = False

                                elif other.rect.collidepoint(self.points[3]) or other.rect.collidepoint(self.points[4])\
                                   or other.rect.collidepoint(self.points[5]):
                                        if not self.chock_down_key:
                                                self.movement_speed = self.max_speed/8 - self.movement_speed/5
                                                self.chocks += 1
                                                car.sound.play()
                                                self.chock_down_key = True
                                                self.chock_up_key = False

                                elif self.chock_up_key and -5 <= self.movement_speed <= 5:
                                        self.chock_up_key = False

                                elif self.chock_down_key and -5 <= self.movement_speed <= 5:
                                        self.chock_down_key = False

                        if type == 'cone':
                                if other.rect.collidepoint(self.points[0]) or other.rect.collidepoint(self.points[1])\
                                   or other.rect.collidepoint(self.points[2]):
                                        if not self.chock_up_key:
                                                self.movement_speed = (self.max_speed/8 + self.movement_speed/4)
                                                self.chocks += 1
                                                car.sound.play()
                                                self.chock_up_key = True
                                                self.chock_down_key = False
                                                other.varia_x = -self.movement_speed * 0.1 * sin(self.rotation_angule * pi/180)#15
                                                other.varia_y = -self.movement_speed * 0.1 * cos(self.rotation_angule * pi/180)
                                                other.muda_imagem()

                                elif other.rect.collidepoint(self.points[3]) or other.rect.collidepoint(self.points[4])\
                                   or other.rect.collidepoint(self.points[5]):
                                        if not self.chock_down_key:
                                                self.movement_speed = -self.max_speed/8 + self.movement_speed/2
                                                self.chocks += 1
                                                car.sound.play()
                                                self.chock_down_key = True
                                                self.chock_up_key = False
                                                other.varia_x = -self.movement_speed * 0.1 * sin(self.rotation_angule * pi/180)
                                                other.varia_y = -self.movement_speed * 0.1 * cos(self.rotation_angule * pi/180)
                                                other.muda_imagem()

                                elif not (other.rect.collidepoint(self.points[0]) or other.rect.collidepoint(self.points[1])\
                                   or other.rect.collidepoint(self.points[2])):
                                        self.chock_up_key = False

                                elif (other.rect.collidepoint(self.points[3]) or other.rect.collidepoint(self.points[4])\
                                   or other.rect.collidepoint(self.points[5])):
                                        self.chock_down_key = False
                                
                                #pygame.mixer.misuc.load("nomedamusa.mp3")
                                #pyagme.mixer.music.play()

        class OtherCar:

                def __init__(self, x, y, image):
                        self.image = load_image(image, 2)
                        self.rect = self.image.get_rect()
                        self.rect.center = x, y

        class Cone:

                def __init__(self, pos):
                        self.images = load_image('cone.png', 2, [((x,0),(32,32))\
                                                    for x in xrange(0, 96, 32)])
                        self.image = self.images[0]
                        self.rect = self.image.get_rect()
                        self.rect.center = pos[0], pos[1]
                        self.time_collision = None
                        self.varia_x = 0
                        self.varia_y = 0

                def varia_pos(self):
                        self.rect.center = self.rect.center[0] + self.varia_x, self.rect.center[1] + self.varia_y
                        if self.varia_x > 0:
                                self.varia_x -= 0.2
                        if self.varia_x < 0:
                                self.varia_x += 0.2
                        if self.varia_y > 0:
                                self.varia_y -= 0.2
                        if self.varia_y < 0:
                                self.varia_y += 0.2

                def muda_imagem(self):
                        if self.varia_x > 5 or self.varia_y < -10:
                                self.image = self.images[1]
                        if self.varia_x < -5 or self.varia_y > 10:
                                self.image = self.images[2]

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
                        write_in_screen(text, (255, 255, 255), 20, (10, 10))

        class Semaforo:

                def __init__(self, seconds):
                        self.images = load_image('semaforo.png', 2, [((x,0),(94,140))\
                                                        for x in xrange(0, 188, 94)])
                        self.image = self.images[0]
                        self.pos = (400, 380)
                        
                        self.chron = Chronometer()
                        self.chron.start(seconds + 1.5)
                        self.chron.set_time()
                        self.finished = False
                        self.opened = False
                        self.closed = True;

                def abre_semaforo(self):
                        self.chron.run()
                        if self.chron.seconds < 1.5:
                                self.opened = True
                                self.closed = False
                                self.image = self.images[1]
                        if self.chron.seconds == 0.0:
                                self.finished = True

                def show(self):
                        if not self.finished:
                                screen.blit(self.image, self.pos)

        class Game:

                def __init__(self):
                        self.image = None
                        self.track_map = None
                        self.track = 0
                        self.obstacles = []
                        self.time = 0.0
                        self.chronometer = Chronometer()
                        self.car_type = None
                        self.level = None


                        # Mapas para os obstaculos de acordo com o nivel do jogo

                        self.map_time = {1: (40.0, 60), 2: (30.0, 50), 3: (20.0, 40)}
                        self.parking1_size_map = {1: (553, 283, 100, 180), 2: (555, 283, 95, 180), 3: (557, 283, 90, 180)}
                        self.cars_y = {1: (170, 620), 2: (175, 615), 3: (185, 605)}

                        self.obstaclesx_pos = {1: [(x, 210) for x in xrange(370, 671, 150)],\
                                               2: [(x, 210) for x in xrange(370, 671, 75)],\
                                               3: [(x, 210) for x in xrange(370, 671, 50)]}

                        self.obstaclesy_pos = {1: [(365, y) for y in xrange(410, 731, 150)],\
                                               2: [(365, y) for y in xrange(395, 731, 83)],\
                                               3: [(365, y) for y in xrange(390, 731, 56)]}
                        
                        self.parked = False
                        self.in_check_point = False
                        self.in_ladeira = False

                def track_01(self):
                        self.track = 1
                        self.car_x, self.car_y = 450, 650
                        self.image = load_image('tela_testes.bmp')
                        obstacle1 = OtherCar(600, self.cars_y[self.level][0], 'carro_obstaculo.png')
                        obstacle2 = OtherCar(600, self.cars_y[self.level][1], 'carreta.png')
                        self.parking = Rect(self.parking1_size_map[self.level])
                        self.obstacles.append(obstacle1)
                        self.obstacles.append(obstacle2)
                        self.time = self.map_time[self.level][0]
                        self.chronometer.start(self.time)
                        self.semaforo = Semaforo(3)



                def track_02(self):
                        self.track = 2
                        self.car_x, self.car_y = 240, 705
                        self.image = load_image('tela2_teste.bmp')
                        self.track_map = load_image('mapa_tela2.bmp')
                        self.obstacles = []
                        self.parking = Rect(180, 55, 70, 130)
                        obstacle1 = Cone((205, 220))
                        obstacle2 = Cone((205, 20))
                        obstacle3 = Cone((500, 365))
                        obstacle4 = Cone((580, 640))
                        obstacle5 = Cone((640, 395))
                        obstacle6 = Cone((640, 615))
                        
                        for pos in self.obstaclesx_pos[self.level]:
                                obst = Cone(pos)
                                self.obstacles.append(obst)
                                
                        for pos in self.obstaclesy_pos[self.level]:
                                obst = Cone(pos)
                                self.obstacles.append(obst)
                                
                        self.obstacles.append(obstacle1)
                        self.obstacles.append(obstacle2)
                        self.obstacles.append(obstacle3)
                        self.obstacles.append(obstacle4)
                        self.obstacles.append(obstacle5)
                        self.obstacles.append(obstacle6)
                        self.check_point1 = False
                        self.check_point2 = False
                        self.check_point3 = False
                        self.parked = False
                        self.time = self.map_time[self.level][1]
                        self.chronometer.start(self.time)
                        self.semaforo = Semaforo(3)
                        self.semaforo.pos = (200, 380)
                        self.semaforo2 = Semaforo(3)

                def track_03(self):
                        self.track = 3


                def shift_track(self):
                        if self.track == 1:
                                self.track_02()
                                return True
                        if self.track == 2:
                                self.track_03()
                                return True
                        if self.track == 3:
                                return False
                        
                def box(self, car, status = None):
                        mouse_pos = pygame.mouse.get_pos()

                        tempo_decorrido = self.time - self.chronometer.seconds
                        tempo_descontado = 2 * car.chocks
                        tempo_final = self.time - (self.chronometer.seconds - 2 * car.chocks)

                        if status == 'win':
                                botaozinho_image = load_image('continuar.bmp',2)
                                botaozinho_rect = botaozinho_image.get_rect()
                                botaozinho_rect.center = 525, 330
                                screen.blit(load_image('venceu.bmp'), (200, 150))
                                screen.blit(botaozinho_image, (botaozinho_rect.center))
                                write_in_screen('%1.2f' % tempo_decorrido, (0, 0, 0), 20, (400,215))
                                write_in_screen('%d' % tempo_descontado, (220, 0, 0), 20, (400, 250))
                                write_in_screen('%1.2f' % tempo_final, (0, 150, 0), 25, (400, 280))

                                if botaozinho_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                                        fase = self.shift_track()
                                        return fase
                                return

                        if status == 'lose':
                                lose_list = load_image('perdeu1.bmp', 1, [((x,0),(384,237))\
                                                        for x in xrange(0, 1152, 384)])
                                image = lose_list[0]
                                if 218 <= mouse_pos[0] <= 392 and 352 <= mouse_pos[1] <= 368:
                                        image = lose_list[1]
                                        if pygame.mouse.get_pressed()[0]:
                                                main(screen, car_type, level)
                                        
                                elif 425 <= mouse_pos[0] <= 570 and 352 <= mouse_pos[1] <= 368:
                                        image = lose_list[2]
                                        if pygame.mouse.get_pressed()[0]:
                                                return False

                                screen.blit(image, (200, 150))
                                write_in_screen('%1.2f' % tempo_decorrido, (0, 0, 0), 20, (400,215))
                                write_in_screen('%d' % tempo_descontado, (220, 0, 0), 20, (400, 250))
                                write_in_screen('%1.2f' % tempo_final, (0, 150, 0), 25, (400, 280))

                def game(self, car, pressed_keys):
                        if self.track == 1:
                                for object in self.obstacles:
                                        screen.blit(object.image, (object.rect.x, object.rect.y))
                                        car.collid(object, 'car')

                                tempo_decorrido = self.time - self.chronometer.seconds
                                tempo_descontado = 2 * car.chocks
                                tempo_final = self.time - (self.chronometer.seconds - 2 * car.chocks)
                
                                if self.chronometer.seconds - 2 * car.chocks > 0:
                                        if game.parking.contains(car.rect) and car.movement_speed == 0\
                                           and not pressed_keys[K_UP] and not pressed_keys[K_DOWN]:
                                                self.parked = True
                                        if self.parked:
                                                car.movement_direction, car.rotation_direction = 0, 0
                                                self.chronometer.stop = True
                                                box = self.box(car, 'win')
                                                return box

                                else:
                                        self.chronometer.stop = True
                                        car.movement_direction, car.rotation_direction = 0, 0
                                        return self.box(car, 'lose')

                        if self.track == 2:
                                for object in self.obstacles:
                                        screen.blit(object.image, (object.rect.x, object.rect.y))
                                        car.collid(object, 'cone')
                                        object.varia_pos()

                                tempo_decorrido = self.time - self.chronometer.seconds
                                tempo_descontado = 2 * car.chocks
                                tempo_final = self.time - (self.chronometer.seconds - 2 * car.chocks)

                                
                                if self.track_map.get_at((int(car.x), int(car.y))) == (0, 255, 0, 255):
                                        car.diminui_velocidade()

                                if self.track_map.get_at((int(car.x), int(car.y))) == (255, 0, 0, 255):
                                        if not (sin(car.rotation_angule * pi/180) <= 0.85 and -0.5 <= cos(car.rotation_angule * pi/180) <= 0.5):
                                                #print sin(car.rotation_angule * pi/180), cos(car.rotation_angule * pi/180)
                                                car.y += 0.5
                                                self.in_ladeira = True

                                if self.track_map.get_at((int(car.x), int(car.y))) == (0, 0, 255, 255):
                                        car.y -= 0.5

                                if not self.in_check_point:
                                        if self.track_map.get_at((int(car.x), int(car.y))) == (0, 255, 255, 255):
                                                self.in_check_point = True
                                                self.check_point1 = not self.check_point1

                                        if self.track_map.get_at((int(car.x), int(car.y))) == (255, 255, 0, 255):
                                                self.in_check_point = True
                                                self.check_point2 = not self.check_point2

                                        if self.track_map.get_at((int(car.x), int(car.y))) == (255, 255, 255, 255):
                                                self.in_check_point = True
                                                self.check_point3 = not self.check_point3

                                if self.track_map.get_at((int(car.x), int(car.y))) != (0, 255, 255, 255)\
                                and self.track_map.get_at((int(car.x), int(car.y))) != (255, 255, 0, 255)\
                                and self.track_map.get_at((int(car.x), int(car.y))) != (255, 255, 255, 255):
                                        self.in_check_point = False

                                if self.chronometer.seconds - 2 * car.chocks > 0:
                                        if (self.check_point1 and self.check_point2 and self.check_point3 and self.in_ladeira)\
                                           and self.parking.contains(car.rect) and car.movement_speed == 0\
                                           and not pressed_keys[K_UP] and not pressed_keys[K_DOWN]:
                                                self.parked = True
                                        if self.parked:
                                                self.chronometer.stop = True
                                                car.movement_direction, car.rotation_direction = 0, 0
                                                box = self.box(car, 'win')
                                                return box

                                else:
                                        self.chronometer.stop = True
                                        car.movement_direction, car.rotation_direction = 0, 0
                                        return self.box(car, 'lose')
                        if self.track == 3:
                            print 'passou'
                            running = False
                            main3.main()




        def write_in_screen(text, color, size, pos, bold = True):
                font = pygame.font.SysFont("arial", size, bold = bold)
                screen.blit(font.render(text, True, color), pos)
        
        # Iniciando o corpo do jogo

        width, height = 1024, 768
        resolution = (width, height)

        #pygame.mixer.music.load('sounds' + os.sep + 'game_music.mp3')
        #pygame.mixer.music.play()

        # Instanciando os objetos do jogo
        game = Game()
        game.car_type = car_type
        game.level = level
        if (track == 1):
                game.track_01()
        if (track == 2):
                game.track_02()
        if (track == 3):
                main3.main()
        
        car = Car(game)

        fullscreen = False
        running = True

        while running:

                for event in pygame.event.get():
                        if event.type == QUIT:
                                exit()

                        if event.type == KEYDOWN:
                                if event.key == K_f:
                                        Fullscreen = not Fullscreen
                                        if Fullscreen:
                                                screen = pygame.display.set_mode(resolution, FULLSCREEN, 32)
                                        else:
                                                screen = pygame.display.set_mode(resolution, 0, 32)

                screen.blit(game.image, (0, 0))
                car.rotaciona_imagem()

                # Recebendo entradas de acessorios externos
                pressed_keys = pygame.key.get_pressed()

                if pressed_keys[K_ESCAPE]:
                        return False

                if pressed_keys[K_LALT] and pressed_keys[K_RETURN]:
                        fullscreen = not fullscreen

                        if fullscreen: screen = pygame.display.set_mode((1024,768), FULLSCREEN, 32)
                        else: screen = pygame.display.set_mode((1024,768), 0, 32)

                
                game.semaforo.abre_semaforo()
                game.semaforo.show()


                if randint(0,50) == 5 and game.track == 2:
                    game.semaforo2.pos = (200, 380)
                    game.semaforo2.abre_semaforo()
                    game.semaforo2.show()
                    write_in_screen('Entrou: %d' % car.chocks, (255, 0, 0), 20, (10, 70))


                if game.semaforo.opened:
                        game.chronometer.set_time()
                        game.chronometer.run()
                        # Movimentando o carro
                        car.move(pressed_keys)
                        car.accelerate(pressed_keys)

                if game.semaforo.closed:
                    if pressed_keys[pygame.K_UP]:
                        car.chocks += 0.03


                game.chronometer.show()
                write_in_screen('Batidas: %d' % car.chocks, (255, 255, 255), 20, (10, 30))
                write_in_screen('Tentativa de Avancar Sinal Vermelho:Tempo Descontado =  %d segundos' % car.chocks,
                                (255, 255, 255), 20, (10, 50))

                #if movement_direction != 0:
                    #car.sound.play()
                
                rotation, movement = car.clocked_movementation(120)

                car.collide_screen(resolution)


                if game.game(car, pressed_keys) == True:
                        car = Car(game)
                if game.game(car, pressed_keys) == False:
                        return False

                # Variacao no eixo do movimento
                car.rotation_angule += car.rotation_direction * rotation

                x1 = sin(car.rotation_angule * pi / 180) * car.movement_direction
                y1 = cos(car.rotation_angule * pi / 180) * car.movement_direction
                car.x += x1 * movement
                car.y += y1 * movement
                mouse = pygame.mouse.get_pos()
                print mouse

                pygame.display.flip()


