from engine.scene_manager import scene_manager
from engine.game_objects import GameObject
from user_components import ImageComponent, PhysicsCollider, TriggerCollider, PlayerController
import json


def load_scene(path):
    with open(path, encoding='utf-8') as f:
        scene_dict = json.load(f)

    scene_manager.create_scene(scene_dict['name'], set_current=True)
    scene = scene_manager.current_scene

    for obj in scene_dict['objects']:
        game_object = GameObject(
            obj.get('x', 0), obj.get('y', 0),
            obj.get('name', 'NewObject')
        )

        for component_dict in obj['components']:
            game_object.add_component(
                component_loaders[component_dict['name']](component_dict, game_object)
            )

        scene.add_object(game_object)
    return scene


component_loaders = {
    'ImageComponent': ImageComponent.deserialize,
    'PlayerController': PlayerController.deserialize,
    'PhysicsCollider': PhysicsCollider.deserialize,
    'TriggerCollider': TriggerCollider.deserialize,
}
