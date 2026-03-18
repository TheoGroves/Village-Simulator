import pygame

class PawnSelector:
    def __init__(self):
        self.selected_pawn = "test"

        self.font = pygame.font.SysFont(None, 20)
        self.top_left = (25, 500)
        self.padding = 10

    def render(self, screen):
        if self.selected_pawn:
            rect = pygame.Rect(self.top_left[0], self.top_left[1], 500, 170)
            pygame.draw.rect(screen, (80, 80, 80), rect, border_radius=10)
            pygame.draw.rect(screen, (50, 50, 50), rect, width=6, border_radius=10)
            text_surface = self.font.render(f"Test", True, (255, 255, 255))
            text_rect = text_surface.get_rect(topleft=(self.top_left[0]+self.padding, self.top_left[1]+self.padding))
            screen.blit(text_surface, text_rect)