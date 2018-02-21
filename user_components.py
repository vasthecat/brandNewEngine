import itertools as it
from time import time
import random
from math import copysign


from pygame.math import Vector2
import pygame


from engine.input_manager import input_manager
from engine.scene_manager import scene_manager
from engine.initialize_engine import width, height
from engine.base_components import Component, ImageComponent, ImageFile
from engine.game_objects import GameObject
from engine.gui import gui, Label, Button

from gui_misc import MedievalButton


class SceneReplacement:
    coords = {}

    @staticmethod
    def load_house(coord):
        from scene_loader import load_scene
        gui.del_element('house')
        gui.del_element('label_house')
        load_scene('scenes/house.json')
        SceneReplacement.coords['coord_in_street'] = coord

    @staticmethod
    def load_street(obj):
        from scene_loader import load_scene
        gui.del_element('enter_to_street')
        gui.del_element('label_enter_to_street')
        load_scene('scenes/scene1.json')
        scene_manager.current_scene.find_objects(obj.name)[0].transform.move_to(*SceneReplacement.coords['coord_in_street'])


class AnimationController(ImageComponent):
    def __init__(self, animations, start_animation, game_object):
        self.animations = {}
        for name, params in animations.items():
            self.animations[name] = AnimationController.cut_sheet(
                AnimationController.load_image(params['path']), *params['size'], params['repeats']
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
        self.animations[name] = AnimationController.cut_sheet(
            AnimationController.load_image(path), *size, repeats
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
        return AnimationController(
            component_dict['animations'], component_dict['start_animation'], obj
        )

    def serialize(self):
        return {}  # TODO


class PlayerController(Component):
    def __init__(self, speed, game_object):
        super().__init__(game_object)
        self.speed = speed
        self.gui_obj = {}
        self._prev_move = Vector2()
        self._direction = 'down'
        self.set_camera_pos(Vector2())

        self._steps_sound = pygame.mixer.Sound('sounds/steps.ogg')

    def change_animation(self, move):
        animator = self.game_object.get_component(AnimationController)
        if animator is not None:
            if move.x > 0:
                if self._prev_move.x == 0 or self._direction != 'right':
                    animator.set_animation('right')
                self._direction = 'right'
            elif move.x < 0:
                if self._prev_move.x == 0 or self._direction != 'left':
                    animator.set_animation('left')
                self._direction = 'left'
            elif move.y > 0:
                if self._prev_move.y == 0 or self._direction != 'up':
                    animator.set_animation('up')
                self._direction = 'up'
            elif move.y < 0:
                if self._prev_move.y == 0 or self._direction != 'down':
                    animator.set_animation('down')
                self._direction = 'down'
            elif move.x == move.y == 0:
                animator.set_animation('idle_' + self._direction)

    def play_sound(self, move):
        if self._prev_move.length() == 0 and move.length() != 0:
            self._steps_sound.play(-1)
        elif move.length() == 0:
            self._steps_sound.stop()

    def set_camera_pos(self, player_move):
        cam = scene_manager.current_scene.current_camera
        x, y = self.game_object.transform.coord

        if abs(x + player_move.x) < 1024 - width // 2:
            cam.transform.move_to(x + player_move.x, cam.transform.y)
        else:
            cam.transform.move_to(
                copysign(1024 - width // 2, x + player_move.x), cam.transform.y
            )

        if abs(y + player_move.y) < 1024 - height // 2:
            cam.transform.move_to(cam.transform.x, y + player_move.y)
        else:
            cam.transform.move_to(
                cam.transform.x, copysign(1024 - height // 2, y + player_move.y)
            )

    def update(self, *args):
        move = Vector2(
            input_manager.get_axis('Horizontal') * self.speed,
            input_manager.get_axis('Vertical') * self.speed
        )
        self.game_object.transform.move(move.x, move.y)

        phys_collider = self.game_object.get_component(PhysicsCollider)
        trigger_collider = self.game_object.get_component(TriggerCollider)

        for obj in scene_manager.current_scene.objects:
            if phys_collider is not None:
                phys_collider.update()
                if obj != self.game_object and obj.has_component(PhysicsCollider):
                    collision = phys_collider.detect_collision(obj.get_component(PhysicsCollider))
                    if collision:
                        self.game_object.transform.move(-move.x, -move.y)
                        move = Vector2()

            if trigger_collider is not None:
                trigger_collider.update()
                if obj != self.game_object and obj.has_component(TriggerCollider):
                    if trigger_collider.detect_collision(obj.get_component(TriggerCollider)):
                        if obj.get_component(TriggerCollider).trigger_name == 'House':
                            _ = MedievalButton(
                                (width//2, height-100), 'house',
                                lambda: SceneReplacement.load_house(self.game_object.transform.coord)
                            )

                            gui.add_element(_)
                            _1= Label((width//2, height-100), 30, "Enter in house", pygame.Color('white'), 'fonts/Dot.ttf', 'label_house')
                            gui.add_element(_1)
                            self.gui_obj[obj.get_component(TriggerCollider)] = [_, _1]

                        elif obj.get_component(TriggerCollider).trigger_name == 'enter_in_street':
                            _ = MedievalButton(
                                (width // 2, height - 100), 'enter_to_street',
                                lambda: SceneReplacement.load_street(self.game_object)
                            )
                            gui.add_element(_)
                            _1 = Label(
                                (width // 2, height - 100), 30, "Come to street", pygame.Color('white'),
                                'fonts/Dot.ttf', 'label_enter_to_street'
                            )
                            gui.add_element(_1)
                            self.gui_obj[obj.get_component(TriggerCollider)] = [_, _1]
                    else:
                        if obj.get_component(TriggerCollider) in self.gui_obj:
                            for i in self.gui_obj[obj.get_component(TriggerCollider)]:
                                gui.del_element(i.name)
                            del self.gui_obj[obj.get_component(TriggerCollider)]

        self.set_camera_pos(move)
        self.change_animation(move)
        self.play_sound(move)
        self._prev_move = move

    @staticmethod
    def deserialize(component_dict, obj):
        return PlayerController(component_dict['speed'], obj)

    def serialize(self):
        return {'name': 'PlayerController', 'speed': self.speed}


class _ColliderSprite(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.shift_x = rect[0]
        self.shift_y = rect[1]
        self.rect = pygame.Rect(0, 0, *rect[2:])

    def move_to(self, x, y):
        self.rect.center = x + self.shift_x, y + self.shift_y

    def update(self, x, y, *args):
        self.move_to(x, y)


class Collider(Component):
    def __init__(self, rects, game_object):
        super().__init__(game_object)
        self.rects = pygame.sprite.Group(*(_ColliderSprite(rect) for rect in rects))

    def detect_collision(self, collider):
        return pygame.sprite.groupcollide(self.rects, collider.rects, False, False)

    def update(self, *args):
        self.rects.update(*self.game_object.transform.coord)

    @staticmethod
    def deserialize(component_dict, obj):
        return Collider(component_dict['rects'], obj)

    def serialize(self):
        return {'name': 'Collider'}  # TODO


class PhysicsCollider(Collider):
    def __init__(self, rects, game_object):
        if not rects:
            rect = game_object.get_component(ImageComponent)
            if rect is None:
                raise ValueError('rect parameter is empty and PhysicsCollider component added before ImageComponent')
            else:
                rects = [rect.image.get_rect()]

        super().__init__(rects, game_object)

    @staticmethod
    def deserialize(component_dict, obj):
        return PhysicsCollider(component_dict['rects'], obj)

    def serialize(self):
        d = super().serialize()
        d['name'] = 'PhysicsCollider'
        return d


class TriggerCollider(Collider):
    def __init__(self, rects, text_for_player, trigger_name, game_object):
        self.text_for_player = text_for_player
        self.trigger_name = trigger_name
        super().__init__(rects, game_object)

    @staticmethod
    def deserialize(component_dict, obj):
        return TriggerCollider(
            component_dict['rects'], component_dict.get('text_for_player', ''),
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


class MusicController(Component):
    def __init__(self, music_paths, game_object):
        super().__init__(game_object)
        for path, volume in music_paths:
            snd = pygame.mixer.Sound(path)
            snd.set_volume(volume / 100)
            snd.play(-1)

    @staticmethod
    def deserialize(component_dict, obj):
        return MusicController(component_dict['paths'], obj)
