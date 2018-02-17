import engine.initialize_engine

import pygame
import sys

from scene_loader import load_scene
from engine.input_manager import input_manager
from engine.gui import gui, Button, Image, Label


scene = load_scene('scenes/scene1.json')

def a():
    print('Press button')

gui.add_element(Button((200, 50), {'normal': 'images/normal.png', 'hovered':'images/hovered.png', 'clicked': 'images/clicked.png'}, 'but1', a))

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    input_manager.update()

    for event in input_manager.get_events():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        gui.apply_event(event)

    scene.update()
    scene.render()

    gui.update()
    gui.render()

    pygame.display.flip()