from engine.gui import load_image, Image, Button
from random import randint
from engine.initialize_engine import width, height


class CloudsController:
    def __init__(self, name, change_pos):
        self.name = name
        self.change_pos = change_pos
        self.elements = []

    @staticmethod
    def generate_clouds(n_clouds, clouds_controller):
        for _ in range(n_clouds):
            x, y = randint(-100, 700), randint(0, height)
            i = str(randint(1, 7))
            clouds_controller.add_element(
                Image((x, y), load_image(
                    'images/clouds/cloud{}.png'.format(i)), 'cloud{}'.format(i))
            )

    def add_element(self, element):
        if randint(0, 1):
            self.elements.append({'element': element, 'step': (-self.change_pos[0], self.change_pos[1])})
            element.const_rect.x = width
        else:
            self.elements.append({'element': element, 'step': (self.change_pos[0], self.change_pos[1])})

    def update(self):
        for element in self.elements:
            element['element'].move(*element['step'])
            if element['element'].get_pos()[0] > width or element['element'].get_pos()[1] > height \
                    or element['element'].get_pos()[0] + element['element'].size[0] < 0 \
                    or element['element'].get_pos()[1] + element['element'].size[1] < 0:
                element['element'].set_const_pos()

    def render(self, surface):
        for element in self.elements:
            surface.blit(element['element'].image, element['element'].rect)


class MedievalButton(Button):
    def __init__(self, pos, name, func=lambda: None):
        super().__init__(pos, {
            'normal': 'images/button/normal.png',
            'hovered': 'images/button/hovered.png',
            'clicked': 'images/button/clicked.png'
        }, name, func)