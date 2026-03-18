import pygame

class Renderer:
    def __init__(self, screen, grid_size=50):
        self.x = -324
        self.y = -46
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

        speed = 1
        if keys[pygame.K_LSHIFT]:
            speed = 2

        if keys[pygame.K_w]:
            self.y -= 200 * dt * speed
        if keys[pygame.K_s]:
            self.y += 200 * dt * speed
        if keys[pygame.K_a]:
            self.x -= 200 * dt * speed
        if keys[pygame.K_d]:
            self.x += 200 * dt * speed

        if keys[pygame.K_EQUALS]:
            self.target_grid_size += 1
        if keys[pygame.K_MINUS]:
            self.target_grid_size -= 1

        self.target_grid_size = max(2, min(self.target_grid_size, 500))
        self.target_grid_size = round(self.target_grid_size)

        old_gs = self.grid_size

        self.grid_size += (self.target_grid_size - self.grid_size) * 0.2
        self.grid_size = round(self.grid_size)

        if self.grid_size != old_gs:
            scale = self.grid_size / old_gs

            screen_w, screen_h = self.screen.get_size()
            cx = screen_w / 2
            cy = screen_h / 2

            self.x = (self.x + cx) * scale - cx
            self.y = (self.y + cy) * scale - cy

    def render(self):
        for x, y, w, h, col in self.rects:
            pygame.draw.rect(self.screen, col, (x, y, w, h))

        for circ in self.circs:
            pygame.draw.circle(self.screen, circ[2], circ[0], circ[1])

        self.rects = []
        self.circs = []