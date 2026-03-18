import pygame
from renderer import Renderer
from villager import Villager
from tile_manager import TileManager
from detail_manager import DetailManager
from piechart import PieChart
import time

pygame.init()

screen = pygame.display.set_mode((1280,720))

clock = pygame.time.Clock()

renderer = Renderer(screen, 5)

gen_start = time.time()
tile_manager = TileManager(128,128,8,50)
detail_manager = DetailManager(tile_manager, 5000)
print(f"Generated world of size {tile_manager.width}x{tile_manager.height} with {len(tile_manager.chunks)} chunks in {time.time()-gen_start:.2f}s")

v = Villager(20, 20)

pc = PieChart()

dt=0
frame = 0
last_target = (0,0)
path = None

while True:
    start = time.time()
    renderer.draw_calls = 0
    pc.values = {}

    # Events
    event_start = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    event_time = time.time() - event_start

    # Pathfinding
    inp_start = time.time()
    mouse_x = int((pygame.mouse.get_pos()[0]+renderer.x)/renderer.grid_size)
    mouse_y = int((pygame.mouse.get_pos()[1]+renderer.y)/renderer.grid_size)
    if (mouse_x, mouse_y) != last_target:
        if pygame.mouse.get_pressed()[0]:
            path = tile_manager.find_path(v.x, v.y, mouse_x, mouse_y)
            last_target = (mouse_x, mouse_y)

    # World regen
    if pygame.key.get_pressed()[pygame.K_r]:
        tile_manager = TileManager(128, 128, 8, 50)
        detail_manager = DetailManager(tile_manager, 5000)
    inp_time = time.time()-inp_start

    # Object Updating
    update_start = time.time()
    renderer.move(dt)
    if path and frame % 30 == 0:
        v.follow_path(path)
    update_time = time.time() - update_start

    # Rendering
    rend_start = time.time()
    screen.fill("black")
    tile_manager.render(renderer)
    detail_manager.render(renderer)
    v.render(renderer)

    if path:
        for x,y in path:
            renderer.draw_circ(x, y, 0.5, (255, 0, 0))
        renderer.draw_circ(mouse_x, mouse_y, 1, (255, 0, 0))
    
    renderer.render()
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
    pc.render(screen)

    pygame.display.flip()
    clock.tick(60)
    frame += 1
    dt=time.time()-start