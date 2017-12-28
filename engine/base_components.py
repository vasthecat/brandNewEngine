import pygame


class Component:
    def __init__(self, game_object):
        self.game_object = game_object

    def update(self, *args):
        pass


class TransformComponent(Component):
    def __init__(self, x, y, game_object):
        super().__init__(game_object)
        self.x, self.y = self.coord = x, y
        self.rotation = 0

    def move_to(self, x, y):
        self.x, self.y = self.coord = x, y

    def move(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y
        self.coord = self.x, self.y

    def rotate(self, degree):
        self.rotation += degree

    def set_rotation(self, degree):
        self.rotation = degree


class ImageComponent(Component):
    def __init__(self, image_path, game_object):
        super().__init__(game_object)
        self.image = ImageComponent.load_image(image_path)

    @staticmethod
    def load_image(filename):
        return pygame.image.load(filename).convert_alpha()
