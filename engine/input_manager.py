import pygame


class InputManager:
    AXES = {
        'Horizontal': {
            pygame.K_a: -1,
            pygame.K_d: 1,
        },
        'Vertical': {
            pygame.K_w: 1,
            pygame.K_s: -1,
        },
    }

    _events = []
    _clock = pygame.time.Clock()
    _fps = 60
    _delta_tick = _clock.tick(_fps)

    @staticmethod
    def get_axis(name):
        axis = InputManager.AXES.get(name, None)
        if axis is not None:
            return sum(val for key, val in axis.items() if pygame.key.get_pressed()[key])

    @staticmethod
    def get_mouse_pos():
        return pygame.mouse.get_pos()

    @staticmethod
    def set_axis(name, keys):
        InputManager.AXES[name] = keys

    @staticmethod
    def set_max_fps(value):
        InputManager._fps = value

    @staticmethod
    def get_fps():
        return int(InputManager._clock.get_fps())

    @staticmethod
    def get_events():
        return InputManager._events

    @staticmethod
    def get_delta_tick():
        return InputManager._delta_tick

    @staticmethod
    def get_ticks():
        return pygame.time.get_ticks()

    @staticmethod
    def update():
        InputManager._events = list(pygame.event.get())
        InputManager._delta_tick = InputManager._clock.tick(InputManager._fps)
