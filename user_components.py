from engine.input_manager import input_manager
from engine.scene_manager import scene_manager
from engine.base_components import Component

from pygame.math import Vector2
import pygame


class PlayerController(Component):
    def __init__(self, speed, game_object):
        super().__init__(game_object)
        self.speed = speed

    def update(self, *args):
        hor = input_manager.get_axis('Horizontal')
        vert = input_manager.get_axis('Vertical')

        x, y = self.game_object.transform.coord

        cam_move = Vector2(
            hor * self.speed if abs(x + hor * self.speed) < 1370 else 0,
            vert * self.speed if abs(y + vert * self.speed) < 1650 else 0
        )
        scene_manager.current_scene.current_camera.transform.move(cam_move.x, cam_move.y)

        move = Vector2(hor * self.speed, vert * self.speed)
        self.game_object.transform.move(move.x, move.y)

        for obj in scene_manager.current_scene.objects:
            phys_collider = self.game_object.get_component(PhysicsCollider)
            trigger_collider = self.game_object.get_component(TriggerCollider)

            if phys_collider is not None:
                phys_collider.update()
                if obj != self.game_object and obj.has_component(PhysicsCollider):
                    if phys_collider.detect_collision(obj.get_component(PhysicsCollider)):
                        scene_manager.current_scene.current_camera.transform.move(-cam_move.x, -cam_move.y)
                        self.game_object.transform.move(-move.x, -move.y)
            if trigger_collider is not None:
                trigger_collider.update()
                if obj != self.game_object and obj.has_component(TriggerCollider):
                    if trigger_collider.detect_collision(obj.get_component(TriggerCollider)):
                        print('trigger') # TODO


class Collider(Component):
    def __init__(self, shift_x, shift_y, rect, game_object):
        super().__init__(game_object)
        self.shift_x = shift_x
        self.shift_y = shift_y
        self.rect = pygame.Rect(rect)

    def detect_collision(self, collider):
        return self.rect.colliderect(collider.rect)

    def update(self, *args):
        self.rect.centerx = self.game_object.transform.x + self.shift_x
        self.rect.centery = self.game_object.transform.y + self.shift_y


class PhysicsCollider(Collider):
    pass


class TriggerCollider(Collider):
    pass
