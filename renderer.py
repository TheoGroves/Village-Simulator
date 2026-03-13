import pygame

class Renderer:
    def __init__(self, screen, grid_size=50):
        self.screen = screen
        self.grid_size = grid_size

    def draw_rect(self, x, y, width, height, col):
        pygame.draw.rect(self.screen, col, pygame.Rect(round(x) * self.grid_size - (self.grid_size/2), round(y) * self.grid_size - (self.grid_size/2), width * self.grid_size, height * self.grid_size))

    def draw_circ(self, x, y, rad, col):
        pygame.draw.circle(self.screen, col, (round(x)*self.grid_size,round(y)*self.grid_size), rad*self.grid_size//2)