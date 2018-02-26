from engine.game_objects import Camera


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

    def remove_object(self, game_obj):
        self.objects.remove(game_obj)

    def find_object(self, name):
        try:
            return next(self.find_objects(name))
        except StopIteration:
            return None

    def find_objects(self, name):
        for obj in self.objects:
            if obj.name == name:
                yield obj

    def update(self):
        for obj in self.objects:
            obj.update()
        for cam in self.cameras:
            cam.update()

    def render(self):
        self.current_camera.draw(self.objects)


class SceneManager:
    current_scene = Scene('default_scene', Camera())
    scenes = {'default_scene': current_scene}

    @staticmethod
    def set_current(name):
        scene = SceneManager.scenes.get(name, None)
        if scene is not None:
            SceneManager.current_scene = scene

    @staticmethod
    def create_scene(scene_name, camera=None, set_current=False):
        if camera is None:
            camera = Camera()
        SceneManager.scenes[scene_name] = Scene(scene_name, camera)
        if set_current:
            SceneManager.current_scene = SceneManager.scenes[scene_name]

    @staticmethod
    def rename_scene(old_name, new_name):
        scene = SceneManager.scenes.get(old_name, None)
        if scene is not None:
            if new_name not in SceneManager.scenes:
                SceneManager.scenes[new_name] = SceneManager.scenes[old_name]
                del SceneManager.scenes[old_name]
                scene.name = new_name

    @staticmethod
    def remove_scene(name):
        del SceneManager.scenes[name]
