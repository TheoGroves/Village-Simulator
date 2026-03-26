from .tile_manager import PLAN, PLANT, HAUL
import pygame

class BuildingSystem:
    def __init__(self, tile_manager, renderer):
        self.tile_manager = tile_manager
        self.renderer = renderer

        self.building_enabled = False
        self.plant_zoning_enabled = False
        self.haul_zoning_enabled = False

        self.zero_held = False # Zero to build
        self.nine_held = False # Nine to zone plants
        self.eight_held = False # Eight to zone hauling

    def build(self, notification_system):
        mouse_x = int((pygame.mouse.get_pos()[0] + self.renderer.x) / self.renderer.grid_size)
        mouse_y = int((pygame.mouse.get_pos()[1] + self.renderer.y) / self.renderer.grid_size)

        if pygame.key.get_pressed()[pygame.K_0]:
            if not self.zero_held:
                self.building_enabled = not self.building_enabled
                self.zero_held = True

                mode = "Building enabled" if self.building_enabled else "Building disabled"
                notification_system.add_notification(mode, 3)

            else:
                pass
        else:
            self.zero_held = False

        if pygame.key.get_pressed()[pygame.K_9]:
            if not self.nine_held:
                self.plant_zoning_enabled = not self.plant_zoning_enabled
                self.nine_held = True

                mode = "Plant zoning enabled" if self.plant_zoning_enabled else "Plant zoning disabled"
                notification_system.add_notification(mode, 3)

            else:
                pass
        else:
            self.nine_held = False

        if pygame.key.get_pressed()[pygame.K_8]:
            if not self.eight_held:
                self.haul_zoning_enabled = not self.haul_zoning_enabled
                self.eight_held = True

                mode = "Haul zoning enabled" if self.haul_zoning_enabled else "Haul zoning disabled"
                notification_system.add_notification(mode, 3)

            else:
                pass
        else:
            self.eight_held = False

        tile = PLAN

        if self.plant_zoning_enabled:
            tile = PLANT
        elif self.haul_zoning_enabled:
            tile = HAUL

        if pygame.mouse.get_pressed()[0] and self.building_enabled:
            self.tile_manager.add_tile(tile, mouse_x, mouse_y)