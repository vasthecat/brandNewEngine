from pygame import Color
import main_menu_gui
from engine.gui import gui, Button, Image, load_image, Label
from engine.initialize_engine import width, height

def init():
    global names_elements
    names_elements = []
    gui.add_element(Image((width//2, height//2), load_image("images/game_menu_gui/menu.png"), 'background'))
    names_elements.append('background')

    gui.add_element(Button((width//2, height//2-50),{
        'normal': 'images/button/normal.png',
        'hovered': 'images/button/hovered.png',
        'clicked': 'images/button/clicked.png'
    },'resume', deinit))
    names_elements.append('resume')
    gui.add_element(Label((width//2, height//2-50), 38, 'Resume', Color('white'), 'fonts/Dot.ttf', 'label_resume'))
    names_elements.append('label_resume')

    gui.add_element(Button((width // 2, height // 2 + 30), {
        'normal': 'images/button/normal.png',
        'hovered': 'images/button/hovered.png',
        'clicked': 'images/button/clicked.png'
    }, 'exit', exit_in_menu))
    names_elements.append('exit')
    gui.add_element(
        Label((width // 2, height // 2 + 30), 35, 'Exit in menu', Color('white'), 'fonts/Dot.ttf', 'label_exit'))
    names_elements.append('label_exit')

    gui.add_element(Button((width // 2, height // 2 + 85), {
        'normal': 'images/button/normal.png',
        'hovered': 'images/button/hovered.png',
        'clicked': 'images/button/clicked.png'
    }, 'exit_in_desktop', exit_in_menu))
    names_elements.append('exit_in_desktop')
    gui.add_element(
        Label((width // 2, height // 2 + 85), 31, 'Exit in desktop', Color('white'), 'fonts/Dot.ttf', 'label_exit_in_desktop'))
    names_elements.append('label_exit_in_desktop')

def deinit():
    global names_elements
    for _ in names_elements:
        gui.del_element(_)

    names_elements = []

def exit_in_menu():
    deinit()
    main_menu_gui.init()

def exit_in_desktop():
    main_menu_gui.my_exit()
