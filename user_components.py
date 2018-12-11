import itertools as it
from time import time
import random
from math import copysign
import csv
import io

from pygame.math import Vector2
import pygame

from engine.input_manager import InputManager
from engine.scene_manager import SceneManager
from engine.save_manager import SaveManager
from engine.serialization_manager import SerializableClass
from engine.initialize_engine import Config
from engine.base_components import Component, ImageComponent, ImageFile
from engine.game_objects import GameObject
from engine.gui import GUI, Label, TextBox

from gui_misc import MedievalButton
from client import NetworkClient
from scene_loader import load_scene


@SerializableClass
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

    def play_animation(self, name, times=1):
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


@SerializableClass
class PlayerController(Component):
    def __init__(self, speed, game_object):
        super().__init__(game_object)
        self.speed = speed
        self.gui_obj = {}
        self._prev_move = Vector2()
        self._direction = 'down'
        self.set_camera_pos()

        self._steps_sound = pygame.mixer.Sound('sounds/steps.ogg')
        self._steps_sound.set_volume(60)

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
            elif move.x == move.y == 0 and self._prev_move.length() != 0:
                animator.set_animation('idle_' + self._direction)

    def play_sound(self, move):
        if self._prev_move.length() == 0 and move.length() != 0:
            self._steps_sound.play(-1)
        elif move.length() == 0:
            self._steps_sound.stop()

    def set_camera_pos(self):
        cam = SceneManager.current_scene.current_camera
        x, y = self.game_object.transform.coord

        if abs(x) < 1024 - Config.get_width() // 2:
            cam.transform.move_to(x, cam.transform.y)
        else:
            cam.transform.move_to(
                copysign(1024 - Config.get_width() // 2, x), cam.transform.y
            )

        if abs(y) < 1024 - Config.get_height() // 2:
            cam.transform.move_to(cam.transform.x, y)
        else:
            cam.transform.move_to(
                cam.transform.x, copysign(1024 - Config.get_height() // 2, y)
            )

    def update(self, *args):
        move = Vector2(
            InputManager.get_axis('Horizontal') * self.speed,
            InputManager.get_axis('Vertical') * self.speed
        ) * (InputManager.get_delta_tick() / 1000)
        self.game_object.transform.move(move.x, move.y)

        phys_collider = self.game_object.get_component(PhysicsCollider)

        for obj in SceneManager.current_scene.objects:
            if phys_collider is not None:
                phys_collider.update()
                if obj != self.game_object and obj.has_component(PhysicsCollider):
                    collision = phys_collider.detect_collision(obj.get_component(PhysicsCollider))
                    if collision:
                        self.game_object.transform.move(-move.x, -move.y)
                        move = Vector2()

        self.set_camera_pos()
        self.change_animation(move)
        self.play_sound(move)
        self._prev_move = move

    @staticmethod
    def deserialize(component_dict, obj):
        return PlayerController(component_dict['speed'], obj)


@SerializableClass
class HousesTrigger(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self._player = SceneManager.current_scene.find_object('player')
        self._player_collider = self._player.get_component(TriggerCollider)
        self._collider = self.game_object.get_component(TriggerCollider)

        self.gui_obj = None
        self._button_shown = False

    def load_scene(self):
        pass

    def update(self, *args):
        self.gui_obj.pos = Config.get_width() // 2, Config.get_height() - 100
        if self._collider is not None and self._player_collider is not None:
            if self._collider.detect_collision(self._player_collider):
                if not self._button_shown:
                    GUI.add_element(self.gui_obj)
                    self._button_shown = True
            else:
                if self._button_shown:
                    GUI.del_element(self.gui_obj.name)
                    self._button_shown = False

    @staticmethod
    def deserialize(component_dict, obj):
        return HousesTrigger(obj)


@SerializableClass
class House1Trigger(HousesTrigger):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.gui_obj = MedievalButton(
            (Config.get_width() // 2, Config.get_height() - 100), 'Enter in house', 29, 'house', self.load_scene
        )

    def load_scene(self):
        GUI.del_element('house')
        SaveManager.set_entry('village1', 'plr_coord', self._player.transform.coord)
        load_scene('scenes/house1.json')
        if SaveManager.get_entry('village1', 'seen_tardis'):
            SceneManager.current_scene.remove_object(SceneManager.current_scene.find_object('tardis'))

    @staticmethod
    def deserialize(component_dict, obj):
        return House1Trigger(obj)


@SerializableClass
class House2Trigger(HousesTrigger):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.gui_obj = MedievalButton(
            (Config.get_width() // 2, Config.get_height() - 100), 'Enter in house', 29, 'house', self.load_scene
        )

    def load_scene(self):
        GUI.del_element('house')
        SaveManager.set_entry('village1', 'plr_coord', self._player.transform.coord)
        load_scene('scenes/house2.json')

    @staticmethod
    def deserialize(component_dict, obj):
        return House2Trigger(obj)


@SerializableClass
class House3Trigger(HousesTrigger):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.gui_obj = MedievalButton(
            (Config.get_width() // 2, Config.get_height() - 100), 'Enter in house', 29, 'house', self.load_scene
        )

    def load_scene(self):
        GUI.del_element('house')
        SaveManager.set_entry('village1', 'plr_coord', self._player.transform.coord)
        load_scene('scenes/house3.json')

    @staticmethod
    def deserialize(component_dict, obj):
        return House3Trigger(obj)


@SerializableClass
class EnterVillageTrigger(HousesTrigger):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.gui_obj = MedievalButton(
            (Config.get_width() // 2, Config.get_height() - 100),
            'Enter the village', 25, 'enter_village', self.load_scene
        )

    def load_scene(self):
        GUI.del_element('enter_village')
        load_scene('scenes/scene1.json')
        SceneManager.current_scene.find_object('player').transform.move_to(
            *SaveManager.get_entry('village1', 'plr_coord')
        )

    @staticmethod
    def deserialize(component_dict, obj):
        return EnterVillageTrigger(obj)


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


@SerializableClass
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


@SerializableClass
class TriggerCollider(Collider):
    def __init__(self, rects, trigger_name, game_object):
        self.trigger_name = trigger_name
        super().__init__(rects, game_object)

    @staticmethod
    def deserialize(component_dict, obj):
        return TriggerCollider(
            component_dict['rects'], component_dict['trigger_name'], obj
        )


@SerializableClass
class ParticleEmitter(Component):
    def __init__(self, image_path, particles_per_second, correction, speed, life_time, game_object):
        self.path = image_path
        self.particles_per_second = particles_per_second
        self.speed = speed
        self.life_time = life_time
        self.correction = Vector2(correction) + Vector2(-0.5, -0.5)
        super().__init__(game_object)

    def update(self, *args):
        fps = InputManager.get_fps()
        if fps != 0:
            for _ in range(self.particles_per_second // fps + 1):
                go = GameObject(*self.game_object.transform.coord)
                go.add_component(ImageFile(self.path, go))
                go.add_component(Particle(
                    (self.correction + Vector2(random.random(), random.random())).normalize(),
                    self.speed, self.life_time, go
                ))
                SceneManager.current_scene.add_object(go)

    @staticmethod
    def deserialize(component_dict, obj):
        return ParticleEmitter(
            component_dict['path'], component_dict['particles_per_second'], component_dict['correction'],
            component_dict['speed'], component_dict['life_time'], obj
        )


class Particle(Component):
    def __init__(self, direction, speed, life_time, game_object):
        super().__init__(game_object)
        self.life_time = life_time
        self.direction = direction
        self.speed = speed
        # self._start = time()
        self._start = InputManager.get_ticks()

    def update(self, *args):
        if self._start + self.life_time * 1000 < InputManager.get_ticks():
            # POSSIBLE MEMORY LEAK ????????
            SceneManager.current_scene.remove_object(self.game_object)
        else:
            move = self.direction * self.speed * InputManager.get_delta_tick() / 1000
            self.game_object.transform.move(move.x, move.y)


@SerializableClass
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


@SerializableClass
class WaterSound(Component):
    def __init__(self, max_distance, game_object):
        super().__init__(game_object)
        self.sound = pygame.mixer.Sound('sounds/water_waves.ogg')
        self.sound.play(-1)
        self.player_transform = SceneManager.current_scene.find_object('player').transform
        self.max_distance = max_distance

    def update(self, *args):
        vol = (self.max_distance - Vector2(
            self.game_object.transform.x - self.player_transform.x,
            self.game_object.transform.y - self.player_transform.y
        ).length()) / self.max_distance

        self.sound.set_volume(0 if vol < 0 else vol)
        if vol < 0:
            self.sound.set_volume(0)
        else:
            self.sound.set_volume(vol)

    @staticmethod
    def deserialize(component_dict, obj):
        return WaterSound(component_dict['max_distance'], obj)


@SerializableClass
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
            elif move.x == move.y == 0 and self._prev_move.length() != 0:
                animator.set_animation('idle_' + self._direction)

    def update(self, *args):
        command = self.current_command.split()
        if command[0] == 'move_to':
            move = Vector2(
                int(command[1]) - self.game_object.transform.x,
                int(command[2]) - self.game_object.transform.y
            )

            if move.length() > self.speed * (InputManager.get_delta_tick() / 1000):
                move = move.normalize() * self.speed * (InputManager.get_delta_tick() / 1000)
            else:
                self.current_command = next(self.commands)

            self.game_object.transform.move(move.x, move.y)

            phys_collider = self.game_object.get_component(PhysicsCollider)
            for obj in SceneManager.current_scene.objects:
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
            SceneManager.current_scene.remove_object(self.game_object)

    @staticmethod
    def deserialize(component_dict, obj):
        return NPCController(component_dict['speed'], component_dict['commands'], obj)


@SerializableClass
class TardisController(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self._start_time = time()
        self.game_object.get_component(AnimationController).play_animation('start')

    def update(self, *args):
        SaveManager.set_entry('village1', 'seen_tardis', True)
        if time() - self._start_time > 3:
            SceneManager.current_scene.remove_object(self.game_object)

    @staticmethod
    def deserialize(component_dict, obj):
        return TardisController(obj)


@SerializableClass
class NetworkingController(Component):
    def __init__(self, login, host, port, game_object):
        super().__init__(game_object)
        self.client = NetworkClient(login, (host, port))
        self.player = SceneManager.current_scene.find_object('player')
        self.client.send('create')

    def update(self, *args):
        coord = 'coord {};{}'.format(*self.player.transform.coord)
        self.client.send(coord)
        for line in self.client.received.readlines():
            login, command = self.parse(line)
            if login != self.client.login:
                if command.startswith('coord '):
                    coord = map(float, command.replace('coord ', '').split(';'))
                    SceneManager.current_scene.find_object(login).transform.move_to(*coord)
                elif command.startswith('create'):
                    SceneManager.current_scene.add_object(self.create_player(login))

    def create_player(self, login):
        go = GameObject(-960, 712, login)
        go.add_component(AnimationController.deserialize({
            "name": "AnimationController",
            "start_animation": "idle_right",
            "animations": {
                "up": {"path": "images/player/run_up.png", "size": [1, 4], "repeats": 10},
                "down": {"path": "images/player/run_down.png", "size": [1, 4], "repeats": 10},
                "right": {"path": "images/player/run_right.png", "size": [1, 4], "repeats": 10},
                "left": {"path": "images/player/run_left.png", "size": [1, 4], "repeats": 10},

                "idle_up": {"path": "images/player/idle_up.png", "size": [1, 1], "repeats": 1},
                "idle_down": {"path": "images/player/idle_down.png", "size": [1, 1], "repeats": 1},
                "idle_right": {"path": "images/player/idle_right.png", "size": [1, 1], "repeats": 1},
                "idle_left": {"path": "images/player/idle_left.png", "size": [1, 1], "repeats": 1}
            }
        }, go))
        go.add_component(PhysicsCollider.deserialize({
            "name": "PhysicsCollider",
            "rects": [
                [0, -24, 30, 15]
            ]
        }, go))
        go.add_component(TriggerCollider.deserialize({
            "name": "TriggerCollider",
            "trigger_name": "PlayerTrigger",
            "rects": [
                [0, -24, 30, 15]
            ]
        }, go))
        return go

    def parse(self, s):
        return list(csv.reader(io.StringIO(s.decode()), delimiter=' ', quotechar='"'))[0]

    @staticmethod
    def deserialize(component_dict, obj):
        return NetworkingController(
            component_dict['login'], component_dict['host'],
            component_dict['port'], obj
        )


@SerializableClass
class ChatController(Component):
    def __init__(self, login, host, port, game_object):
        super().__init__(game_object)
        self.client = NetworkClient(login, (host, port))
        self.on_screen = False

    def update(self, *args):
        container = self.game_object.get_component(ChatContainer)
        for msg in self.client.received.readlines():
            container.add(': '.join(self.parse(msg)))
        for event in InputManager.get_events():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not self.on_screen:
                        GUI.add_element(TextBox(
                            (Config.get_width() // 8 + 10, Config.get_height() - 40, Config.get_width() // 4, 40),
                            '', callback=self.client.send, name='message_textbox'
                        ))
                        self.on_screen = True
                elif event.key == pygame.K_ESCAPE:
                    if self.on_screen:
                        GUI.del_element('message_textbox')
                        self.on_screen = False

    def parse(self, s):
        return list(csv.reader(io.StringIO(s.decode()), delimiter=' ', quotechar='"'))[0]

    @staticmethod
    def deserialize(component_dict, obj):
        return NetworkingController(
            component_dict['login'], component_dict['host'],
            component_dict['port'], obj
        )


@SerializableClass
class ChatContainer(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.container = []

    def add(self, message):
        if len(self.container) >= 5:
            GUI.del_element(self.container[0][0])
            self.container.pop(0)

        for i in range(5):
            name = 'message' + str(i)
            try:
                if name not in list(zip(*self.container))[0]:
                    break
            except IndexError:
                break

        self.container.append((name, GUI.add_element(Label(
            (200, Config.get_height() - 80), 32, message,
            pygame.Color('black'), 'fonts/Dot.ttf', name
        ))))

        for name, label in self.container:
            label.pos[1] -= 50

    @staticmethod
    def deserialize(component_dict, obj):
        return ChatContainer(obj)
