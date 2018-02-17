from engine.scene_manager import scene_manager
from engine.game_objects import GameObject
from engine.base_components import ImageFile
from user_components import PhysicsCollider, TriggerCollider, PlayerController, AnimationContoller, ParticleSystem
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
    'ImageFile': ImageFile.deserialize,
    'PlayerController': PlayerController.deserialize,
    'PhysicsCollider': PhysicsCollider.deserialize,
    'TriggerCollider': TriggerCollider.deserialize,
    'AnimationController': AnimationContoller.deserialize,
    'ParticleSystem': ParticleSystem.deserialize
}
