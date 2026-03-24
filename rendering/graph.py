import pygame

COLOURS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0)
]

class LineGraph:
    def __init__(self):
        self.x = 155
        self.y = 150

        self.num_lines = len(COLOURS)

        self.values = [[0] * 150 for _ in range(self.num_lines)]
        self.names = [f"Line {i}" for i in range(self.num_lines)]

        self.maximum = 1

        pygame.font.init()
        self.font = pygame.font.SysFont(None, 18)

    def add_value(self, value, line, name=None):
        if name is not None:
            self.names[line] = name

        self.values[line].append(value)
        self.values[line].pop(0)

        self.maximum = max(max(line_vals) for line_vals in self.values)

    def render(self, screen):
        # axis
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), (self.x, self.y - 100))
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), (self.x + 150, self.y))

        max_val = self.maximum if self.maximum != 0 else 1

        # draw lines
        for line_index, line_vals in enumerate(self.values):
            points = []

            for i, value in enumerate(line_vals):
                x = self.x + i
                y = self.y - (value / max_val) * 100
                points.append((x, y))

            pygame.draw.lines(
                screen,
                COLOURS[line_index % len(COLOURS)],
                False,
                points,
                2
            )

        legend_y = self.y + 10
        legend_x = self.x

        for i, name in enumerate(self.names):
            colour = COLOURS[i % len(COLOURS)]

            pygame.draw.rect(screen, colour, (legend_x, legend_y, 10, 10))

            text_surface = self.font.render(name, True, (255, 255, 255))
            screen.blit(text_surface, (legend_x + 15, legend_y - 2))

            legend_y += 20