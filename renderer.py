import pygame

class Renderer:
    def __init__(self, screen, grid_size=50):
        self.x = 0
        self.y = 0
        self.screen = screen

        self.grid_size = grid_size
        self.target_grid_size = grid_size

        self.draw_calls = 0

        self._rect = pygame.Rect(0, 0, 0, 0)

        self.rects = []
        self.circs = []

    def draw_rect(self, x, y, width, height, col):
        gs = self.grid_size

        self.rects.append((
            round(x) * gs - (gs/2) - self.x,
            round(y) * gs - (gs/2) - self.y,
            width * gs,
            height * gs,
            col
        ))
        self.draw_calls += 1

    def draw_circ(self, x, y, rad, col):
        self.circs.append(((round(x) * self.grid_size-self.x, round(y) * self.grid_size-self.y), rad * self.grid_size//2, col))
        self.draw_calls += 1

    def move(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.y -= 50 * dt
        if keys[pygame.K_DOWN]:
            self.y += 50 * dt
        if keys[pygame.K_LEFT]:
            self.x -= 50 * dt
        if keys[pygame.K_RIGHT]:
            self.x += 50 * dt

        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                self.target_grid_size += event.y * 5

        self.target_grid_size = max(5, min(self.target_grid_size, 500))
        self.target_grid_size = round(self.target_grid_size)

        self.grid_size += (self.target_grid_size - self.grid_size) * 0.2

    def render(self):
        for x, y, w, h, col in self.rects:
            pygame.draw.rect(self.screen, col, (x, y, w, h))

        for circ in self.circs:
            pygame.draw.circle(self.screen, circ[2], circ[0], circ[1])

        self.rects = []
        self.circs = []