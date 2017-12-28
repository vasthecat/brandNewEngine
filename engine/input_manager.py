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

    def __init__(self):
        self.subscribers = []
        self.events = []

    def get_axis(self, name):
        axis = InputManager.AXES.get(name, None)
        if axis is not None:
            return sum(val for key, val in axis.items() if pygame.key.get_pressed()[key])

    def get_mouse_pos(self):
        return pygame.mouse.get_pos()

    def add_axis(self, name, keys):
        InputManager.AXES[name] = keys

    def get_events(self):
        return self.events

    def update(self):
        self.events = list(pygame.event.get())


input_manager = InputManager()
