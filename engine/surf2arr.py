import pygame
import numpy as np


def surf2nparr(surface, format):
    arr = np.array(bytearray(pygame.image.tostring(surface, format)), dtype=int)
    return arr.reshape(surface.get_rect().size + ({'RGBA': 4, 'RGB': 3}.get(format),))
