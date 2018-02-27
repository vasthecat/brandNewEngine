from engine.gui import GUI, load_image, Label, Image
from engine.initialize_engine import Config
from engine.save_manager import SaveManager

from scene_loader import load_scene
from gui_misc import CloudsController, MedievalButton, MedievalCheckbox

from pygame import Color
import pygame


class MainMenuGUI:
    @staticmethod
    def start_game():
        load_scene('scenes/scene1.json')
        SaveManager.add_profile('village1', {'seen_tardis': False})
        GUI.clear()
        GameGUI.init()

    @staticmethod
    def load_settings():
        MainMenuGUI.remove_buttons()
        SettingsGUI.init()

    @staticmethod
    def exit():
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    @staticmethod
    def add_buttons():
        GUI.add_element(MedievalButton(
            (Config.get_width() // 2, Config.get_height() // 2),
            'Start game', 35, 'start_game', MainMenuGUI.start_game
        ))

        GUI.add_element(MedievalButton(
            (Config.get_width() // 2, Config.get_height() // 2 + 75),
            'Settings', 35, 'settings', MainMenuGUI.load_settings
        ))

        GUI.add_element(MedievalButton(
            (Config.get_width() // 2, Config.get_height() // 2 + 150),
            'Exit', 35, 'exit', MainMenuGUI.exit
        ))

    @staticmethod
    def remove_buttons():
        GUI.del_element('start_game')
        GUI.del_element('settings')
        GUI.del_element('exit')

    @staticmethod
    def init():
        clouds_controller = CloudsController('Con', [1, 0])
        CloudsController.generate_clouds(15, clouds_controller)

        GUI.add_element(Image((Config.get_width() // 2, Config.get_height() // 2), pygame.transform.scale(
            load_image('images/main_menu/sky.png'), (Config.get_width(), Config.get_height())
        ), 'sky'))
        GUI.add_element(clouds_controller)

        GUI.add_element(Image((Config.get_width() // 2, 75), load_image('images/main_menu/title_bg.png'), 'title'))
        GUI.add_element(Label(
            (Config.get_width() // 2, 159), 53, 'Untitled game',
            Color('white'), 'fonts/Dot.ttf', 'title_text'
        ))

        MainMenuGUI.add_buttons()


class SettingsGUI:
    @staticmethod
    def exit():
        SettingsGUI.clear()
        MainMenuGUI.init()

    @staticmethod
    def clear():
        GUI.del_element(
            'lbl_change_keys', 'btn_mvup', 'btn_mvdown', 'btn_mvleft', 'btn_mvright',
            'lbl_set_resolution', 'btn_res1080p', 'btn_res_wxga+', 'btn_res_wxga', 'btn_res_720p', 'btn_res_xga',
            'bg_img', 'toggle_fullscreen', 'close_settings',
        )

    @staticmethod
    def toggle_fullscreen(value):
        SaveManager.set_entry('preferences', 'fullscreen', value)
        Config.set_fullscreen(value)

    @staticmethod
    def add_move_buttons():
        x = 230
        y = 280

        GUI.add_element(Label(
            (Config.get_width() // 2 - x, Config.get_height() // 2 - y + 75), 32, 'Change control keys',
            pygame.Color('white'), 'fonts/Dot.ttf', 'lbl_change_keys'
        ))

        GUI.add_element(MedievalButton(
            (Config.get_width() // 2 - x, Config.get_height() // 2 - y + 75 * 2),
            'Move up: {}'.format(
                pygame.key.name(SaveManager.get_entry('preferences', 'up'))
            ), 29, 'btn_mvup'
        ))

        GUI.add_element(MedievalButton(
            (Config.get_width() // 2 - x, Config.get_height() // 2 - y + 75 * 3),
            'Move down: {}'.format(
                pygame.key.name(SaveManager.get_entry('preferences', 'down'))
            ), 29, 'btn_mvdown'
        ))

        GUI.add_element(MedievalButton(
            (Config.get_width() // 2 - x, Config.get_height() // 2 - y + 75 * 4),
            'Move left: {}'.format(
                pygame.key.name(SaveManager.get_entry('preferences', 'left'))
            ), 29, 'btn_mvleft'
        ))

        GUI.add_element(MedievalButton(
            (Config.get_width() // 2 - x, Config.get_height() // 2 - y + 75 * 5),
            'Move right: {}'.format(
                pygame.key.name(SaveManager.get_entry('preferences', 'right'))
            ), 29, 'btn_mvright'
        ))

    @staticmethod
    def add_resolutions_buttons():
        x = 230
        y = 280

        GUI.add_element(Label(
            (Config.get_width() // 2 + x, Config.get_height() // 2 - y + 75), 32, 'Set display resolution',
            pygame.Color('white'), 'fonts/Dot.ttf', 'lbl_set_resolution'
        ))

        GUI.add_element(MedievalButton(
            (Config.get_width() // 2 + x, Config.get_height() // 2 - y + 75 * 2),
            '1920x1080', 29, 'btn_res1080p', SettingsGUI.set_resolution, 1920, 1080
        ))

        GUI.add_element(MedievalButton(
            (Config.get_width() // 2 + x, Config.get_height() // 2 - y + 75 * 3),
            '1440x900', 29, 'btn_res_wxga+', SettingsGUI.set_resolution, 1440, 900
        ))

        GUI.add_element(MedievalButton(
            (Config.get_width() // 2 + x, Config.get_height() // 2 - y + 75 * 4),
            '1366x768', 29, 'btn_res_wxga', SettingsGUI.set_resolution, 1366, 768
        ))

        GUI.add_element(MedievalButton(
            (Config.get_width() // 2 + x, Config.get_height() // 2 - y + 75 * 5),
            '1280x720', 29, 'btn_res_720p', SettingsGUI.set_resolution, 1280, 720
        ))

        GUI.add_element(MedievalButton(
            (Config.get_width() // 2 + x, Config.get_height() // 2 - y + 75 * 6),
            '1024x768', 29, 'btn_res_xga', SettingsGUI.set_resolution, 1024, 768
        ))

    @staticmethod
    def set_resolution(width, height):
        Config.set_resolution(width, height)
        SaveManager.set_entry('preferences', 'resolution', [width, height])
        GUI.clear()
        MainMenuGUI.init()
        MainMenuGUI.remove_buttons()
        SettingsGUI.init()

    @staticmethod
    def init():
        GUI.add_element(Image(
            (Config.get_width() // 2, Config.get_height() // 2 + 40),
            load_image('images/bg.png'), 'bg_img')
        )

        SettingsGUI.add_move_buttons()
        SettingsGUI.add_resolutions_buttons()

        GUI.add_element(MedievalCheckbox(
            'toggle_fullscreen', (Config.get_width() // 2 + 230, Config.get_height() // 2 - 280 + 525),
            'Toggle Fullscreen', 29, SaveManager.get_entry('preferences', 'fullscreen'),
            SettingsGUI.toggle_fullscreen
        ))
        GUI.add_element(MedievalButton(
            (Config.get_width() // 2, Config.get_height() // 2 + 280),
            'Close', 29, 'close_settings', SettingsGUI.exit
        ))


class GameGUI:
    pause_menu_elements = set()

    @staticmethod
    def exit_in_menu():
        GUI.clear()
        load_scene('scenes/main_menu.json')
        MainMenuGUI.init()

    @staticmethod
    def pause_menu_clear():
        for _ in GameGUI.pause_menu_elements:
            GUI.del_element(_)

        GameGUI.pause_menu_elements.clear()
        GUI.get_element('game_menu').func = GameGUI.create_menu

    @staticmethod
    def create_menu():
        GUI.get_element('game_menu').func = GameGUI.pause_menu_clear

        GUI.add_element(Image((Config.get_width() // 2, Config.get_height() // 2), load_image("images/game_menu_gui/menu.png"), 'background'))
        GameGUI.pause_menu_elements.add('background')

        GUI.add_element(MedievalButton((Config.get_width() // 2, Config.get_height() // 2 - 50), 'Resume', 35, 'resume', GameGUI.pause_menu_clear))
        GameGUI.pause_menu_elements.add('resume')

        GUI.add_element(MedievalButton((Config.get_width() // 2, Config.get_height() // 2 + 20), 'Exit in menu', 33, 'exit', GameGUI.exit_in_menu))
        GameGUI.pause_menu_elements.add('exit')

        GUI.add_element(MedievalButton((Config.get_width() // 2, Config.get_height() // 2 + 90), 'Exit in desktop', 29, 'exit_in_desktop', MainMenuGUI.exit))
        GameGUI.pause_menu_elements.add('exit_in_desktop')

    @staticmethod
    def init():
        GUI.add_element(MedievalButton((Config.get_width() // 2, Config.get_height() - 35), 'Menu', 35, 'game_menu', GameGUI.create_menu))
