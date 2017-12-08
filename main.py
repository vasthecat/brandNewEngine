from initialize_engine import scene_manager
from game_objects import Sprite
import pygame
import sys


scene_manager.rename_scene('default_scene', 'scene1')
scene = scene_manager.current_scene

cam = scene.current_camera
scene.create_camera()

scene.add_object(0, 0, Sprite('image.png'))
scene.add_object(50, 50, Sprite('image.png'))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                cam.move(0, 100)
            elif event.key == pygame.K_s:
                cam.move(0, -100)
            elif event.key == pygame.K_d:
                cam.move(100, 0)
            elif event.key == pygame.K_a:
                cam.move(-100, 0)
            elif event.key == pygame.K_k:
                scene.set_current_camera(1)
                cam = scene.current_camera
            elif event.key == pygame.K_l:
                scene.set_current_camera(0)
                cam = scene.current_camera

    scene.render()
    pygame.display.flip()
