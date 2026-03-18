from renderer import Renderer
from tile_manager import ROCK, WATER
import random
import pygame

TONES = [
    (255, 244, 219),
    (230, 215, 184),
    (209, 189, 146),
    (99, 84, 51),
    (54, 45, 25)
]

class Pawn:
    def __init__(self, x, y, tile_manager):
        # engine
        self.x = x
        self.y = y
        self.tone = random.choice(TONES)
        self.name = "Test Name"
        self.drafted = False

        self.tile_manager = tile_manager
        self.last_target = (0,0)
        self.path = []

        # stats (0-100)
        self.food = 100
        self.sleep = 100
        self.recreation = 100

    def update(self, renderer):
        if self.drafted: # Manual pathfinding when drafted
            self.drafted_pathfind(renderer)
        else: # Automatic AI pathfinding when undrafted
            print("AI in control")

        if self.path:
            self.follow_path(self.path)
        self.food -= 0.125
        self.sleep -= 0.125
        self.recreation -= 0.125

        self.food = max(0, min(100, self.food))
        self.sleep = max(0, min(100, self.sleep))
        self.recreation = max(0, min(100, self.recreation))

    def pathfind(self, x, y):
        return self.tile_manager.find_path(self.x, self.y, x, y)
    
    def drafted_pathfind(self, renderer):
        path = []
        mouse_x = int((pygame.mouse.get_pos()[0]+renderer.x)/renderer.grid_size)
        mouse_y = int((pygame.mouse.get_pos()[1]+renderer.y)/renderer.grid_size)
        if (mouse_x, mouse_y) != self.last_target and self.drafted:
            if pygame.mouse.get_pressed()[0]:
                path = self.tile_manager.find_path(self.x, self.y, mouse_x, mouse_y)
                self.last_target = (mouse_x, mouse_y)
        if path:
            self.path = path

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
        renderer.draw_circ(self.x, self.y, 1.3, (0,0,0))
        renderer.draw_circ(self.x, self.y, 1, self.tone)

        if self.path:
            for x,y in self.path:
                renderer.draw_circ(x, y, 0.5, (255, 255, 255))