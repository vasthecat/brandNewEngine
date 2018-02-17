from engine.gui import gui, Button, Label, Image, CloudsController
from pygame import Color, quit
from sys import exit

from scene_loader import load_scene

from random import randint

def start_game():
    load_scene('scenes/scene1.json')
    gui.clear()

def my_exit():
    quit()
    exit()


def generate_cloude(max_cl):
    for i in range(1, max_cl+1):
        x, y = randint(-100, 700), randint(0, 700)
        clouds_controller.add_element(Image((x, y), 'images/clouds/cloud{}.png'.format(i), 'cloud{}'.format(i)))

clouds_controller = CloudsController('Con', [1, 0])
generate_cloude(7)

def init():
    gui.add_element(Image((0, 0), 'images/sky.png', 'sky'))
    gui.add_element(clouds_controller)

    gui.add_element(Button((640, 280), {
        'normal': 'images/button/normal.png',
        'hovered': 'images/button/hovered.png',
        'clicked': 'images/button/clicked.png'
    }, 'start_game', start_game))

    gui.add_element(Label((640, 280), 38, "Start game", Color('white'), 'fonts/Dot.ttf', 'label_game'))

    gui.add_element(Button((640, 400), {
        'normal': 'images/button/normal.png',
        'hovered': 'images/button/hovered.png',
        'clicked': 'images/button/clicked.png'
    }, 'exit', my_exit))

    gui.add_element(Label((640, 400), 38, "Exit", Color('white'), 'fonts/Dot.ttf', 'label_exit'))
