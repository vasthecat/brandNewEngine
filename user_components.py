from engine.input_manager import input_manager
from engine.scene_manager import scene_manager
from engine.initialize_engine import width, height
from engine.base_components import Component, ImageComponent, ImageFile
from engine.game_objects import GameObject

from pygame.math import Vector2
import pygame
import itertools as it
from time import time
import random

from engine.gui import gui, Label


class AnimationContoller(ImageComponent):
    def __init__(self, animations, start_animation, game_object):
        self.animations = {}
        for name, params in animations.items():
            self.animations[name] = AnimationContoller.cut_sheet(
                AnimationContoller.load_image(params['path']), *params['size'], params['repeats']
            )
        self._current_animation_name = start_animation
        self._current_animation = it.cycle(self.animations[start_animation])
        super().__init__(next(self._current_animation), game_object)

    @staticmethod
    def cut_sheet(sheet, rows, cols, repeats):
        frames = []
        for j in range(rows):
            for i in range(cols):
                frame = sheet.subsurface(pygame.Rect(
                    sheet.get_width() // cols * i, sheet.get_height() // rows * j,
                    sheet.get_width() // cols, sheet.get_height() // rows
                ))
                for _ in range(repeats):
                    frames.append(frame)
        return frames

    def add_animation(self, name, path, size, repeats):
        self.animations[name] = AnimationContoller.cut_sheet(
            AnimationContoller.load_image(path), *size, repeats
        )

    def set_animation(self, name):
        self._current_animation_name = name
        self._current_animation = it.cycle(self.animations[name])

    def play_animation(self, name, times):
        self._current_animation = it.chain(
            iter(self.animations[name] * times), it.cycle(self.animations[self._current_animation_name])
        )

    def update(self, *args):
        self.image = next(self._current_animation)

    @staticmethod
    def deserialize(component_dict, obj):
        return AnimationContoller(
            component_dict['animations'], component_dict['start_animation'], obj
        )

    def serialize(self):
        return {}  # TODO


def test_func_press_e():
    #It is test function
    print('Press "e"')


def test_func_press_spase():
    print('Press " "')


class PlayerController(Component):
    def __init__(self, speed, game_object):
        super().__init__(game_object)
        self.speed = speed
        self.gui_obj = {}
        self._prev_move = Vector2()
        self._direction = 'down'

    def update(self, *args):
        hor = input_manager.get_axis('Horizontal')
        vert = input_manager.get_axis('Vertical')

        x, y = self.game_object.transform.coord
        print(x, y)

        cam = scene_manager.current_scene.current_camera
        old_cam_pos = cam.transform.coord

        if abs(x + hor * self.speed) < 1024 - width // 2:
            cam.transform.move_to(x + hor * self.speed, cam.transform.y)
        if abs(y + vert * self.speed) < 1024 - height // 2:
            cam.transform.move_to(cam.transform.x, y + vert * self.speed)

        move = Vector2(hor * self.speed, vert * self.speed)
        self.game_object.transform.move(move.x, move.y)

        animator = self.game_object.get_component(AnimationContoller)
        if animator is not None:
            if self._prev_move.y == 0 and move.y > 0:
                animator.set_animation('up')
                self._direction = 'up'
            elif self._prev_move.y == 0 and move.y < 0:
                animator.set_animation('down')
                self._direction = 'down'

            if self._prev_move.x == 0 and move.x > 0:
                animator.set_animation('right')
                self._direction = 'right'
            elif self._prev_move.x == 0 and move.x < 0:
                animator.set_animation('left')
                self._direction = 'left'

            if move.x == move.y == 0:
                animator.set_animation('idle_' + self._direction)

        self._prev_move = move

        for obj in scene_manager.current_scene.objects:
            phys_collider = self.game_object.get_component(PhysicsCollider)
            trigger_collider = self.game_object.get_component(TriggerCollider)

            if phys_collider is not None:
                phys_collider.update()
                if obj != self.game_object and obj.has_component(PhysicsCollider):
                    if phys_collider.detect_collision(obj.get_component(PhysicsCollider)):
                        scene_manager.current_scene.current_camera.transform.move_to(*old_cam_pos)
                        self.game_object.transform.move(-move.x, -move.y)
                        self._prev_move = Vector2()
            if trigger_collider is not None:
                trigger_collider.update()
                if obj != self.game_object and obj.has_component(TriggerCollider):
                    if trigger_collider.detect_collision(obj.get_component(TriggerCollider)):
                        text = obj.get_component(TriggerCollider).text_for_player
                        x = 1280 / 2 - len(text) * len(text) / 2 - 100
                        _ = Label((x, 500, 10, 100), text, pygame.Color('black'), 'fonts/8875.otf',obj.get_component(TriggerCollider).trigger_name,
                                  {pygame.K_e: test_func_press_e,
                                   pygame.K_SPACE: test_func_press_spase})
                        gui.add_element(_)
                        self.gui_obj[obj.get_component(TriggerCollider).trigger_name] = _
                    else:
                        _ = obj.get_component(TriggerCollider).trigger_name
                        gui.del_element(_)
                        if _ in self.gui_obj:
                            del self.gui_obj[_]

    @staticmethod
    def deserialize(component_dict, obj):
        return PlayerController(component_dict['speed'], obj)

    def serialize(self):
        return {'name': 'PlayerController', 'speed': self.speed}


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

    @staticmethod
    def deserialize(component_dict, obj):
        return Collider(
            component_dict['shift_x'], component_dict['shift_y'],
            component_dict['rect'], obj
        )

    def serialize(self):
        return {'name': 'Collider', 'shift_x': self.shift_x, 'shift_y': self.shift_y, 'rect': self.rect}


class PhysicsCollider(Collider):
    def __init__(self, shift_x, shift_y, rect, game_object):
        if not rect:
            rect = game_object.get_component(ImageComponent)
            if rect is None:
                raise ValueError('rect parameter is empty and PhysicsCollider component added before ImageComponent')
            else:
                rect = rect.image.get_rect()

        self.go = GameObject(*game_object.transform.coord)
        surface = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        surface.fill(pygame.Color(255, 0, 0, 120))
        i = ImageComponent('images/player.png', self.go)
        i.image = surface
        i._original = surface
        scene_manager.current_scene.add_object(self.go)
        self.go.add_component(i)

        super().__init__(shift_x, shift_y, rect, game_object)

    def update(self, *args):
        super().update()
        x = self.game_object.transform.x + self.shift_x
        y = self.game_object.transform.y + self.shift_y
        self.go.transform.move_to(x, y)

    @staticmethod
    def deserialize(component_dict, obj):
        return PhysicsCollider(
            component_dict['shift_x'], component_dict['shift_y'],
            component_dict['rect'], obj
        )

    def serialize(self):
        d = super().serialize()
        d['name'] = 'PhysicsCollider'
        return d


class TriggerCollider(Collider):
    def __init__(self, shift_x, shift_y, rect, text_for_player, trigger_name, game_object):
        self.text_for_player = text_for_player
        self.trigger_name = trigger_name
        super().__init__(shift_x, shift_y, rect, game_object)

    @staticmethod
    def deserialize(component_dict, obj):
        return TriggerCollider(
            component_dict['shift_x'], component_dict['shift_y'],
            component_dict['rect'], component_dict.get('text_for_player', ''),
            component_dict['trigger_name'], obj
        )

    def serialize(self):
        d = super().serialize()
        d.update({
            'name': 'TriggerCollider', 'trigger_name': self.trigger_name,
            'text_for_player': self.text_for_player
        })
        return d


class ParticleSystem(Component):
    def __init__(self, image_path, particles_per_frame, correction, speed, life_time, game_object):
        self.path = image_path
        self.particles_per_frame = particles_per_frame
        self.speed = speed
        self.life_time = life_time
        self.correction = Vector2(correction) + Vector2(-0.5, -0.5)
        super().__init__(game_object)

    def update(self, *args):
        for _ in range(self.particles_per_frame):
            go = GameObject(*self.game_object.transform.coord)
            go.add_component(ImageFile(self.path, go))
            go.add_component(Particle(
                (self.correction + Vector2(random.random(), random.random())).normalize(),
                self.speed, self.life_time, go
            ))
            scene_manager.current_scene.add_object(go)

    @staticmethod
    def deserialize(component_dict, obj):
        return ParticleSystem(
            component_dict['path'], component_dict['particles_per_frame'], component_dict['correction'],
            component_dict['speed'], component_dict['life_time'], obj
        )


class Particle(Component):
    def __init__(self, direction, speed, life_time, game_object):
        super().__init__(game_object)
        self.life_time = life_time
        self.direction = direction
        self.speed = speed
        self._start = time()

    def update(self, *args):
        if time() - self._start >= self.life_time:
            # POSSIBLE MEMORY LEAK ????????
            scene_manager.current_scene.remove_object(self.game_object)
        else:
            move = self.direction * self.speed
            self.game_object.transform.move(move.x, move.y)
