import engine.initialize_engine

import pygame
import sys

from scene_loader import load_scene
from engine.input_manager import input_manager
from engine.gui import GUI, Label


scene = load_scene('scenes/scene1.json')

gui = GUI()
gui.add_element(Label((10, 50, 300, 80), "Huge text", pygame.Color('green')))
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    input_manager.update()

    for event in input_manager.get_events():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    scene.update()
    scene.render()

    gui.apply_event(input_manager.get_events())
    gui.update()
    gui.render()

    pygame.display.flip()