from engine.gui import load_image, Image, Button, CheckboxWithText
from engine.base_components import Component
from engine.input_manager import InputManager
from engine.scene_manager import SceneManager
from engine.initialize_engine import Config
from engine.save_manager import SaveManager

from random import randint
import pygame


class CloudsController:
    def __init__(self, name, change_pos):
        self.name = name
        self.change_pos = change_pos
        self.elements = []

    @staticmethod
    def generate_clouds(n_clouds, clouds_controller):
        for _ in range(n_clouds):
            x, y = randint(-100, 700), randint(0, Config.get_height())
            i = str(randint(1, 7))
            clouds_controller.add_element(
                Image((x, y), load_image(
                    'images/clouds/cloud{}.png'.format(i)), 'cloud{}'.format(i))
            )

    def add_element(self, element):
        if randint(0, 1):
            self.elements.append({'element': element, 'step': (-self.change_pos[0], self.change_pos[1])})
            element.const_rect.x = Config.get_width()
        else:
            self.elements.append({'element': element, 'step': (self.change_pos[0], self.change_pos[1])})

    def update(self):
        for element in self.elements:
            element['element'].move(*element['step'])
            if element['element'].get_pos()[0] > Config.get_width() or element['element'].get_pos()[1] > Config.get_width() \
                    or element['element'].get_pos()[0] + element['element'].size[0] < 0 \
                    or element['element'].get_pos()[1] + element['element'].size[1] < 0:
                element['element'].set_const_pos()

    def render(self, surface):
        for element in self.elements:
            surface.blit(element['element'].image, element['element'].rect)


class MedievalButton(Button):
    def __init__(self, pos, text, text_size, name, func=lambda: None, *args):
        super().__init__(pos, {
            'normal': 'images/button/normal.png',
            'hovered': 'images/button/hovered.png',
            'clicked': 'images/button/clicked.png'
        }, text, 'fonts/Dot.ttf', 'white', text_size, name, func, *args)


class MedievalCheckbox(CheckboxWithText):
    def __init__(self, name, pos, text, text_size, value=False, func=lambda val: None):
        super().__init__(name, pos, {
            'normal_checked': 'images/checkbox/normal_checked.png',
            'normal_unchecked': 'images/checkbox/normal_unchecked.png',
            'hovered_checked': 'images/checkbox/hovered_checked.png',
            'hovered_unchecked': 'images/checkbox/hovered_unchecked.png',
        }, text, 'fonts/Dot.ttf', 'white', text_size, value, func)


class ButtonChanger(Component):
    def __init__(self, name, button, game_object):
        super().__init__(game_object)
        self.name = name
        self.button = button

    def update(self, *args):
        for event in InputManager.get_events():
            if event.type == pygame.KEYDOWN:
                if event.key not in list(InputManager.AXES['Horizontal']) + list(InputManager.AXES['Vertical']) or \
                        event.key == SaveManager.get_entry('preferences', self.name):

                    direction = 'Horizontal' if self.name in ('left', 'right') else 'Vertical'

                    axis = InputManager.AXES[direction]
                    axis[event.key] = axis.pop(SaveManager.get_entry('preferences', self.name))
                    InputManager.set_axis(direction, axis)

                    SaveManager.set_entry('preferences', self.name, event.key)
                    self.button.text = 'Move {}: {}'.format(
                        self.name, pygame.key.name(SaveManager.get_entry('preferences', self.name))
                    )
                    SceneManager.current_scene.remove_object(self.game_object)
