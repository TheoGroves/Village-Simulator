import pygame
from renderer import Renderer
from villager import Villager

pygame.init()

screen = pygame.display.set_mode((1280,720))

clock = pygame.time.Clock()

renderer = Renderer(screen, 50)

v = Villager(5, 5)

while True:
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

    screen.fill("black")

    v.render(renderer)
    renderer.draw_rect(5, 5, 3, 2, (255, 0, 255))

    pygame.display.flip()
    dt=1/clock.tick(60)