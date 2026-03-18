from renderer import Renderer
from tile_manager import ROCK, WATER
import random

TONES = [
    (255, 244, 219),
    (230, 215, 184),
    (209, 189, 146),
    (99, 84, 51),
    (54, 45, 25)
]

class Pawn:
    def __init__(self, x=0, y=0):
        # engine
        self.x = x
        self.y = y
        self.tone = random.choice(TONES)
        self.name = "Test Name"
        self.drafted = False

        # stats (0-100)
        self.food = 100
        self.sleep = 100
        self.recreation = 100

    def follow_path(self, path):
        if not path == []:
            self.x = path[0][0]
            self.y = path[0][1]
            path.pop(0)

    def set_random_pos(self, tile_manager):
        """Sets a random pos, avoiding impassable terrain - use for spawning villagers"""
        test_x = random.randint(0, tile_manager.width-1)
        test_y = random.randint(0, tile_manager.height-1)
        type = tile_manager.tiles[test_y][test_x].type
        while type == ROCK or type == WATER:
            test_x = random.randint(0, tile_manager.width-1)
            test_y = random.randint(0, tile_manager.height-1)
            type = tile_manager.tiles[test_y][test_x].type
        self.x = test_x
        self.y = test_y


    def render(self, renderer: Renderer):
        renderer.draw_circ(self.x, self.y, 1, self.tone)