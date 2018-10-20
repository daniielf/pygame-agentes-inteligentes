import os
import pygame
from pygame.locals import *

def load_image2(image, transparence_type=None, subsurfaces=None):
    try:
        img = pygame.image.load('media' + os.sep + image)
    except:
        print
        'Erro: Nao existe imagem com nome %s no diretorio' % image

    if subsurfaces is None:
        if transparence_type == 1:  # Imagem de fundo transparente
            return img.convert_alpha()
        if transparence_type == 2:  # Torna a cor do pixel na posicao (0,0) transparente
            loaded_image = img.convert()
            color = loaded_image.get_at((0, 0))
            loaded_image.set_colorkey(color, RLEACCEL)
            return loaded_image

    else:
        images = []
        for rect in subsurfaces:
            sub = img.subsurface(rect).convert()
            if transparence_type == 2:
                color = img.get_at((0, 0))
                sub.set_colorkey(color, RLEACCEL)
            images.append(sub)

        return images

    return img.convert()


def write_in_screen(text, color, size, pos, bold=True):
    font = pygame.font.SysFont("arial", size, bold=bold)
    #screen.blit(font.render(text, True, color), pos)