import pygame
from renderer import Renderer
from pawn import Pawn
from tile_manager import TileManager
from detail_manager import DetailManager
from piechart import PieChart
from pawn_selector import PawnSelector
from building_system import BuildingSystem
from plant_manager import PlantManager
from item_manager import ItemManager
import time

pygame.init()

screen = pygame.display.set_mode((1280,720))

world_width = 128
world_height = 128

estimate = TileManager.generation_time_estimate(world_width, world_height)
font = pygame.font.SysFont(None, 50)
text_surface = font.render(f"Generating World. Estimated Generation time: {estimate:.2f}s", True, (255, 255, 255))
text_rect = text_surface.get_rect(center=(pygame.display.get_window_size()[0]/2, pygame.display.get_window_size()[1]/2))
screen.blit(text_surface, text_rect)
pygame.display.flip()

clock = pygame.time.Clock()

renderer = Renderer(screen, 5)

gen_start = time.time()
tile_manager = TileManager(world_width,world_height,8,50)
detail_manager = DetailManager(tile_manager, 5000)
print(f"Generated world of size {tile_manager.width}x{tile_manager.height} with {len(tile_manager.chunks)} chunks in {time.time()-gen_start:.2f}s")

ps = PawnSelector()

building_system = BuildingSystem(tile_manager, renderer)

plant_manager = PlantManager(tile_manager)

item_manager = ItemManager()

v = Pawn(0, 0, tile_manager)
v.set_random_pos(tile_manager)

ps.select_pawn(v)

pc = PieChart()
render_pc = False
f1_held = False

dt=0
frame = 0

time_scale = 1

while True:
    start = time.time()
    renderer.draw_calls = 0
    pc.values = {}

    # Events
    event_start = time.time()
    for event in pygame.event.get():
        ps.handle_event(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    event_time = time.time() - event_start

    # Pathfinding
    inp_start = time.time()

    # World regen
    if pygame.key.get_pressed()[pygame.K_r]:
        tile_manager = TileManager(128, 128, 8, 50)
        detail_manager = DetailManager(tile_manager, 5000)
        v.set_random_pos(tile_manager)

    # Debug Pie Chart
    if pygame.key.get_pressed()[pygame.K_F1]:
        if not f1_held:
            render_pc = not render_pc
            f1_held = True
    else:
        f1_held = False

    # Time Scaling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        time_scale = 1
    elif keys[pygame.K_2]:
        time_scale = 2
    elif keys[pygame.K_3]:
        time_scale = 6
    elif keys[pygame.K_4]:
        time_scale = 12

    # Building
    building_system.build()

    inp_time = time.time()-inp_start

    # Object Updating
    update_start = time.time()
    renderer.move(dt)
    if frame % (30//time_scale) == 0: # Tick
        v.update(renderer, plant_manager, item_manager)
        plant_manager.update()

    update_time = time.time() - update_start

    # World Rendering
    rend_start = time.time()
    screen.fill((37, 43, 48))
    tile_manager.render(renderer)
    detail_manager.render(renderer)
    plant_manager.render(renderer)
    item_manager.render(renderer)
    v.render(renderer)
    
    renderer.render()

    # UI Rendering
    ps.render(screen)
    rend_time = time.time()-rend_start

    # Misc
    pygame.display.set_caption(
        f"E: {event_time*1000:.2f} "
        f"I: {inp_time*1000:.2f} "
        f"U: {update_time*1000:.2f} "
        f"R: {rend_time*1000:.2f} "
        f"T: {(event_time + inp_time + update_time + rend_time)*1000:.2f} ms "
        f"DC: {renderer.draw_calls}"
    )
    pc.add_value("E", event_time*1000)
    pc.add_value("I", inp_time*1000)
    pc.add_value("U", update_time*1000)
    pc.add_value("R", rend_time*1000)
    if render_pc:
        pc.render(screen)

    pygame.display.flip()
    clock.tick(60)
    frame += 1
    dt=time.time()-start