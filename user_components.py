from engine.input_manager import input_manager
from engine.scene_manager import scene_manager
from engine.base_components import Component, ImageComponent

import engine.gui

from pygame.math import Vector2
import pygame

from engine.gui import *


class PlayerController(Component):
    def __init__(self, speed, game_object):
        super().__init__(game_object)
        self.speed = speed
        self.gui_obj = {}

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
                        text = obj.get_component(TriggerCollider).text_for_player

                        _ = Label((200, 500, 10, 100), text, pygame.Color('black'), obj.get_component(TriggerCollider).trigger_name)
                        gui.add_element(_)
                        self.gui_obj[obj.get_component(TriggerCollider).trigger_name] = _
                    else:
                        _ = obj.get_component(TriggerCollider).trigger_name
                        gui.del_element(_)
                        if _ in self.gui_obj:
                            del self.gui_obj[_]


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
    def __init__(self, shift_x, shift_y, rect, game_object):
        if not rect:
            rect = game_object.get_component(ImageComponent)
            if rect is None:
                raise ValueError('rect parameter is empty and PhysicsCollider component added before ImageComponent')
            else:
                rect = rect.image.get_rect()
        super().__init__(shift_x, shift_y, rect, game_object)


class TriggerCollider(Collider):
    def __init__(self, shift_x, shift_y, rect, name, text_for_player, trigger_name,game_object):
        self.name = name
        self.text_for_player = text_for_player
        self.trigger_name = trigger_name
        super().__init__(shift_x, shift_y, rect, game_object)
