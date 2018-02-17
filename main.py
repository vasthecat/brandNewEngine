import engine.initialize_engine
from engine.scene_manager import scene_manager

import pygame
import sys

from engine.input_manager import input_manager
from engine.gui import gui
import main_menu_gui

main_menu_gui.init()

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    input_manager.update()

    for event in input_manager.get_events():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

        gui.apply_event(event)

    scene_manager.current_scene.update()
    scene_manager.current_scene.render()

    gui.update()
    gui.render()

    pygame.display.flip()
