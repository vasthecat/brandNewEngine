from engine.input_manager import input_manager
from engine.scene_manager import scene_manager
from engine.base_components import Component, TransformComponent

from pygame.math import Vector2

from math import acos, degrees


class ControllerComponent(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.transform = self.game_object.get_component(TransformComponent)
        self.speed = 10

    def get_mouse_coord(self):
        mouse = input_manager.get_mouse_pos()
        cam = scene_manager.current_scene.current_camera
        t = cam.get_component(TransformComponent)
        mouse_x = t.x + (cam.surface.get_rect().center[0] - mouse[0])
        mouse_y = t.y + (mouse[1] - cam.surface.get_rect().center[1])
        return -mouse_x, -mouse_y

    def update(self, *args):
        hor = input_manager.get_axis('Horizontal')
        vert = input_manager.get_axis('Vertical')
        # rot = input_manager.get_axis('Rotation')
        # self.transform.move(hor * 10, vert * 10)
        # self.transform.rotate(rot * 5)
        mouse = self.get_mouse_coord()

        delta = Vector2(mouse[0] - self.transform.x, mouse[1] - self.transform.y)
        try:
            cos = delta.x / delta.length()
            sin = delta.y / delta.length()
            rot = degrees(acos(cos))
            if sin < 0:
                rot = -rot
        except:
            rot = 0

        move = Vector2(hor, vert)
        if move.length() != 0:
            move = move.normalize() * self.speed
        self.transform.move(move.x, move.y)
        self.transform.set_rotation(rot)
