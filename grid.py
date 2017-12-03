import pygame
import sys


class Grid:
    def __init__(self, surface):
        self.surface = surface

        self.center_x = 0
        self.center_y = 0

        self.cell_size = 50
        self.nlines = 30

        self.font_size = 18
        self.font = pygame.font.SysFont('couriernew', self.font_size, bold=True)

    def new_hor_line(self, y_pos, width=1):
        pygame.draw.line(self.surface, BLACK, (0, y_pos), (w, y_pos), width)

    def new_vert_line(self, x_pos, width=1):
        pygame.draw.line(self.surface, BLACK, (x_pos, 0), (x_pos, h), width)

    def new_vert_num(self, x_pos, num):
        text = self.font.render(str(num), 3, BLACK)
        height = text.get_rect().height
        rect = text.get_rect(centerx=x_pos, y=h - height)

        bg = pygame.Surface(rect.size)
        bg.fill(GRAY)

        self.surface.blit(bg, rect)
        self.surface.blit(text, rect)

    def new_hor_num(self, y_pos, num):
        text = self.font.render(str(num), 3, BLACK)
        rect = text.get_rect(x=5, centery=y_pos)

        bg = pygame.Surface(rect.size)
        bg.fill(GRAY)

        self.surface.blit(bg, rect)
        self.surface.blit(text, rect)

    def draw(self):
        x = self.center_x // self.cell_size
        y = self.center_y // self.cell_size
        for i in range(self.nlines):
            x_pos = int(self.center_x) - x * self.cell_size + self.cell_size * i
            width = 5 if x - i == 0 else 1
            self.new_hor_line(x_pos, width)

        for i in range(self.nlines):
            y_pos = int(self.center_y) - y * self.cell_size + self.cell_size * i
            width = 5 if y - i == 0 else 1
            self.new_vert_line(y_pos, width)

        for i in range(self.nlines):
            x_pos = int(self.center_x) - x * self.cell_size + self.cell_size * i
            y_pos = int(self.center_y) - y * self.cell_size + self.cell_size * i

            self.new_hor_num(x_pos, x - i)
            self.new_vert_num(y_pos, y - i)

    def resize(self, delta):
        if delta < 0:
            # scale up
            if self.cell_size + 10 < 150:
                self.font_size += 2
                self.font = pygame.font.SysFont('couriernew', self.font_size, bold=True)

                self.cell_size += 10
                if self.font_size < 18:
                    self.nlines -= 15
        else:
            # scale down
            if self.cell_size - 10 > 20:
                self.font_size -= 2
                self.font = pygame.font.SysFont('couriernew', self.font_size, bold=True)

                self.cell_size -= 10
                self.nlines += 15

    def move(self, delta_y, delta_x):
        self.center_x += delta_x
        self.center_y += delta_y


BLACK = (0, 0, 0)
GRAY = (136, 136, 136)

pygame.init()
w, h = size = 1280, 720
screen = pygame.display.set_mode(size)

grid = Grid(screen)

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (4, 5):
                grid.resize(event.button - 5)
        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            grid.move(*event.rel)

    screen.fill(GRAY)
    grid.draw()
    pygame.display.flip()
