from engine.scene_manager import SceneManager
from engine.game_objects import GameObject
from engine.serialization_manager import serializable_types

import json
import pygame


def load_scene(path):
    pygame.mixer.stop()
    with open(path, encoding='utf-8') as f:
        scene_dict = json.load(f)

    SceneManager.create_scene(scene_dict['name'], set_current=True)
    scene = SceneManager.current_scene

    for obj in scene_dict['objects']:
        game_object = GameObject(
            obj.get('x', 0), obj.get('y', 0),
            obj.get('name', 'NewObject')
        )

        for component_dict in obj['components']:
            game_object.add_component(
                serializable_types[component_dict['name']].deserialize(component_dict, game_object)
            )

        scene.add_object(game_object)
    return scene
