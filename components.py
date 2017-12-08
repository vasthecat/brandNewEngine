class Component:
    def __init__(self, game_object):
        self.game_object = game_object

    def update(self, *args):
        pass


class TransformComponent(Component):
    def __init__(self, x, y, game_object):
        super().__init__(game_object)
        self.x, self.y = self.coord = x, y

    def move(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y
        self.coord = self.x, self.y
