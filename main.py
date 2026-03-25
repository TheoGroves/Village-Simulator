import pygame
import time
from rendering import Renderer
from pawn import Pawn
from world import TileManager, DetailManager, BuildingSystem, PlantManager, ItemManager, DayNightCycle
from ui import PawnSelector, HealthPanel, PieChart, LineGraph
from helpers import closest_to_mouse

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
hp = HealthPanel()

building_system = BuildingSystem(tile_manager, renderer)

plant_manager = PlantManager(tile_manager)

item_manager = ItemManager()
item_manager.scatter_items("Food", (230, 232, 216), 0.1,  500, tile_manager)

dnc = DayNightCycle(500)

num_pawns = 5
pawns = []
for i in range(num_pawns):
    pawns.append(Pawn(0, 0, tile_manager))
    pawns[i].set_random_pos(tile_manager)

avg_event = [0] * 150
avg_inp = [0] * 150
avg_update = [0] * 150
avg_rend = [0] * 150

pc = PieChart()
lg = LineGraph()
pc2 = PieChart(offset_y=250)
lg2 = LineGraph(offset_y=250)
timings = {"move": 0, "item": 0, "pawns": 0, "plants": 0, "move_t": 0, "item_t": 0, "pawns_t": 0, "plants_t": 0}
count = 0
fps = [0]*200

render_pc = False
f1_held = False

dt=0
frame = 0

time_scale = 1

while True:
    start = time.time()
    renderer.draw_calls = 0
    pc.values = {}
    pc2.values = {}

    # Events
    event_start = time.time()
    for event in pygame.event.get():
        ps.handle_event(event)
        hp.handle_event(event)
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
        for p in pawns:
            p.set_random_pos(tile_manager)

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

    # Select Pawns
    if pygame.mouse.get_pressed()[0] and not building_system.building_enabled:
        pawn = closest_to_mouse(pawns, renderer)
        ps.select_pawn(pawn)
        hp.select_pawn(pawn)

    inp_time = time.time()-inp_start

    # Object Updating
    update_start = time.time()
    start_o = time.perf_counter()

    renderer.move(dt)
    t1 = time.perf_counter()

    t2 = time.perf_counter()

    if frame % (30//time_scale) == 0:
        t5 = time.perf_counter()
        item_manager.update(tile_manager)
        t6 = time.perf_counter()
        for pawn in pawns:
            pawn.update(renderer, plant_manager, item_manager)
        t3 = time.perf_counter()

        dnc.update()
        plant_manager.update()
        t4 = time.perf_counter()

        timings["pawns"] += (t3 - t2)
        timings["pawns_t"] = (t3-t2)
        timings["plants"] += (t4 - t3)
        timings["plants_t"] = (t4-t3)
        timings["item"] += (t6 - t5)
        timings["item_t"] = (t6-t5)

    timings["move"] += (t1 - start_o)
    timings["move_t"] = (t1-start_o)
    count += 1

    update_time = time.time() - update_start

    # World Rendering
    rend_start = time.time()
    screen.fill((37, 43, 48))
    tile_manager.render(renderer)
    detail_manager.render(renderer)
    plant_manager.render(renderer)
    item_manager.render(renderer)
    for pawn in pawns:
        pawn.render(renderer)
    
    renderer.render(dnc)

    # UI Rendering
    ps.render(screen)
    hp.render(screen)
    rend_time = time.time()-rend_start

    # Misc
    if dt == 0:
        pygame.display.set_caption(f"Village Simulator | FPS: inf | AVG FPS: inf")
    else:
        fps.append(1/dt)
        fps.pop(0)
        pygame.display.set_caption(f"Village Simulator | FPS: {1/dt:.1f} | AVG FPS: {sum(fps)/len(fps):.1f}")

    avg_event.remove(avg_event[0])
    avg_inp.remove(avg_inp[0])
    avg_update.remove(avg_update[0])
    avg_rend.remove(avg_rend[0])
    avg_event.append(event_time*1000)
    avg_inp.append(inp_time*1000)
    avg_update.append(update_time*1000)
    avg_rend.append(rend_time*1000)
    pc.add_value("E", sum(avg_event)/len(avg_event))
    pc.add_value("I", sum(avg_inp)/len(avg_inp))
    pc.add_value("U", sum(avg_update)/len(avg_update))
    pc.add_value("R", sum(avg_rend)/len(avg_rend))
    lg.add_value(event_time*1000, 0, "Events")
    lg.add_value(inp_time*1000, 1, "Input")
    lg.add_value(update_time*1000, 2, "Update")
    lg.add_value(rend_time*1000, 3, "Rendering")

    pc2.add_value("M", timings["move"]/count*1000)
    pc2.add_value("I", timings["item"]/count*1000)
    pc2.add_value("Pa", timings["pawns"]/count*1000)
    pc2.add_value("Pl", timings["plants"]/count*1000)

    lg2.add_value(timings["move_t"]*1000, 0, "Move")
    lg2.add_value(timings["item_t"]*1000, 1, "Item")
    lg2.add_value(timings["pawns_t"]*1000, 2, "Pawn")
    lg2.add_value(timings["plants_t"]*1000, 3, "Plant")

    if render_pc:
        pc.render(screen)
        lg.render(screen)
        pc2.render(screen)
        lg2.render(screen)

    pygame.display.flip()
    clock.tick(60)
    frame += 1
    dt=time.time()-start