from pygame.locals import *
import pygame


class Label:
    def __init__(self, rect, text, front_color, name):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font_color = front_color
        self.name = name

        self.font = pygame.font.Font(None, self.rect.height - 4)
        self.rendered_text = None
        self.rendered_rect = None


    def render(self, surface):
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        surface.blit(self.rendered_text, self.rendered_rect)


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
            get_event = getattr(element, "get_event", None)
            if callable(get_event):
                element.apply_event(event)

    def del_element(self, name):
        for element in self.elements:
            if element.name == name:
                self.elements.remove(element)

gui = GUI()
