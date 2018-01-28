from engine.input_manager import input_manager
from engine.scene_manager import scene_manager
from engine.base_components import Component, TransformComponent, ImageComponent
from engine.game_objects import GameObject

from pygame.math import Vector2
import pygame

from math import acos, degrees
from time import time


class ControllerComponent(Component):
    def __init__(self, speed, game_object):
        super().__init__(game_object)
        self.transform = self.game_object.get_component(TransformComponent)
        self.speed = speed
        self.sound = pygame.mixer.Sound('sounds/steps.ogg')
        self._prev_move = Vector2(0, 0)

    def get_mouse_coord(self):
        mouse = input_manager.get_mouse_pos()
        cam = scene_manager.current_scene.current_camera
        t = cam.transform
        mouse_x = t.x + (mouse[0] - cam.surface.get_rect().center[0])
        mouse_y = t.y + (cam.surface.get_rect().center[1] - mouse[1])
        return mouse_x, mouse_y

    def update(self, *args):
        hor = input_manager.get_axis('Horizontal')
        vert = input_manager.get_axis('Vertical')
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
            if self._prev_move.length() == 0:
                pygame.mixer.Channel(0).play(self.sound, -1)
        else:
            pygame.mixer.Channel(0).stop()
        self._prev_move = move

        self.transform.move(move.x, move.y)
        self.transform.set_rotation(rot)
        scene_manager.current_scene.current_camera.transform.move(move.x, move.y)


class ShooterComponent(Component):
    def __init__(self, speed, life_time, rate_of_fire, game_object):
        super().__init__(game_object)
        self.speed = speed
        self.life_time = life_time
        self.rate_of_fire = rate_of_fire
        self.bullets = []
        self.prev_t = -1
        self.scene = scene_manager.current_scene
        self.sound = pygame.mixer.Sound('sounds/shot.ogg')

    def update(self, *args):
        if pygame.mouse.get_pressed()[0] and time() - self.prev_t >= self.rate_of_fire:
            pygame.mixer.Channel(1).play(self.sound)
            bullet = GameObject(*self.game_object.transform.coord)
            bullet.add_component(ImageComponent('images/bullet.png', False, bullet))
            bullet.transform.set_rotation(self.game_object.transform.rotation)
            self.bullets.append((bullet, time()))
            self.scene.add_object(bullet)
            self.prev_t = time()

        for bullet, t in self.bullets:
            if time() - t >= self.life_time:
                self.scene.remove_object(bullet)
                self.bullets.remove((bullet, t))
            else:
                move = Vector2(1, 0).rotate(bullet.transform.rotation).normalize() * self.speed
                bullet.transform.move(move.x, move.y)
