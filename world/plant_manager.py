from .tile_manager import PLANT, TileManager
from .item_manager import ItemManager
from rendering import Renderer
import random

class Plant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = 0
        self.MATURE_AGE = 600
        self.harvestable = False
        self.harvest_min = 6
        self.harvest_max = 15

    def render(self, renderer: Renderer):
        renderer.draw_circ(self.x, self.y, self.age / self.MATURE_AGE, (136, 163, 116))

    def harvest(self, item_manager: ItemManager):
        self.harvestable = False
        self.age = 0
        for _ in range(random.randint(self.harvest_min, self.harvest_max)):
            item_manager.add_item(self.x, self.y, "Food", (230, 232, 216))

class PlantManager:
    def __init__(self, tile_manager: TileManager):
        self.tile_manager = tile_manager
        self.plants = {}

    def find_nearest_plant(self, x, y):
        nearest_plant = None
        nearest_distance = float('inf')

        for plant_pos, plant in self.plants.items():
            distance = ((plant_pos[0] - x) ** 2 + (plant_pos[1] - y) ** 2)**0.5

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_plant = plant
        
        return nearest_plant
    
    def find_nearest_mature_plant(self, x, y):
        nearest_mature_plant = None
        nearest_distance = float('inf')

        for plant_pos, plant in self.plants.items():
            if plant.age >= plant.MATURE_AGE:
                distance = ((plant_pos[0] - x) ** 2 + (plant_pos[1] - y) ** 2) ** 0.5

                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_mature_plant = plant

        return nearest_mature_plant

    def update(self):
        plant_tiles = self.tile_manager.get_tiles(PLANT)
        
        for _, x, y in plant_tiles:
            if (x, y) not in self.plants:
                self.plants[(x, y)] = Plant(x, y)
            else:
                plant = self.plants[(x, y)]
                if plant.age < plant.MATURE_AGE:
                    plant.age += 0.1
                else:
                    plant.harvestable = True

    def render(self, renderer):
        for p in self.plants.values():
            p.render(renderer)

                