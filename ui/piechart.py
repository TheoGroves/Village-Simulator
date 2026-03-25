import pygame
import math

class PieChart:
    def __init__(self,offset_y=0,offset_x=0):
        self.values = {}
        self.total = 0

        self.x = 75+offset_x
        self.y = 100+offset_y
        self.rad = 70

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

        font = pygame.font.SysFont(None, 18)

        for i, (key, value) in enumerate(self.values.items()):
            if self.total == 0:
                self.total = 1
            fraction = value / self.total
            end_angle = start_angle + fraction * 2 * math.pi

            points = [(self.x, self.y)]

            steps = 30
            for s in range(steps + 1):
                angle = start_angle + (end_angle - start_angle) * (s / steps)
                px = self.x + math.cos(angle) * self.rad
                py = self.y + math.sin(angle) * self.rad
                points.append((px, py))

            color = colors[i % len(colors)]
            pygame.draw.polygon(screen, color, points)

            mid_angle = (start_angle + end_angle) / 2
            text_radius = self.rad * 0.5

            tx = self.x + math.cos(mid_angle) * text_radius
            ty = self.y + math.sin(mid_angle) * text_radius

            label = f"{key}: {value:.2f}"
            text_surface = font.render(label, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(tx, ty))

            screen.blit(text_surface, text_rect)

            start_angle = end_angle

        pygame.draw.circle(screen, (255,255,255), (self.x, self.y), self.rad, 2)