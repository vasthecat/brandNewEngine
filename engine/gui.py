import pygame


class Label:
    def __init__(self, rect, text, front_color, name, dict_with_func = None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font_color = front_color
        self.name = name

        self.font = pygame.font.Font(None, self.rect.height - 4)

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
    def __init__(self, rect, image, name, func):
        self.image = pygame.image.load(image).convert_alpha()

        self.name = name
        self.rect = pygame.Rect(rect[0], rect[1], self.image.get_size()[0], self.image.get_size()[1])
        self.func = func

    def render(self, surface):
        surface.blit(self.image, self.rect)

    def apply_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.func()


class Image:
    def __init__(self, rect, image, name):
        self.rect = rect
        self.image = pygame.image.load(image).convert_alpha()

        self.name = name
        size = self.image.get_size()
        self.rect = pygame.Rect(rect[0], rect[1], size[0], size[1])

    def render(self, surface):
        surface.blit(self.image, self.rect)


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


gui = GUI()