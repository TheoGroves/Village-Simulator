from .perlin_noise import perlin_octaves
from .smoothstep import smoothstep_n
import pygame
import heapq
import random
import time

# Physical Tiles
WATER = 0
DIRT  = 1
GRASS = 2
ROCK  = 3
WALL  = 4

# Zoned Tiles
PLANT = 5
HAUL = 6
PLAN = 7

TILE_SIZE = 64

def load_tex(path):
    img = pygame.image.load(path).convert()
    return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

TILE_TEXTURES = {
    WATER: load_tex("assets/textures/water.jpg"),
    DIRT:  load_tex("assets/textures/dirt.jpg"),
    GRASS: load_tex("assets/textures/grass.jpg"),
    ROCK:  load_tex("assets/textures/rock.jpg"),
    WALL:  load_tex("assets/textures/wall.jpg")
}

CHUNK_SIZE = 16

class Tile:
    __slots__ = ('type', 'height', 'variation', 'yellow', 'tex')

    def __init__(self):
        self.type = WATER
        self.height = 0
        self.variation = 0
        self.yellow = 0
        self.tex = TILE_TEXTURES[self.type]

    def set_type(self, type_int):
        self.type = type_int
        self.tex = TILE_TEXTURES[self.type]

    def set_height(self, height):
        self.height = height

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
                surf = pygame.Surface((CHUNK_SIZE * TILE_SIZE, CHUNK_SIZE * TILE_SIZE))

                for ty in range(CHUNK_SIZE):
                    for tx in range(CHUNK_SIZE):
                        world_x = cx * CHUNK_SIZE + tx
                        world_y = cy * CHUNK_SIZE + ty

                        if world_x < self.width and world_y < self.height:
                            tile = self.tiles[world_y][world_x]
                            texture = tile.tex.copy()

                            shade = 0.4 * tile.height + 0.6
                            variation = 0.85 + (tile.variation + 1) * 0.15
                            brightness = shade * variation

                            brightness = max(0.3, min(brightness, 1.5))

                            overlay = pygame.Surface((TILE_SIZE, TILE_SIZE))
                            val = int(255 * brightness)
                            overlay.fill((val, val, val))

                            texture.blit(overlay, (0, 0), special_flags=pygame.BLEND_MULT)

                            surf.blit(texture, (tx * TILE_SIZE, ty * TILE_SIZE))

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
        # Early break if attempting to pathfind out of bounds
        if not 0 < start_x < self.width-1 or not 0 < start_y < self.height-1 or not 0 < end_x < self.width-1 or not 0 < end_y < self.height-1:
            return None
        # Early break if attempting to pathfind to an impassable
        if self.get_tile(start_x, start_y).type in (WATER, ROCK, WALL) or self.get_tile(end_x, end_y).type in (WATER, ROCK, WALL):
            return None

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

            texture = tile.tex
            chunk_surf.blit(texture, (tx * TILE_SIZE, ty * TILE_SIZE))

    def get_tiles(self, type):
        tiles = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile.type == type:
                    tiles.append((tile, x, y))
        return tiles
    
    def get_tile(self, x, y):
        return self.tiles[y][x]
    
    def find_nearest_tile(self, x, y, tile_type):
        nearest_tile = None
        nearest_pos = None
        nearest_distance = float("inf")

        tiles = self.get_tiles(tile_type)

        for tile, t_x, t_y in tiles:
            dx = x - t_x
            dy = y - t_y
            distance = dx * dx + dy * dy

            if distance == 0:
                return tile, (t_x, t_y)

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_tile = tile
                nearest_pos = (t_x, t_y)

        return nearest_tile, nearest_pos

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
                    screen_x = int(cx * CHUNK_SIZE * TILE_SIZE - cam_x)
                    screen_y = int(cy * CHUNK_SIZE * TILE_SIZE - cam_y)

                    renderer.screen.blit(chunk_surf, (screen_x, screen_y))
