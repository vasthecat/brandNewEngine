from engine.scene_manager import SceneManager
from engine.game_objects import GameObject
from engine.base_components import ImageFile
from user_components import (PhysicsCollider, TriggerCollider, PlayerController, AnimationController, ParticleEmitter,
                             MusicController, NPCController, WaterSound, House1Trigger, House2Trigger,
                             TardisController, EnterVillageTrigger)
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
                component_loaders[component_dict['name']](component_dict, game_object)
            )

        scene.add_object(game_object)
    return scene


component_loaders = {
    'ImageFile': ImageFile.deserialize,
    'PlayerController': PlayerController.deserialize,
    'PhysicsCollider': PhysicsCollider.deserialize,
    'TriggerCollider': TriggerCollider.deserialize,
    'AnimationController': AnimationController.deserialize,
    'ParticleEmitter': ParticleEmitter.deserialize,
    'MusicController': MusicController.deserialize,
    'NPCController': NPCController.deserialize,
    'WaterSound': WaterSound.deserialize,
    'House1Trigger': House1Trigger.deserialize,
    'House2Trigger': House2Trigger.deserialize,
    'EnterVillageTrigger': EnterVillageTrigger.deserialize,
    'TardisController': TardisController.deserialize,
}
