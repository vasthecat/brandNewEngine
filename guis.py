from engine.gui import gui, load_image, Label, Image
from engine.initialize_engine import width, height

from scene_loader import load_scene
from gui_misc import CloudsController, MedievalButton

from pygame import Color
import pygame
import sys


class MainMenuGUI:
    @staticmethod
    def start_game():
        load_scene('scenes/scene1.json')
        gui.clear()
        GameGUI.init()

    @staticmethod
    def exit():
        pygame.quit()
        sys.exit()

    @staticmethod
    def init():
        clouds_controller = CloudsController('Con', [1, 0])
        CloudsController.generate_clouds(15, clouds_controller)

        gui.add_element(Image((width // 2, height // 2), pygame.transform.scale(
            load_image('images/sky.png'), (width, height)
        ), 'sky'))
        gui.add_element(clouds_controller)

        gui.add_element(Image((width // 2, 75), load_image('images/title_bg.png'), 'title'))
        gui.add_element(
            Label((width // 2, 159), 53, 'Untitled game', Color('white'), 'fonts/Dot.ttf', 'title_text'))

        gui.add_element(MedievalButton((width // 2, height // 2), 'start_game', MainMenuGUI.start_game))
        gui.add_element(
            Label((width // 2, height // 2), 38, "Start game", Color('white'), 'fonts/Dot.ttf', 'label_game'))

        gui.add_element(MedievalButton((width // 2, height // 2 + 100), 'exit', MainMenuGUI.exit))
        gui.add_element(
            Label((width // 2, height // 2 + 100), 38, "Exit", Color('white'), 'fonts/Dot.ttf', 'label_exit'))


class GameGUI:
    pause_menu_elements = set()

    @staticmethod
    def exit_in_menu():
        gui.clear()
        load_scene('scenes/main_menu.json')
        MainMenuGUI.init()

    @staticmethod
    def pause_menu_clear():
        for _ in GameGUI.pause_menu_elements:
            gui.del_element(_)

        GameGUI.pause_menu_elements.clear()

    @staticmethod
    def create_menu():
        gui.add_element(Image((width // 2, height // 2), load_image("images/game_menu_gui/menu.png"), 'background'))
        GameGUI.pause_menu_elements.add('background')

        gui.add_element(MedievalButton((width // 2, height // 2 - 50), 'resume', GameGUI.pause_menu_clear))
        GameGUI.pause_menu_elements.add('resume')
        gui.add_element(Label(
            (width // 2, height // 2 - 50), 38, 'Resume', Color('white'), 'fonts/Dot.ttf', 'label_resume')
        )
        GameGUI.pause_menu_elements.add('label_resume')

        gui.add_element(MedievalButton((width // 2, height // 2 + 30), 'exit', GameGUI.exit_in_menu))
        GameGUI.pause_menu_elements.add('exit')
        gui.add_element(
            Label((width // 2, height // 2 + 30), 35, 'Exit in menu', Color('white'), 'fonts/Dot.ttf', 'label_exit'))
        GameGUI.pause_menu_elements.add('label_exit')

        gui.add_element(MedievalButton((width // 2, height // 2 + 85), 'exit_in_desktop', MainMenuGUI.exit))
        GameGUI.pause_menu_elements.add('exit_in_desktop')
        gui.add_element(
            Label((width // 2, height // 2 + 85), 31, 'Exit in desktop', Color('white'), 'fonts/Dot.ttf',
                  'label_exit_in_desktop'))
        GameGUI.pause_menu_elements.add('label_exit_in_desktop')

    @staticmethod
    def init():
        gui.add_element(MedievalButton((width // 2, height - 35), 'game_menu', GameGUI.create_menu))
        gui.add_element(
            Label((width // 2, height - 35), 38, "Menu", Color('white'), 'fonts/Dot.ttf', 'label_game_menu'))
