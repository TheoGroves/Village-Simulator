from tile_manager import TileManager, DIRT, GRASS
from renderer import Renderer
from perlin_noise import perlin_octaves
from smoothstep import smoothstep_n
import random
import pygame

CHUNK_SIZE = 16

class DetailManager:
    def __init__(self, tile_manager: TileManager, num_trees=500, num_rocks = 300):
        self.trees = []
        self.rocks = []
        self.chunks = {}

        self.num_trees = num_trees
        self.num_rocks = num_rocks

        self.width = tile_manager.width
        self.height = tile_manager.height

        self.generate_details(tile_manager)

    def generate_details(self, tile_manager):
        for _ in range(self.num_trees):
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)

            h = perlin_octaves(x * 0.05, y * 0.05, 1, 4)
            h_smooth = smoothstep_n(h, 10)

            if tile_manager.tiles[y][x].type == DIRT or tile_manager.tiles[y][x].type == GRASS and h_smooth >= 0.7:
                self.trees.append((x,y,h_smooth))

        for _ in range(self.num_rocks):
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)

            h = perlin_octaves(x * 0.08, y * 0.08, 3, 4)
            h_smooth = smoothstep_n(h, 10)

            if tile_manager.tiles[y][x].type == DIRT or tile_manager.tiles[y][x].type == GRASS and h_smooth >= 0.7:
                self.rocks.append((x,y,h_smooth))

        chunk_cols = (self.width + CHUNK_SIZE - 1) // CHUNK_SIZE
        chunk_rows = (self.height + CHUNK_SIZE - 1) // CHUNK_SIZE

        for cy in range(chunk_rows):
            for cx in range(chunk_cols):
                surf = pygame.Surface((CHUNK_SIZE, CHUNK_SIZE), pygame.SRCALPHA)

                # trees
                for x, y, size in self.trees:
                    if cx * CHUNK_SIZE <= x < (cx+1) * CHUNK_SIZE and cy * CHUNK_SIZE <= y < (cy+1) * CHUNK_SIZE:
                        tx = x - cx * CHUNK_SIZE
                        ty = y - cy * CHUNK_SIZE

                        pygame.draw.circle(
                            surf,
                            (58, 94, 60),
                            (tx, ty),
                            max(1, int(size * 2))
                        )

                # rocks
                for x, y, size in self.rocks:
                    if cx * CHUNK_SIZE <= x < (cx+1) * CHUNK_SIZE and cy * CHUNK_SIZE <= y < (cy+1) * CHUNK_SIZE:
                        tx = x - cx * CHUNK_SIZE
                        ty = y - cy * CHUNK_SIZE

                        pygame.draw.circle(
                            surf,
                            (179, 179, 179),
                            (tx, ty),
                            max(1, int(size * 2))
                        )

                self.chunks[(cx, cy)] = surf

    def render(self, renderer: Renderer):
        gs = renderer.grid_size
        cam_x, cam_y = renderer.x, renderer.y

        # trees
        for x, y, size in self.trees:
            screen_x = int(x * gs - cam_x)
            screen_y = int(y * gs - cam_y)

            pygame.draw.circle(
                renderer.screen,
                (58, 94, 60),
                (screen_x, screen_y),
                max(1, int(size * gs * 0.5))
            )

        # rocks
        for x, y, size in self.rocks:
            screen_x = int(x * gs - cam_x)
            screen_y = int(y * gs - cam_y)

            pygame.draw.circle(
                renderer.screen,
                (179, 179, 179),
                (screen_x, screen_y),
                max(1, int(size * gs * 0.5))
            )