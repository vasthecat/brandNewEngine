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

    @staticmethod
    def get_axis(name):
        axis = InputManager.AXES.get(name, None)
        if axis is not None:
            return sum(val for key, val in axis.items() if pygame.key.get_pressed()[key])

    @staticmethod
    def get_mouse_pos():
        return pygame.mouse.get_pos()

    @staticmethod
    def add_axis(name, keys):
        InputManager.AXES[name] = keys

    @staticmethod
    def get_events():
        return InputManager.events

    @staticmethod
    def update():
        InputManager.events = list(pygame.event.get())
