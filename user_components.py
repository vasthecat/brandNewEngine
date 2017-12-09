from engine.input_manager import input_manager
from engine.base_components import Component, TransformComponent


class ControllerComponent(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.transform = self.game_object.get_component(TransformComponent)

    def update(self, *args):
        hor = input_manager.get_axis('Horizontal')
        vert = input_manager.get_axis('Vertical')
        rot = input_manager.get_axis('Rotation')
        self.transform.move(hor * 10, vert * 10)
        self.transform.rotate(rot * 5)

