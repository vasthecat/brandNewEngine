import pygame
import sys


class GameObject(pygame.sprite.Sprite):
    def __init__(self, surface):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.rect = surface.get_rect()

    def move_center_to(self, x, y):
        self.rect = self.surface.get_rect(center=(x, y))

    def move(self, x, y):
        self.rect.move_ip(x, y)

    def draw(self, surface):
        surface.blit(self.surface, self.rect)


if __name__ == '__main__':
    BLACK = (0, 0, 0)
    pygame.init()
    w, h = size = 1280, 720
    screen = pygame.display.set_mode(size)

    surf = pygame.Surface(10, 10)
    surf.fill((255, 255, 255))

    obj = GameObject(surf)
    obj.move_center_to(0, 80)

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(BLACK)
        obj.draw(screen)
        pygame.display.flip()
