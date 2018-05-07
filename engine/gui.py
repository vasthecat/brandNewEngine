import pygame
from engine.initialize_engine import Config
from random import randint
from pygame import Color


def load_image(path):
    return pygame.image.load(path).convert_alpha()


class Label:
    def __init__(self, pos, size, text, front_color, path_font, name):
        self.pos = pos
        self.size = size
        self.text = text
        self.font_color = front_color
        self.name = name

        self.font = pygame.font.Font(path_font, size)

    def render(self, surface):
        rendered_text = self.font.render(self.text, 1, self.font_color)
        rendered_rect = rendered_text.get_rect(center=self.pos)
        surface.blit(rendered_text, rendered_rect)


class Element:
    def __init__(self, pos=(0, 0), size=(1, 1)):
        self.rect = pygame.Rect(pos, size)
        self.name = ''

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def apply_event(self, event):
        pass

    def update(self):
        pass

    def render(self, surface):
        pass

class LabelForTextBox(Element):
    def __init__(self, rect, text):
        super().__init__()

        self.rect = pygame.Rect(rect)
        self.text = text
        self.bgcolor = pygame.Color("white")
        self.font_color = (77, 81, 83)
        self.font = pygame.font.Font(None, self.rect.height - 4)
        self.rendered_text = None
        self.rendered_rect = None

    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        surface.blit(self.rendered_text, self.rendered_rect)

class TextBox(LabelForTextBox):
    def __init__(self, rect, text, max_len=None, default_text='', name=''):
        super().__init__(rect, text)
        self.active = False
        self.blink = True
        self.blink_timer = 0
        self.caret = 0

        self.rect.center = (rect[0], rect[1])

        self.flag_first_active = True
        self.default_text = default_text

        self.max_len = max_len

        self.text = self.default_text

        self.name = name

    def apply_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:

            if event.key == pygame.K_BACKSPACE:
                if len(self.text) > 0 and self.caret != 0:
                    self.text = self.text[:self.caret - 1] + self.text[self.caret:]
                    if self.caret > 0:
                        self.caret -= 1

            else:
                if self.font.render(self.text + event.unicode, 1, self.font_color).get_rect().w < self.rect.w:
                    self.text = self.text[:self.caret] + event.unicode + self.text[self.caret:]
                    self.caret += 1
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                self.active = self.rect.collidepoint(event.pos)
                if self.active:
                    if len(self.text) > 0 and self.text != self.default_text:
                        self.caret = (event.pos[0] - self.rect.x) // (self.rendered_rect.width // len(self.text))
                        if self.caret >= len(self.text):
                            self.caret = len(self.text)
                    else:
                        self.caret = 0

    def update(self):
        if self.active and self.flag_first_active:
            self.flag_first_active = False
            self.text = ''
            self.caret = 0

        elif not self.active and not self.flag_first_active and self.text == '':
            self.flag_first_active = True
            self.text = self.default_text
            self.caret = 0

        if pygame.time.get_ticks() - self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()

    def render(self, surface):
        super(TextBox, self).render(surface)
        w = self.rect.x + self.font.render(self.text[:self.caret], 1, self.font_color).get_rect().width

        pygame.draw.line(surface, Color('gray'), (self.rect.x, self.rect.y), (self.rect.x, self.rect.y + self.rect.h),
                         2)
        pygame.draw.line(surface, Color('gray'), (self.rect.x, self.rect.y + self.rect.h),
                         (self.rect.x + self.rect.w, self.rect.y + self.rect.h), 2)
        pygame.draw.line(surface, Color('gray'), (self.rect.x + self.rect.w, self.rect.y),
                         (self.rect.x + self.rect.w, self.rect.y + self.rect.h), 2)
        pygame.draw.line(surface, Color('gray'), (self.rect.x, self.rect.y), (self.rect.x + self.rect.w, self.rect.y),
                         2)

        if self.blink and self.active:
            pygame.draw.line(
                surface, pygame.Color("black"), (w + 2, self.rendered_rect.top + 2),
                (w + 2, self.rendered_rect.bottom - 2))


class Checkbox:
    def __init__(self, name, pos, image_states, value=False, func=lambda val, *args: None, *args):
        self.images = {
            'normal': {
                True: load_image(image_states['normal_checked']),
                False: load_image(image_states['normal_unchecked'])
            },
            'hovered': {
                True: load_image(image_states['hovered_checked']),
                False: load_image(image_states['hovered_unchecked'])
            }
        }

        self.name = name
        self.args = args

        self.image = self.images['normal'][value]
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)

        self.func = func
        self.value = value

        self.states = {
            'hovered': False,
            'clicked': False
        }

    def update(self):
        self.rect = self.image.get_rect(center=self.pos)
        if self.states['hovered']:
            self.image = self.images['hovered'][self.value]
        else:
            self.image = self.images['normal'][self.value]

    def render(self, surface):
        surface.blit(self.image, self.image.get_rect(center=self.pos))

    def apply_event(self, event):
        self.states['hovered'] = self.rect.collidepoint(*pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.states['hovered']:
                    self.states['clicked'] = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.states['hovered'] and self.states['clicked']:
                    self.value = not self.value
                    self.states['clicked'] = False
                    self.func(self.value, *self.args)


class CheckboxWithText(Checkbox):
    def __init__(self, name, pos, image_states, text, font_path, text_color, text_size,
                 value=False, func=lambda val, *args: None, *args):
        super().__init__(name, pos, image_states, value, func, *args)
        self.font = pygame.font.Font(font_path, text_size)
        self.text_color = pygame.Color(text_color)
        self.text = text

        self.text_surf = self.font.render(self.text, 1, self.text_color)
        self.rect = pygame.Rect(0, 0,
            self.text_surf.get_width() + self.image.get_width(),
            self.text_surf.get_height(),
        )
        self.rect.center = self.pos

    def update(self):
        super().update()
        self.text_surf = self.font.render(self.text, 1, self.text_color)
        self.rect = pygame.Rect(0, 0,
            self.text_surf.get_width() + self.image.get_width(),
            self.text_surf.get_height(),
        )
        self.rect.center = self.pos

    def render(self, surface):
        surface.blit(self.text_surf, self.text_surf.get_rect(left=self.rect.left, centery=self.pos[1]))
        surface.blit(self.image, self.image.get_rect(right=self.rect.right, centery=self.pos[1]))


class Button:
    def __init__(self, pos, image_states, text, font_path, text_color, text_size, name,
                 func=lambda *args: None, *args):
        self.normal_image = load_image(image_states['normal'])
        self.hover_image = load_image(image_states['hovered'])
        self.click_image = load_image(image_states['clicked'])

        self.text = text
        self.font = pygame.font.Font(font_path, text_size)
        self.text_color = pygame.Color(text_color)

        self.pos = pos

        self.image = self.normal_image

        self.name = name
        self.func = func
        self.args = args

        self.states = {
            'hovered': False,
            'clicked': False,
            'after_click': False
        }

    def update(self):
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
        text = self.font.render(self.text, 4, self.text_color)
        surface.blit(text, text.get_rect(center=self.pos))

    def apply_event(self, event):
        self.states['hovered'] = self.image.get_rect(center=self.pos).collidepoint(*pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.states['hovered']:
                    self.states['clicked'] = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.states['hovered'] and self.states['after_click']:
                    self.states['after_click'] = False
                    self.func(*self.args)


class Image:
    def __init__(self, pos, image, name):
        self.image = image

        self.name = name
        self.size = self.image.get_size()
        self.rect = pygame.Rect(pos[0], pos[1], self.size[0], self.size[1])
        self.rect = self.image.get_rect(center=pos)
        self.const_rect = self.rect.copy()
        self.const_rect.x = -self.size[0]

    def render(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, x, y):
        self.rect[0] += x
        self.rect[1] += y

    def get_pos(self):
        return self.rect[0], self.rect[1]

    def set_const_pos(self):
        self.const_rect.y = randint(0, Config.get_height() - self.size[1])
        self.rect = self.const_rect.copy()


class GUI:
    elements = []
    _cursor = None

    @staticmethod
    def set_cursor(path):
        GUI._cursor = load_image(path)

    @staticmethod
    def add_element(element):
        if all(map(lambda elem: elem.name != element.name, GUI.elements)):
            GUI.elements.append(element)
            return element

    @staticmethod
    def get_element(name):
        for elem in GUI.elements:
            if elem.name == name:
                return elem

    @staticmethod
    def render():
        for element in GUI.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(pygame.display.get_surface())

        if GUI._cursor is not None:
            pygame.display.get_surface().blit(
                GUI._cursor, GUI._cursor.get_rect(topleft=pygame.mouse.get_pos())
            )

    @staticmethod
    def update():
        pygame.mouse.set_visible(GUI._cursor is None)

        for element in GUI.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()

    @staticmethod
    def apply_event(event):
        for element in GUI.elements:
            get_event = getattr(element, "apply_event", None)
            if callable(get_event):
                element.apply_event(event)

    @staticmethod
    def del_element(*names):
        for element in GUI.elements.copy():
            if element.name in names:
                GUI.elements.remove(element)

    @staticmethod
    def clear():
        GUI.elements = []
