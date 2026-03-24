import pygame
import math

def mouse_in_rect(rect: pygame.Rect) -> bool:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return rect.x < mouse_x < rect.x + rect.width and rect.y < mouse_y < rect.y + rect.height


pygame.font.init()
font = pygame.font.SysFont(None, 18)

def closest_to_mouse(points, renderer):
    mouse_x = int((pygame.mouse.get_pos()[0]+renderer.x)/renderer.grid_size)
    mouse_y = int((pygame.mouse.get_pos()[1]+renderer.y)/renderer.grid_size)
    closest = None
    closest_dist = float("inf")

    for point in points:
        if hasattr(point, "x") and hasattr(point, "y"):
            dx = point.x - mouse_x
            dy = point.y - mouse_y
        else:
            dx = point[0] - mouse_x
            dy = point[1] - mouse_y

        dist = dx*dx + dy*dy

        if dist < closest_dist:
            closest_dist = dist
            closest = point

    if closest_dist < 50:
        return closest
    else:
        return None