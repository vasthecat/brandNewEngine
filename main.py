import engine.initialize_engine

import pygame
import sys

from engine.game_objects import Sprite
from user_components import ControllerComponent
from engine.scene_manager import scene_manager
from engine.input_manager import input_manager

scene_manager.rename_scene('default_scene', 'scene1')
scene = scene_manager.current_scene
input_manager.add_axis('Rotation', {
    pygame.K_q: -1,
    pygame.K_e: 1,
})

obj = Sprite('images/image.png')
scene.add_object(0, 0, obj)

obj.add_component(ControllerComponent(obj))

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
    pygame.display.flip()
