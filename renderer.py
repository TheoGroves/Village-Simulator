import pygame

class Renderer:
    def __init__(self, screen, grid_size=50):
        self.x=0
        self.y=0
        self.screen = screen
        self.grid_size = grid_size

    def draw_rect(self, x, y, width, height, col):
        pygame.draw.rect(self.screen, col, pygame.Rect(round(x) * self.grid_size - (self.grid_size/2) - self.x, round(y) * self.grid_size - (self.grid_size/2) - self.y, width * self.grid_size, height * self.grid_size))

    def draw_circ(self, x, y, rad, col):
        pygame.draw.circle(self.screen, col, (round(x)*self.grid_size-self.x,round(y)*self.grid_size-self.y), rad*self.grid_size//2)

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
                self.grid_size += event.y
        
        self.grid_size = max(1, min(self.grid_size, 500))