from perlin_noise import perlin_octaves
from smoothstep import smoothstep_n
import pygame
import heapq
import random
import time

WATER = 0
DIRT  = 1
GRASS = 2
ROCK  = 3
WALL  = 4
PLANT = 5

TILE_COLOURS = {
    WATER: (109, 164, 201),
    DIRT:  (128, 110, 91),
    GRASS: (178, 212, 148),
    ROCK:  (102, 102, 102),
    WALL:  (105, 95, 84),
    PLANT: (237, 255, 191)
}

CHUNK_SIZE = 16

class Tile:
    __slots__ = ('type', 'height', 'colour', 'height_colour', 'variation', 'yellow')

    def __init__(self):
        self.type = WATER
        self.height = 0
        self.variation = 0
        self.yellow = 0
        self.colour = TILE_COLOURS[self.type]
        self.height_colour = self.colour

    def set_type(self, type_int):
        self.type = type_int
        self.colour = TILE_COLOURS[self.type]

    def set_height(self, height):
        self.height = height

        shade = 0.4 * self.height + 0.6
        variation_factor = 0.85 + (self.variation + 1) * 0.15

        r, g, b = self.colour

        # Yellow patches in grass
        if self.type == GRASS:
            yellow_shift = int(self.yellow * 20)

            r += yellow_shift
            g += yellow_shift // 2
            b -= yellow_shift

        # Darker mountains
        if self.type == ROCK:
            shade = 0.5 * ((height-0.8)/0.2) + 0.5

        # Darker Water
        if self.type == WATER:
            shade = 0.3 * ((height-0.2)/0.2) + 0.7
            
        r = int(r * shade * variation_factor)
        g = int(g * shade * variation_factor)
        b = int(b * shade * variation_factor)

        self.height_colour = (
            max(0, min(r, 255)),
            max(0, min(g, 255)),
            max(0, min(b, 255))
        )

class TileManager:
    def __init__(self, width, height, octaves=8, scale=20):
        self.width = width
        self.height = height
        self.chunk_size = CHUNK_SIZE
        self.ind = 0

        self.tiles = []
        self.generate_world(octaves, scale)
        self.rebuild_chunks()

    @staticmethod
    def generation_time_estimate(width, height):
        """Estimates time to generate a world of width and height"""
        times = []
        for _ in range(5):
            start = time.time()
            h=perlin_octaves(1 * 0.05, 1 * 0.05, 0, 8)
            smoothstep_n(h, 10)
            perlin_octaves(1 * 0.1, 1 * 0.1, 0, 4)
            smoothstep_n(perlin_octaves(1 * 0.02, 1 * 0.02, 200, 2), 20)
            times.append(time.time()-start)
        
        return (sum(times)/len(times)) * (width*height)

    def generate_world(self, octaves=8, scale=20):
        self.tiles = [[Tile() for _ in range(self.width)] for _ in range(self.height)]
        seed = random.randint(0, 10000)
        for y in range(self.height):
            for x in range(self.width):
                h = perlin_octaves(x * (1/scale), y * (1/scale), seed, octaves)
                h_smooth = smoothstep_n(h, 10)
                c = perlin_octaves(x * (1/(scale*0.5)), y * (1/(scale*0.5)), seed, 4)
                y_noise = smoothstep_n(perlin_octaves(x * 0.02, y * 0.02, 200, 2), 20)
                tile_type = self.determine_type(h_smooth)
                self.tiles[y][x].set_type(tile_type)
                self.tiles[y][x].variation = c
                self.tiles[y][x].yellow = y_noise
                self.tiles[y][x].set_height(h_smooth)

    def rebuild_chunks(self):
        self.chunks = {}

        chunk_cols = (self.width + CHUNK_SIZE - 1) // CHUNK_SIZE
        chunk_rows = (self.height + CHUNK_SIZE - 1) // CHUNK_SIZE

        for cy in range(chunk_rows):
            for cx in range(chunk_cols):
                surf = pygame.Surface((CHUNK_SIZE, CHUNK_SIZE))

                for ty in range(CHUNK_SIZE):
                    for tx in range(CHUNK_SIZE):
                        world_x = cx * CHUNK_SIZE + tx
                        world_y = cy * CHUNK_SIZE + ty

                        if world_x < self.width and world_y < self.height:
                            color = self.tiles[world_y][world_x].height_colour
                            surf.set_at((tx, ty), color)

                self.chunks[(cx, cy)] = surf


    @staticmethod
    def determine_type(height):
        if height > 0.8:
            return ROCK
        elif height > 0.4:
            return GRASS
        elif height > 0.2:
            return DIRT
        else:
            return WATER
        
    def find_path(self, start_x, start_y, end_x, end_y):
        end = (end_x, end_y)

        def heuristic(x, y):
            return abs(x - end_x) + abs(y - end_y)

        directions = [(-1,0),(1,0),(0,-1),(0,1)]

        open_heap = [(0, start_x, start_y)]
        open_set = {(start_x, start_y)}
        came_from = {}
        g_score = {(start_x, start_y): 0}

        while open_heap:
            _, cx, cy = heapq.heappop(open_heap)
            open_set.discard((cx, cy))

            if (cx, cy) == end:
                path = [(cx, cy)]
                while (cx, cy) in came_from:
                    cx, cy = came_from[(cx, cy)]
                    path.append((cx, cy))
                return path[::-1]

            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue

                tile = self.tiles[ny][nx]
                if tile.type in (WATER, ROCK, WALL):
                    continue

                cost = 1 + tile.height * 5
                tentative_g = g_score[(cx, cy)] + cost

                if (nx, ny) not in g_score or tentative_g < g_score[(nx, ny)]:
                    came_from[(nx, ny)] = (cx, cy)
                    g_score[(nx, ny)] = tentative_g
                    f_score = tentative_g + heuristic(nx, ny)
                    if (nx, ny) not in open_set:
                        heapq.heappush(open_heap, (f_score, nx, ny))
                        open_set.add((nx, ny))

        return None
    
    def add_tile(self, type, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return

        tile = self.tiles[y][x]

        tile.set_type(type)

        tile.set_height(tile.height)

        cx = x // CHUNK_SIZE
        cy = y // CHUNK_SIZE

        chunk_surf = self.chunks.get((cx, cy))
        if chunk_surf:
            tx = x % CHUNK_SIZE
            ty = y % CHUNK_SIZE

            chunk_surf.set_at((tx, ty), tile.height_colour)

    def get_tiles(self, type):
        tiles = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile.type == type:
                    tiles.append((tile, x, y))
        return tiles

    def render(self, renderer):
        screen_w, screen_h = pygame.display.get_window_size()
        gs = renderer.grid_size
        cam_x, cam_y = renderer.x, renderer.y

        start_tile_x = max(0, int(cam_x // gs))
        start_tile_y = max(0, int(cam_y // gs))
        end_tile_x   = min(self.width, int((cam_x + screen_w) // gs) + 1)
        end_tile_y   = min(self.height, int((cam_y + screen_h) // gs) + 1)

        start_chunk_x = start_tile_x // CHUNK_SIZE
        start_chunk_y = start_tile_y // CHUNK_SIZE
        end_chunk_x = end_tile_x // CHUNK_SIZE
        end_chunk_y = end_tile_y // CHUNK_SIZE

        for cy in range(start_chunk_y, end_chunk_y + 1):
            for cx in range(start_chunk_x, end_chunk_x + 1):
                chunk_surf = self.chunks.get((cx, cy))
                if chunk_surf:
                    screen_x = int(cx * CHUNK_SIZE * gs - cam_x - gs/2)
                    screen_y = int(cy * CHUNK_SIZE * gs - cam_y - gs/2)
                    scaled_surf = pygame.transform.scale(chunk_surf, (CHUNK_SIZE * gs, CHUNK_SIZE * gs))
                    renderer.screen.blit(scaled_surf, (screen_x, screen_y))