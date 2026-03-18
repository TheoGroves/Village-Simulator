from tile_manager import WALL
import pygame

class BuildingSystem:
    def __init__(self, tile_manager, renderer):
        self.tile_manager = tile_manager
        self.renderer = renderer

        self.building_enabled = False
        self.zero_held = False

    def build(self):
        mouse_x = int((pygame.mouse.get_pos()[0]+self.renderer.x)/self.renderer.grid_size)
        mouse_y = int((pygame.mouse.get_pos()[1]+self.renderer.y)/self.renderer.grid_size)

        if pygame.key.get_pressed()[pygame.K_0]:
            if not self.zero_held:
                self.building_enabled = not self.building_enabled
                self.zero_held = True
        else:
            self.zero_held = False

        if pygame.mouse.get_pressed()[0] and self.building_enabled:
            self.tile_manager.add_tile(WALL, mouse_x, mouse_y)