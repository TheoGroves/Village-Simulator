from tile_manager import TileManager, DIRT, GRASS
from renderer import Renderer
from perlin_noise import perlin_octaves
from smoothstep import smoothstep_n
import random

class DetailManager:
    def __init__(self, tile_manager: TileManager, num_trees=500, num_rocks = 300):
        self.trees = []
        self.rocks = []

        self.num_trees = num_trees
        self.num_rocks = num_rocks

        self.width = tile_manager.width
        self.height = tile_manager.height

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

    def render(self, renderer: Renderer):
        for tree in self.trees:
            renderer.draw_circ(tree[0], tree[1], tree[2], (58, 94, 60))

        for rock in self.rocks:
            renderer.draw_circ(rock[0], rock[1], rock[2], (179, 179, 179))