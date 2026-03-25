import pygame
import random
from .tile_manager import ROCK, WATER, HAUL

class Item:
    def __init__(self, x, y, type, col, weight):
        self.type = type 
        self.x = x
        self.y = y
        self.col = col
        self.condition = 100
        self.weight = weight

    def render(self, renderer):
        renderer.draw_circ(self.x, self.y, 0.7, self.col)

class ItemManager:
    def __init__(self):
        self.items = {}

    def add_item(self, x=None, y=None, type=None, col=None, weight=None, item=None):
        if item is None:
            item = Item(x, y, type, col, weight)

        pos = (item.x, item.y)

        if pos not in self.items:
            self.items[pos] = []

        self.items[pos].append(item)

    def remove(self, item):
        pos = (item.x, item.y)

        if pos in self.items:
            if item in self.items[pos]:
                self.items[pos].remove(item)

                if not self.items[pos]:
                    del self.items[pos]

    def find_nearest_by_type(self, x, y, item_type, tm=None, exclude_types=None):
        if exclude_types is None:
            exclude_types = []

        nearest_item = None
        nearest_distance = float("inf")

        for (ix, iy), items in self.items.items():
            if tm:
                if tm.get_tile(ix, iy).type in exclude_types:
                    continue

            dx = x - ix
            dy = y - iy
            distance = dx*dx + dy*dy

            for item in items:
                if item_type != "Any" and item.type != item_type:
                    continue

                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_item = item

        return nearest_item
    
    def scatter_items(self, type, col, weight, num, tm):
        x = random.randint(5, tm.width-6)
        y = random.randint(5, tm.height-6)
        while tm.get_tile(x, y).type in [ROCK, WATER]:
            x = random.randint(5, tm.width-6)
            y = random.randint(5, tm.height-6)
        for _ in range(num):
            item = Item(x + random.randint(-5, 5), y + random.randint(-5, 5), type, col, weight)
            while tm.get_tile(item.x, item.y).type in [ROCK, WATER]:
                item = Item(x + random.randint(-5, 5), y + random.randint(-5, 5), type, col, weight)

            self.add_item(item=item)

    def update(self, tile_manager):
        remove_items = []
        for pos in self.items:
            items = self.items[pos] # All items on that tile

            tile_type = tile_manager.get_tile(items[0].x, items[0].y).type
            for item in items: # Loop through all items on the tile
                if not tile_type == HAUL: # Decrease condition every tick if the tile isn't on a haul zone
                    item.condition -= 0.01
                if item.condition <= 0: # If the condition is zero or less, remove the item
                    remove_items.append(item)
        for item in remove_items:
            self.remove(item)
        
    def render(self, renderer):
        font = pygame.font.SysFont(None, 14)

        for (x, y), items in self.items.items():
            if not items:
                continue

            items[0].render(renderer)

            if len(items) > 1:
                text = font.render(str(len(items)), True, (255, 255, 255))

                screen_x = int(x * renderer.grid_size - renderer.x)
                screen_y = int(y * renderer.grid_size - renderer.y)

                renderer.screen.blit(text,(screen_x, screen_y + renderer.grid_size // 2))