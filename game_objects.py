from components import TransformComponent
import pygame


class GameObject:
    def __init__(self, name='NewObject'):
        self.name = name
        self.components = []

    def get_component(self, type):
        for component in self.components:
            if isinstance(component, type):
                return component

    def get_components(self, type):
        return list(filter(lambda comp: isinstance(comp, type), self.components))

    def update(self):
        for component in self.components:
            component.update()


class Sprite(GameObject):
    def __init__(self, sprite_filename, name='NewSprite'):
        super().__init__(name)
        self.image = load_image(sprite_filename)


class Camera:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.surface = pygame.display.get_surface()

    def move(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y

    def update(self):
        self.surface.fill((0, 0, 0))

    def draw(self, game_object):
        surface = game_object.image
        obj_x, obj_y = game_object.get_component(TransformComponent).coord
        rect = surface.get_rect(centerx=obj_x - self.x, centery=self.y - obj_y)
        self.surface.blit(surface, rect)


def load_image(filename):
    return pygame.image.load(filename).convert_alpha()
