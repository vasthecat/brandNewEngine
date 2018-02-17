import pygame
from engine.initialize_engine import width, height
from random import randint, choice


def load_image(path):
    return pygame.image.load(path).convert_alpha()


class Label:
    def __init__(self, rect, text, front_color, path_font,name, dict_with_func = None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font_color = front_color
        self.name = name

        self.font = pygame.font.Font(path_font, self.rect.height - 4)

        self.key_and_func = dict_with_func

    def render(self, surface):
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        surface.blit(self.rendered_text, self.rendered_rect)

    def apply_event(self, event):
        if self.key_and_func is not None:
            for key, func in self.key_and_func.items():
                if event.type == pygame.KEYDOWN:
                    if event.key == key:
                        func()


class Button:
    def __init__(self, pos, image_states, name, func=lambda: None):
        self.normal_image = load_image(image_states['normal'])
        self.hover_image = load_image(image_states['hovered'])
        self.click_image = load_image(image_states['clicked'])

        self.pos = pos

        self.image = self.normal_image

        self.name = name
        self.func = func

        self.states = {
            'hovered': False,
            'clicked': False,
            'after_click': False
        }

    def update(self, *args):
        if self.states['clicked']:
            self.states['clicked'] = False
            self.image = self.click_image
            self.states['after_click'] = True
        elif self.states['after_click']:
            if self.states['hovered']:
                self.image = self.click_image
            else:
                self.states['after_click'] = False

        elif self.states['hovered']:
            self.image = self.hover_image

        else:
            self.image = self.normal_image

    def render(self, surface):
        surface.blit(self.image, self.image.get_rect(center=self.pos))

    def apply_event(self, event):
        self.states['hovered'] = self.image.get_rect(center=self.pos).collidepoint(*pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.states['hovered']:
                    self.states['clicked'] = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.states['hovered']:
                    self.states['after_click'] = False
                    self.func()


class Image:
    def __init__(self, rect, image, name):
        self.image = pygame.image.load(image).convert_alpha()

        self.name = name
        self.size = self.image.get_size()
        self.rect = pygame.Rect(rect[0], rect[1], self.size[0], self.size[1])
        self.const_rect = self.rect.copy()
        self.const_rect.x = -self.size[0]

    def render(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, x, y):
        self.rect[0] += x
        self.rect[1] += y

    def get_pos(self):
        return (self.rect[0], self.rect[1])

    def set_const_pos(self):
        self.const_rect.y = randint(0, height-self.size[1])
        self.rect = self.const_rect.copy()

class CloudsController:
    def __init__(self, name, chance_pos):
        self.name = name
        self.chance_pos = chance_pos
        self.elements = []

    def add_element(self, element):
        _ = choice(range(0, 2))
        if _:
            self.elements.append({'element':element, 'shag': (-self.chance_pos[0], self.chance_pos[1])})
            element.const_rect.x = width
        else:
            self.elements.append({'element': element, 'shag': (self.chance_pos[0], self.chance_pos[1])})

    def update(self):
        for element in self.elements:
            x = element['shag'][0]
            y = element['shag'][1]
            element['element'].move(x, y)
            if element['element'].get_pos()[0] > width or element['element'].get_pos()[1] > height \
                    or element['element'].get_pos()[0]+ element['element'].size[0]< 0 \
                    or element['element'].get_pos()[1] + element['element'].size[1] < 0 :
                element['element'].set_const_pos()

    def render(self, surface):
        for element in self.elements:
            surface.blit(element['element'].image, element['element'].rect)


class GUI:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        if all(map(lambda elem: elem.name != element.name, self.elements)):
            self.elements.append(element)

    def render(self):
        for element in self.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(pygame.display.get_surface())

    def update(self):
        for element in self.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()

    def apply_event(self, event):
        for element in self.elements:
            get_event = getattr(element, "apply_event", None)
            if callable(get_event):
                element.apply_event(event)

    def del_element(self, name):
        for element in self.elements:
            if element.name == name:
                self.elements.remove(element)

    def clear(self):
        self.elements = []


gui = GUI()