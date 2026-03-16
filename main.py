import pygame
from renderer import Renderer
from villager import Villager
from tile_manager import TileManager

pygame.init()

screen = pygame.display.set_mode((1280,720))

clock = pygame.time.Clock()

renderer = Renderer(screen, 16)

tm = TileManager(64,64,8)

v = Villager(1, 1)

dt=0
while True:
    import time
    start = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        v.y -= 1 * dt
    if keys[pygame.K_s]:
        v.y += 1 * dt
    if keys[pygame.K_a]:
        v.x -= 1 * dt
    if keys[pygame.K_d]:
        v.x += 1 * dt

    renderer.move(dt)

    screen.fill("black")
    tm.render(renderer)
    v.render(renderer)
    pygame.display.set_caption(f"{time.time()-start:.4f}/{(1/60):.4f} - {(time.time()-start)/(1/60)*100:.2f}% frametime used")

    pygame.display.flip()
    clock.tick(60)
    dt=time.time()-start