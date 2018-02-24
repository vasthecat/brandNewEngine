import itertools as it
from time import time
import random
from math import copysign, hypot


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
    del_tardis_flag = False


    @staticmethod
    def load_house(coord, house):
        from scene_loader import load_scene
        gui.del_element('house')
        gui.del_element('label_house')
        load_scene('scenes/{}.json'.format(house))
        SceneReplacement.coords['coord_in_street'] = coord

        if SceneReplacement.del_tardis_flag:
            if scene_manager.current_scene.find_objects('tardis'):
                scene_manager.current_scene.remove_object(scene_manager.current_scene.find_objects('tardis')[0])
        else:
            SceneReplacement.del_tardis_flag = True

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


        self.flag = False #Debug


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
        print(self.game_object.transform.coord)
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
                        trigger_name = obj.get_component(TriggerCollider).trigger_name
                        if len(trigger_name) > 5 and trigger_name[:5] == 'house':
                            _ = MedievalButton(
                                (width//2, height-100), 'Enter in house', 29, 'house',
                                lambda: SceneReplacement.load_house(self.game_object.transform.coord, trigger_name)
                            )

                            gui.add_element(_)
                            self.gui_obj[obj.get_component(TriggerCollider)] = _

                        elif trigger_name == 'enter_in_street':
                            _ = MedievalButton(
                                (width // 2, height - 100), 'Come to street', 29, 'enter_to_street',
                                lambda: SceneReplacement.load_street(self.game_object)
                            )
                            gui.add_element(_)
                            self.gui_obj[obj.get_component(TriggerCollider)] = _
                    else:
                        if obj.get_component(TriggerCollider) in self.gui_obj:
                            gui.del_element(self.gui_obj[obj.get_component(TriggerCollider)].name)
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

        self.go = GameObject(*self.rect.center)
        surface = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        surface.fill(pygame.Color(0, 255, 0, 120))
        i = ImageComponent(surface, self.go)

        scene_manager.current_scene.add_object(self.go)
        self.go.add_component(i)

    def move_to(self, x, y):
        self.rect.center = x + self.shift_x, y + self.shift_y

    def update(self, x, y, *args):
        self.go.transform.move_to(self.rect.centerx, self.rect.centery)

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
    def __init__(self, rects, trigger_name, game_object):
        self.trigger_name = trigger_name
        super().__init__(rects, game_object)

    @staticmethod
    def deserialize(component_dict, obj):
        return TriggerCollider(
            component_dict['rects'], component_dict['trigger_name'], obj
        )

    def serialize(self):
        d = super().serialize()
        d.update({'name': 'TriggerCollider', 'trigger_name': self.trigger_name})
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


class NPCController(Component):
    def __init__(self, speed, commands, game_object):
        super().__init__(game_object)
        self.speed = speed

        _ = []
        for i, com in enumerate(commands):
            com_ = com.split()[0]
            if com_ == 'move_to' and len(com_) > 2:
                for com2 in com.split()[1:]:
                    _1 = com2.replace('(', '').replace(')', '').replace(';', ' ')
                    _.append("move_to {}".format(_1))
            else:
                _.append(com)

        self.commands = it.cycle(_)
        self.current_command = next(self.commands)
        self._start_sleep = None
        self._prev_move = Vector2()
        self._direction = 'down'

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

    def update(self, *args):
        command = self.current_command.split()
        if command[0] == 'move_to':
            move = Vector2(int(command[1]) - self.game_object.transform.x, int(command[2]) - self.game_object.transform.y)
            if move.length() > self.speed:
                move = move.normalize() * self.speed
            else:
                self.current_command = next(self.commands)

            self.game_object.transform.move(move.x, move.y)

            phys_collider = self.game_object.get_component(PhysicsCollider)
            for obj in scene_manager.current_scene.objects:
                if phys_collider is not None:
                    phys_collider.update()
                    if obj != self.game_object and obj.has_component(PhysicsCollider):
                        collision = phys_collider.detect_collision(obj.get_component(PhysicsCollider))
                        if collision:
                            self.game_object.transform.move(-move.x, -move.y)
                            move = Vector2()

            self.change_animation(move)
            self._prev_move = move

        elif command[0] == 'sleep':
            if self._start_sleep is None:
                self._start_sleep = time()
            if time() - self._start_sleep >= float(command[1]):
                self.current_command = next(self.commands)
                self._start_sleep = None
            self.change_animation(Vector2())
            self._prev_move = Vector2()

        elif command[0] == 'del_self':
            scene_manager.current_scene.remove_object(self.game_object)


    @staticmethod
    def deserialize(component_dict, obj):
        return NPCController(component_dict['speed'], component_dict['commands'], obj)
