import pygame
from renderer import Renderer
from villager import Villager
from tile_manager import TileManager
import time

pygame.init()

screen = pygame.display.set_mode((1280,720))

clock = pygame.time.Clock()

renderer = Renderer(screen, 16)

tm = TileManager(64,64,8)

v = Villager(20, 20)

dt=0
frame = 0
last_target = (0,0)
path = None

while True:
    renderer.draw_calls = 0
    start = time.time()

    event_start = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    event_time = time.time() - event_start

    inp_start = time.time()
    mouse_x = int((pygame.mouse.get_pos()[0]+renderer.x)/renderer.grid_size)
    mouse_y = int((pygame.mouse.get_pos()[1]+renderer.y)/renderer.grid_size)
    if (mouse_x, mouse_y) != last_target:
        if pygame.mouse.get_pressed()[0]:
            path = tm.find_path(v.x, v.y, mouse_x, mouse_y)
            last_target = (mouse_x, mouse_y)
    inp_time = time.time()-inp_start

    update_start = time.time()
    renderer.move(dt)
    if path and frame % 30 == 0:
        v.follow_path(path)
    update_time = time.time() - update_start

    rend_start = time.time()
    screen.fill("black")
    tm.render(renderer)
    v.render(renderer)

    if path:
        for x,y in path:
            renderer.draw_rect(x, y, 1, 1, (255, 0, 0))
        renderer.draw_circ(mouse_x, mouse_y, 1, (255, 0, 0))

    renderer.render()
    rend_time = time.time()-rend_start

    #pygame.display.set_caption(f"{time.time()-start:.4f}/{(1/60):.4f} - {(time.time()-start)/(1/60)*100:.2f}% frametime used")
    pygame.display.set_caption(
        f"E: {event_time*1000:.2f} "
        f"I: {inp_time*1000:.2f} "
        f"U: {update_time*1000:.2f} "
        f"R: {rend_time*1000:.2f} "
        f"T: {(event_time + inp_time + update_time + rend_time)*1000:.2f} ms "
        f"DC: {renderer.draw_calls}"
    )

    pygame.display.flip()
    clock.tick(60)
    frame += 1
    dt=time.time()-start