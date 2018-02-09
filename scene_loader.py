from engine.scene_manager import scene_manager
from engine.game_objects import GameObject
from user_components import ImageComponent, PhysicsCollider, TriggerCollider, PlayerController
import json


def _load_image_component(component_dict, obj):
    return ImageComponent(component_dict['path'], obj)


def _load_physics_collider(component_dict, obj):
    return PhysicsCollider(
        component_dict['shift_x'], component_dict['shift_y'],
        component_dict['rect'], obj
    )


def _load_npc_collider(component_dict, obj):
    return TriggerCollider(
        component_dict['shift_x'], component_dict['shift_y'],
        component_dict['rect'], obj
    )


def _load_player_controller(component_dict, obj):
    return PlayerController(component_dict['speed'], obj)


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
            component_name = component_dict['name']
            game_object.add_component(component_loaders[component_name](component_dict, game_object))
        scene.add_object(game_object)
    return scene


component_loaders = {
    'ImageComponent': _load_image_component,
    'PlayerController': _load_player_controller,
    'PhysicsCollider': _load_physics_collider,
    'TriggerCollider': _load_npc_collider,
}
