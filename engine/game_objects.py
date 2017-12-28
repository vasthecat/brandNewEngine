from engine.base_components import TransformComponent, ImageComponent
from engine.initialize_engine import width, height
import pygame


class GameObject:
    def __init__(self, x=0, y=0, name='NewObject'):
        self.name = name
        self.components = []
        self.add_component(TransformComponent(x, y, self))
        self.transform = self.get_component(TransformComponent)

    def get_component(self, type):
        for component in self.components:
            if isinstance(component, type):
                return component

    def add_component(self, component):
        self.components.append(component)

    def has_component(self, type):
        return self.get_component(type) is not None

    def get_components(self, type):
        return list(filter(lambda comp: isinstance(comp, type), self.components))

    def update(self):
        for component in self.components:
            component.update()


class Camera(GameObject):
    def __init__(self, x=0, y=0):
        super().__init__(x, y, 'NewCamera')
        self.surface = pygame.display.get_surface()

    def update(self):
        self.surface.fill((0, 0, 0))

    def draw(self, game_object):
        if game_object.has_component(ImageComponent):
            transform = game_object.transform
            cam_transform = self.transform

            image = game_object.get_component(ImageComponent).image
            surface = pygame.transform.rotate(image, cam_transform.rotation + transform.rotation)
            obj_x, obj_y = transform.coord
            x, y = cam_transform.coord

            rect = surface.get_rect(
                centerx=width // 2 + obj_x - x,
                centery=height // 2 + y - obj_y
            )

            self.surface.blit(surface, rect)


def load_image(filename):
    return pygame.image.load(filename).convert_alpha()
