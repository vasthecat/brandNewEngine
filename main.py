import engine.initialize_engine
from engine.scene_manager import SceneManager

import pygame
import sys

from engine.input_manager import InputManager
from scene_loader import load_scene
from engine.gui import GUI
from guis import MainMenuGUI

load_scene('scenes/main_menu.json')
MainMenuGUI.init()

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    InputManager.update()

    for event in InputManager.get_events():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

        GUI.apply_event(event)

    SceneManager.current_scene.update()
    SceneManager.current_scene.render()

    GUI.update()
    GUI.render()

    pygame.display.flip()
