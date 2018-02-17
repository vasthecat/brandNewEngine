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
        img = self.game_object.get_component(ImageComponent)
        if img is not None:
            img.image = pygame.transform.rotate(img._original, self.rotation)

    def set_rotation(self, degree):
        self.rotation = degree
        img = self.game_object.get_component(ImageComponent)
        if img is not None:
            img.image = pygame.transform.rotate(img._original, self.rotation)


class ImageComponent(Component):
    def __init__(self, image, game_object):
        super().__init__(game_object)
        self._original = image
        self.image = self._original

    @staticmethod
    def load_image(filename):
        return pygame.image.load(filename).convert_alpha()


class ImageFile(ImageComponent):
    def __init__(self, image_path, game_object):
        super().__init__(ImageFile.load_image(image_path), game_object)
        self._path = image_path

    @staticmethod
    def deserialize(component_dict, obj):
        return ImageComponent(ImageFile.load_image(component_dict['path']), obj)

    def serialize(self):
        return {'name': 'ImageComponent', 'path': self._path}
