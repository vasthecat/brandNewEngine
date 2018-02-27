from engine.initialize_engine import Config
from engine.scene_manager import SceneManager

import pygame
import sys

from engine.input_manager import InputManager
from engine.save_manager import SaveManager
from scene_loader import load_scene
from engine.gui import GUI
from guis import MainMenuGUI

SaveManager.load_profile('preferences', 'user_prefs.json')
Config.set_resolution(*SaveManager.get_entry('preferences', 'resolution'))
Config.set_fullscreen(SaveManager.get_entry('preferences', 'fullscreen'))

InputManager.add_axis('Horizontal', {
    SaveManager.get_entry('preferences', 'right'): 1,
    SaveManager.get_entry('preferences', 'left'): -1,
})

InputManager.add_axis('Vertical', {
    SaveManager.get_entry('preferences', 'up'): 1,
    SaveManager.get_entry('preferences', 'down'): -1,
})

load_scene('scenes/main_menu.json')
MainMenuGUI.init()

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    InputManager.update()

    for event in InputManager.get_events():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            SaveManager.save_profile('preferences', 'user_prefs.json')
            pygame.quit()
            sys.exit()

        GUI.apply_event(event)

    SceneManager.current_scene.update()
    SceneManager.current_scene.render()

    GUI.update()
    GUI.render()

    pygame.display.flip()
