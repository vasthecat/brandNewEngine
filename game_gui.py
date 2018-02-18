from pygame import Color
from engine.gui import gui, Button, Image, load_image, Label
from game_menu_gui import init as game_menu_init
from engine.initialize_engine import width, height

def init():
    gui.add_element(Button((width // 2, height - 35), {
        'normal': 'images/button/normal.png',
        'hovered': 'images/button/hovered.png',
        'clicked': 'images/button/clicked.png'
    }, 'game_menu', game_menu_init))
    gui.add_element(Label((width // 2, height - 35), 38, "Menu", Color('white'), 'fonts/Dot.ttf', 'label_game_menu'))


