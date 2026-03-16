import pygame
import math

class PieChart:
    def __init__(self):
        self.values = {}
        self.total = 0

        self.x = 100
        self.y = 100
        self.rad = 50

    def add_value(self, key, value):
        self.values[key] = value
        self.total = sum(self.values.values())

    def clear(self):
        self.values = {}

    def render(self, screen):
        start_angle = 0

        colors = [
            (255,100,100),
            (100,255,100),
            (100,100,255),
            (255,255,100),
            (255,100,255),
            (100,255,255)
        ]

        for i, (key, value) in enumerate(self.values.items()):
            fraction = value / self.total
            end_angle = start_angle + fraction * 2 * math.pi

            points = [(self.x, self.y)]

            steps = 30
            for s in range(steps + 1):
                angle = start_angle + (end_angle - start_angle) * (s / steps)
                px = self.x + math.cos(angle) * self.rad
                py = self.y + math.sin(angle) * self.rad
                points.append((px, py))

            pygame.draw.polygon(screen, colors[i % len(colors)], points)

            start_angle = end_angle

        pygame.draw.circle(screen, (255,255,255), (self.x, self.y), self.rad, 2)