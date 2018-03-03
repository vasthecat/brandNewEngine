import pygame
from engine.save_manager import SaveManager
from engine.input_manager import InputManager

pygame.init()


class Config:
    SaveManager.load_profile('config', 'config.json')

    @staticmethod
    def init():
        pygame.display.set_mode(SaveManager.get_entry('config', 'resolution'), Config.get_flags())
        pygame.display.set_caption(SaveManager.get_entry('config', 'title'))
        if SaveManager.has_entry('config', 'icon'):
            Config.set_icon(SaveManager.get_entry('config', 'icon'))

    @staticmethod
    def get_flags():
        flags = 0
        if SaveManager.get_entry('config', 'fullscreen'):
            flags |= pygame.FULLSCREEN
        return flags

    @staticmethod
    def set_caption(text):
        SaveManager.set_entry('config', 'title', text)
        return text

    @staticmethod
    def get_caption():
        return SaveManager.get_entry('config', 'title')

    @staticmethod
    def set_resolution(width, height):
        SaveManager.set_entry('config', 'resolution', [width, height])
        pygame.display.set_mode((width, height), Config.get_flags())
        return width, height

    @staticmethod
    def get_resolution():
        return SaveManager.get_entry('config', 'resolution')

    @staticmethod
    def set_width(width):
        SaveManager.set_entry('config', 'resolution', [width, Config.get_height()])

    @staticmethod
    def set_height(height):
        SaveManager.set_entry('config', 'resolution', [Config.get_width(), height])

    @staticmethod
    def get_width():
        return SaveManager.get_entry('config', 'resolution')[0]

    @staticmethod
    def get_height():
        return SaveManager.get_entry('config', 'resolution')[1]

    @staticmethod
    def set_fullscreen(value):
        SaveManager.set_entry('config', 'fullscreen', value)
        pygame.display.set_mode(SaveManager.get_entry('config', 'resolution'), Config.get_flags())
        return value

    @staticmethod
    def set_icon(path):
        SaveManager.set_entry('config', 'icon', path)
        pygame.display.set_icon(pygame.image.load(path).convert_alpha())


InputManager.set_max_fps(SaveManager.get_entry('config', 'fps'))
Config.init()
