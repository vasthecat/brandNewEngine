import engine.initialize_engine

import pygame
import sys

from engine.game_objects import GameObject
from engine.base_components import ImageComponent
from user_components import PhysicsCollider, TriggerCollider, PlayerController
from engine.scene_manager import scene_manager
from engine.input_manager import input_manager

scene = scene_manager.current_scene

bg = GameObject()
bg.add_component(ImageComponent('images/ground.png', bg))
scene.add_object(bg)

house1 = GameObject(-1428, 1123)
house1.add_component(ImageComponent('images/house.png', house1))
house1.add_component(PhysicsCollider(
    0, 0,
    house1.get_component(ImageComponent).image.get_rect(),
    house1
))
scene.add_object(house1)

player = GameObject()
player.add_component(ImageComponent('images/player.png', player))
player.add_component(PhysicsCollider(0, -64, [0, 0, 64, 20], player))
player.add_component(TriggerCollider(64, -32, [0, 0, 64, 128], player))
player.add_component(PlayerController(10, player))
scene.add_object(player)

house2 = GameObject(-1500, -500)
house2.add_component(ImageComponent('images/house_back.png', house2))
scene.add_object(house2)

obj = GameObject()
obj.add_component(TriggerCollider(0, 0, [0, 0, 100, 100], obj))
scene.add_object(obj)

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