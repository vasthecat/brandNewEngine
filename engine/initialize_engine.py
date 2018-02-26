import pygame
from engine.save_manager import SaveManager

config = SaveManager.load_profile('config', 'config.json')

pygame.init()
pygame.display.set_caption(config.get('title'))
width, height = resolution = config.get('resolution')
pygame.display.set_mode(resolution, pygame.FULLSCREEN if config.get('fullscreen') else 0)
