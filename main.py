import engine.initialize_engine
from engine.scene_manager import scene_manager

import pygame
import sys

from engine.input_manager import input_manager
from scene_loader import load_scene
from engine.gui import gui, Label
import main_menu_gui

load_scene('scenes/main_menu.json')
main_menu_gui.init()

gui.add_element(Label((50, 25), 50, '0', pygame.Color('red'), 'fonts/Dot.ttf', 'fps_label'))

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

    elem = gui.get_element('fps_label')
    if elem is not None:
        elem.text = str(round(clock.get_fps(), 1))
    gui.update()
    gui.render()

    pygame.display.flip()
