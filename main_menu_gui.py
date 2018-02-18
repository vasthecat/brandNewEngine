from engine.gui import gui, load_image, Button, Label, Image
from engine.initialize_engine import width, height
from pygame import Color, quit
import pygame
from sys import exit
from game_gui import init as init_game_gui

from scene_loader import load_scene

from random import randint


class CloudsController:
    def __init__(self, name, change_pos):
        self.name = name
        self.change_pos = change_pos
        self.elements = []

    def add_element(self, element):
        if randint(0, 1):
            self.elements.append({'element': element, 'step': (-self.change_pos[0], self.change_pos[1])})
            element.const_rect.x = width
        else:
            self.elements.append({'element': element, 'step': (self.change_pos[0], self.change_pos[1])})

    def update(self):
        for element in self.elements:
            element['element'].move(*element['step'])
            if element['element'].get_pos()[0] > width or element['element'].get_pos()[1] > height \
                    or element['element'].get_pos()[0] + element['element'].size[0] < 0 \
                    or element['element'].get_pos()[1] + element['element'].size[1] < 0:
                element['element'].set_const_pos()

    def render(self, surface):
        for element in self.elements:
            surface.blit(element['element'].image, element['element'].rect)



def start_game():
    load_scene('scenes/scene1.json')
    gui.clear()
    init_game_gui()

    gui.add_element(Label((50, 25), 50, '0', pygame.Color('red'), 'fonts/Dot.ttf', 'fps_label'))

def my_exit():
    quit()
    exit()


def generate_clouds(n_clouds, clouds_controller):
    for _ in range(n_clouds):
        x, y = randint(-100, 700), randint(0, height)
        i = str(randint(1, 7))
        clouds_controller.add_element(
            Image((x, y), load_image(
                'images/clouds/cloud{}.png'.format(i)), 'cloud{}'.format(i))
        )


def init():
    clouds_controller = CloudsController('Con', [1, 0])
    generate_clouds(15, clouds_controller)

    gui.add_element(Image((width //2, height // 2), pygame.transform.scale(
        load_image('images/sky.png'), (width, height)
    ), 'sky'))
    gui.add_element(clouds_controller)

    gui.add_element(Image((width // 2, 75), load_image('images/title_bg.png'), 'title'))
    gui.add_element(Label((width // 2, 159), 53, 'Untitled game', pygame.Color('white'), 'fonts/Dot.ttf', 'title_text'))

    gui.add_element(Button((width // 2, height // 2), {
        'normal': 'images/button/normal.png',
        'hovered': 'images/button/hovered.png',
        'clicked': 'images/button/clicked.png'
    }, 'start_game', start_game))

    gui.add_element(Label((width // 2, height // 2), 38, "Start game", Color('white'), 'fonts/Dot.ttf', 'label_game'))

    gui.add_element(Button((width // 2, height // 2 + 100), {
        'normal': 'images/button/normal.png',
        'hovered': 'images/button/hovered.png',
        'clicked': 'images/button/clicked.png'
    }, 'exit', my_exit))

    gui.add_element(Label((width // 2, height // 2 + 100), 38, "Exit", Color('white'), 'fonts/Dot.ttf', 'label_exit'))
