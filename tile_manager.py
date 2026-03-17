from perlin_noise import perlin_octaves
from smoothstep import smoothstep_n
import pygame
import heapq

WATER = 0
DIRT  = 1
GRASS = 2
ROCK  = 3

TILE_COLOURS = {
    WATER: (186, 238, 247),
    DIRT:  (74, 63, 55),
    GRASS: (194, 237, 119),
    ROCK:  (59, 59, 59)
}

CHUNK_SIZE = 16

class Tile:
    __slots__ = ('type', 'height', 'colour', 'height_colour')

    def __init__(self):
        self.type = WATER
        self.height = 0
        self.colour = TILE_COLOURS[self.type]
        self.height_colour = self.colour

    def set_type(self, type_int):
        self.type = type_int
        self.colour = TILE_COLOURS[self.type]

    def set_height(self, height):
        self.height = height
        shade = 0.3 * self.height + 0.7
        r, g, b = self.colour
        self.height_colour = (int(r*shade), int(g*shade), int(b*shade))

class TileManager:
    def __init__(self, width, height, octaves=8):
        self.width = width
        self.height = height
        self.chunk_size = CHUNK_SIZE

        self.tiles = [[Tile() for _ in range(width)] for _ in range(height)]

        for y in range(height):
            for x in range(width):
                h = perlin_octaves(x * 0.05, y * 0.05, 0, octaves)
                h_smooth = smoothstep_n(h, 10)
                tile_type = self.determine_type(h_smooth)
                self.tiles[y][x].set_type(tile_type)
                self.tiles[y][x].set_height(h_smooth)

        self.chunks = {}
        chunk_cols = (width + CHUNK_SIZE - 1) // CHUNK_SIZE
        chunk_rows = (height + CHUNK_SIZE - 1) // CHUNK_SIZE

        for cy in range(chunk_rows):
            for cx in range(chunk_cols):
                surf = pygame.Surface((CHUNK_SIZE, CHUNK_SIZE))
                for ty in range(CHUNK_SIZE):
                    for tx in range(CHUNK_SIZE):
                        world_x = cx * CHUNK_SIZE + tx
                        world_y = cy * CHUNK_SIZE + ty
                        if world_x < width and world_y < height:
                            color = self.tiles[world_y][world_x].height_colour
                            surf.set_at((tx, ty), color)
                self.chunks[(cx, cy)] = surf

        print(f"Generated world {width}x{height} with {len(self.chunks)} pre-rendered chunks")


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
                if tile.type in (WATER, ROCK):
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
                    screen_x = cx * CHUNK_SIZE * gs - cam_x - gs/2
                    screen_y = cy * CHUNK_SIZE * gs - cam_y - gs/2
                    scaled_surf = pygame.transform.scale(chunk_surf, (CHUNK_SIZE * gs, CHUNK_SIZE * gs))
                    renderer.screen.blit(scaled_surf, (screen_x, screen_y))