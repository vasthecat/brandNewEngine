from engine.game_objects import Camera


class SceneManager:
    def __init__(self):
        self.current_scene = None
        self.scenes = {}
        self.create_scene('default_scene', set_current=True)

    def create_scene(self, scene_name, camera=None, set_current=False):
        if camera is None:
            camera = Camera()
        self.scenes[scene_name] = Scene(scene_name, camera)
        if set_current:
            self.current_scene = self.scenes[scene_name]

    def rename_scene(self, old_name, new_name):
        scene = self.scenes.get(old_name, None)
        if scene is not None:
            if new_name not in self.scenes:
                self.scenes[new_name] = self.scenes[old_name]
                del self.scenes[old_name]
                scene.name = new_name

    def remove_scene(self, name):
        del self.scenes[name]


class Scene:
    def __init__(self, name, camera):
        self.name = name
        self.current_camera = camera
        self.cameras = [camera]
        self.objects = []

    def create_camera(self, x=0, y=0, set_current=False):
        camera = Camera(x, y)
        self.cameras.append(camera)
        if set_current:
            self.current_camera = camera

    def set_current_camera(self, index):
        self.current_camera = self.cameras[index]

    def add_object(self, game_obj):
        self.objects.append(game_obj)

    def find_objects(self, name):
        return list(filter(lambda obj: obj.name == name, self.objects))

    def update(self):
        for obj in self.objects:
            obj.update()
        for cam in self.cameras:
            cam.update()

    def render(self):
        for obj in self.objects:
            self.current_camera.draw(obj)


scene_manager = SceneManager()
